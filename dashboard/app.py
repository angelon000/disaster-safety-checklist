"""
재난·안전 체크리스트 대시보드 - FastAPI 앱
"""
import sys
from pathlib import Path

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn

from utils.config import config
from checklist.generator import ChecklistGenerator
from checklist.templates import ChecklistTemplates, FacilityType, CheckPhase, FocusArea
from database import Database

# FastAPI 앱 생성
app = FastAPI(
    title="재난·안전 체크리스트 대시보드",
    description="재난·안전 체크리스트 자동 생성 시스템",
    version="1.0.0"
)

# 정적 파일 및 템플릿 설정
dashboard_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=dashboard_dir / "static"), name="static")
templates = Jinja2Templates(directory=dashboard_dir / "templates")

# 데이터베이스 및 생성기 초기화
db = Database()
generator = ChecklistGenerator(config.settings)
template_manager = ChecklistTemplates()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 페이지"""
    # 통계 정보
    stats = db.get_stats()

    # 최근 프로젝트 (최대 5개)
    recent_projects = db.get_all_projects(limit=5, offset=0)

    # 템플릿 정보
    facility_types = [ft.value for ft in FacilityType]
    check_phases = [cp.value for cp in CheckPhase]
    focus_areas = [fa.value for fa in FocusArea]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "stats": stats,
        "recent_projects": recent_projects,
        "facility_types": facility_types,
        "check_phases": check_phases,
        "focus_areas": focus_areas
    })


@app.post("/api/generate")
async def generate_checklist(
    keyword: str = Form(...),
    facility_type: str = Form(...),
    check_phase: str = Form(...),
    focus_area: Optional[str] = Form(None),
    collect_data: bool = Form(False)
):
    """체크리스트 생성 API"""
    try:
        # 체크리스트 생성
        result = generator.generate(
            keyword=keyword,
            facility_type=facility_type,
            check_phase=check_phase,
            focus_area=focus_area,
            collect_data=collect_data
        )

        # Markdown 파일 저장
        md_path = generator.export_to_markdown(result)
        json_path = generator.export_to_json(result)

        # 데이터베이스에 저장
        project_data = {
            'keyword': keyword,
            'facility_type': facility_type,
            'check_phase': check_phase,
            'focus_area': focus_area,
            'data_collected': collect_data,
            'metadata': result.get('metadata'),
            'checklist': result.get('checklist'),
            'research_summary': result.get('research_summary'),
            'output_path_md': md_path,
            'output_path_json': json_path
        }

        project_id = db.save_project(project_data)

        return JSONResponse({
            "success": True,
            "project_id": project_id,
            "message": "체크리스트가 생성되었습니다."
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.get("/result/{project_id}", response_class=HTMLResponse)
async def show_result(request: Request, project_id: int):
    """결과 페이지"""
    project = db.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")

    # 체크리스트 데이터 준비
    checklist = project.get('checklist_data', {})
    research_summary = project.get('research_summary', {})
    metadata = project.get('metadata', {})

    # 전체 질문 수 계산
    total_questions = sum(len(category.get('questions', [])) for category in checklist.values())

    return templates.TemplateResponse("result.html", {
        "request": request,
        "project": project,
        "checklist": checklist,
        "research_summary": research_summary,
        "metadata": metadata,
        "total_questions": total_questions
    })


@app.get("/projects", response_class=HTMLResponse)
async def list_projects(
    request: Request,
    page: int = 1,
    keyword: Optional[str] = None
):
    """프로젝트 목록 페이지"""
    limit = 20
    offset = (page - 1) * limit

    projects = db.get_all_projects(
        limit=limit,
        offset=offset,
        keyword_filter=keyword
    )

    total_count = db.get_project_count(keyword_filter=keyword)
    total_pages = (total_count + limit - 1) // limit

    # 통계 정보 (필터링용)
    stats = db.get_stats()

    return templates.TemplateResponse("list.html", {
        "request": request,
        "projects": projects,
        "page": page,
        "total_pages": total_pages,
        "keyword": keyword or "",
        "stats": stats
    })


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: int):
    """프로젝트 삭제 API"""
    success = db.delete_project(project_id)

    if success:
        return JSONResponse({"success": True, "message": "삭제되었습니다."})
    else:
        return JSONResponse({"success": False, "error": "삭제 실패"}, status_code=404)


@app.get("/api/projects/{project_id}")
async def get_project_api(project_id: int):
    """프로젝트 조회 API (JSON)"""
    project = db.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")

    return JSONResponse(project)


@app.get("/download/{project_id}/markdown")
async def download_markdown(project_id: int):
    """Markdown 파일 다운로드"""
    project = db.get_project(project_id)

    if not project or not project.get('output_path_md'):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    file_path = project['output_path_md']
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")

    return FileResponse(
        file_path,
        media_type='text/markdown',
        filename=Path(file_path).name
    )


@app.get("/download/{project_id}/json")
async def download_json(project_id: int):
    """JSON 파일 다운로드"""
    project = db.get_project(project_id)

    if not project or not project.get('output_path_json'):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    file_path = project['output_path_json']
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")

    return FileResponse(
        file_path,
        media_type='application/json',
        filename=Path(file_path).name
    )


@app.get("/api/stats")
async def get_stats():
    """통계 API"""
    stats = db.get_stats()
    return JSONResponse(stats)


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import socket

    # 로컬 IP 주소 가져오기
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("\n" + "="*70)
    print("  재난·안전 체크리스트 대시보드")
    print("="*70)
    print("\n  🌐 로컬 접속: http://localhost:8000")
    print(f"  🌍 네트워크 접속: http://{local_ip}:8000")
    print("  📚 API 문서: http://localhost:8000/docs")
    print("\n  💡 외부 접속을 위해 방화벽 8000번 포트를 열어주세요.")
    print("  🛑 종료하려면 Ctrl+C를 누르세요.\n")

    # 0.0.0.0으로 변경하여 외부 접속 허용
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
