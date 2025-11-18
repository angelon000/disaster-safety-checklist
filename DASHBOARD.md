# 재난·안전 체크리스트 대시보드 가이드

## 🌐 웹 대시보드 사용법

### 빠른 시작

#### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

필요한 패키지:
- `fastapi==0.104.1`: 웹 프레임워크
- `uvicorn`: ASGI 서버
- `jinja2==3.1.2`: 템플릿 엔진
- `python-multipart`: 폼 데이터 처리

#### 2. 대시보드 실행
```bash
python run_dashboard.py
```

자동으로 브라우저가 열리고 `http://localhost:8000`으로 이동합니다.

### 주요 기능

#### 1. **홈 페이지** (/)
- 프로젝트 생성 폼
- 통계 대시보드 (전체 프로젝트 수, 시설 유형별/점검 단계별 분포 차트)
- 빠른 가이드

**입력 항목:**
- 키워드 (필수) - 예: "○○시 지자체 재난안전", "△△ 건설현장"
- 시설 유형 (필수) - 지자체, 건설현장, 제조사업장, 물류창고, 상업시설, 교육시설, 의료시설, 주거시설, 기타
- 점검 단계 (필수) - 초기 평가, 정기 점검, 재난 발생 시, 복구 후, 연간 종합
- 중점 영역 (선택) - 안전 중심, 법규 중심, 예방 중심, 대응 중심
- 데이터 수집 여부 (체크박스, v1.0: 더미 데이터)

#### 2. **결과 페이지** (/result/{id})
- 생성된 체크리스트 표시 (8개 카테고리, 28개 질문)
- 리서치 요약 (웹·논문·기술·API 건수)
- 카테고리별 질문 및 참고자료
- Markdown/JSON 다운로드 링크

#### 3. **프로젝트 목록** (/projects)
- 전체 프로젝트 카드 형식 목록
- 키워드 검색 기능
- 페이지네이션 (기본 9개씩)
- 프로젝트 상세 보기 및 삭제

### API 엔드포인트

#### 체크리스트 생성
```http
POST /api/generate
Content-Type: multipart/form-data

keyword: "○○시 지자체 재난안전"
facility_type: "지자체"
check_phase: "초기 평가"
focus_area: "법규 중심"
collect_data: true
```

**응답:**
```json
{
  "success": true,
  "project_id": 1,
  "message": "체크리스트가 생성되었습니다."
}
```

#### 프로젝트 목록 조회
```http
GET /api/projects?page=1&per_page=9&keyword=건설현장
```

**응답:**
```json
{
  "projects": [
    {
      "id": 1,
      "keyword": "△△ 건설현장",
      "facility_type": "건설현장",
      "check_phase": "정기 점검",
      "created_at": "2025-11-18T14:45:00",
      "output_path_md": "output/checklist_△△ 건설현장_20251118_144500.md",
      "output_path_json": "output/checklist_△△ 건설현장_20251118_144500.json"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 9,
  "pages": 1
}
```

#### 프로젝트 상세 조회
```http
GET /api/projects/{project_id}
```

**응답:**
```json
{
  "id": 1,
  "keyword": "○○시 지자체 재난안전",
  "facility_type": "지자체",
  "check_phase": "초기 평가",
  "focus_area": "법규 중심",
  "created_at": "2025-11-18T14:45:00",
  "metadata": {
    "keyword": "○○시 지자체 재난안전",
    "facility_type": "지자체",
    "check_phase": "초기 평가",
    "focus_area": "법규 중심",
    "generated_at": "2025-11-18T14:45:00",
    "version": "1.0"
  },
  "checklist_data": {
    "risk_assessment": {
      "info": {
        "name": "위험도 평가",
        "description": "과거 재난 이력, 지리적 위험, 취약성 분석",
        "priority": 10,
        "icon": "⚠️"
      },
      "questions": [...]
    },
    ...
  },
  "research_summary": {
    "web_sources": 10,
    "papers": 8,
    "tech_projects": 5,
    "apis": 3
  }
}
```

#### 프로젝트 삭제
```http
DELETE /api/projects/{project_id}
```

**응답:**
```json
{
  "success": true,
  "message": "프로젝트가 삭제되었습니다."
}
```

#### 통계 조회
```http
GET /api/stats
```

**응답:**
```json
{
  "total_projects": 15,
  "facility_types": {
    "지자체": 5,
    "건설현장": 4,
    "의료시설": 3,
    "교육시설": 2,
    "상업시설": 1
  },
  "check_phases": {
    "초기 평가": 6,
    "정기 점검": 5,
    "재난 발생 시": 2,
    "연간 종합": 2
  },
  "recent_7days": 8
}
```

#### 파일 다운로드
```http
GET /download/{project_id}/markdown
GET /download/{project_id}/json
```

**응답**: 파일 다운로드 (Content-Type: text/markdown 또는 application/json)

#### 헬스 체크
```http
GET /health
```

**응답:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 데이터베이스 구조 (SQLite)

**테이블: projects**

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | INTEGER | 프로젝트 ID (Primary Key) |
| keyword | TEXT | 키워드 (필수) |
| facility_type | TEXT | 시설 유형 (v1.0 신규) |
| check_phase | TEXT | 점검 단계 (v1.0 신규) |
| content_type | TEXT | 콘텐츠 유형 (하위 호환용) |
| business_stage | TEXT | 사업 단계 (하위 호환용) |
| focus_area | TEXT | 중점 영역 |
| data_collected | BOOLEAN | 데이터 수집 여부 |
| created_at | TIMESTAMP | 생성일시 |
| metadata | TEXT (JSON) | 메타데이터 |
| checklist_data | TEXT (JSON) | 체크리스트 데이터 |
| research_summary | TEXT (JSON) | 리서치 요약 |
| output_path_md | TEXT | Markdown 파일 경로 |
| output_path_json | TEXT | JSON 파일 경로 |

**데이터베이스 파일 위치**: `data/projects.db`

### 사용 예시

#### 1. 지자체 재난안전 점검 체크리스트 생성
1. 홈 페이지에서 입력:
   - 키워드: "○○시 지자체 재난안전"
   - 시설 유형: 지자체
   - 점검 단계: 초기 평가
   - 중점 영역: 법규 중심
   - 데이터 수집: 체크
2. "체크리스트 생성" 버튼 클릭
3. 결과 페이지로 이동하여 체크리스트 확인
4. Markdown 또는 JSON 파일 다운로드

#### 2. 건설현장 정기 점검 체크리스트
1. 홈 페이지에서 입력:
   - 키워드: "△△ 건설현장"
   - 시설 유형: 건설현장
   - 점검 단계: 정기 점검
   - 중점 영역: 안전 중심
2. 생성 후 결과 페이지에서 안전 점검 중심 체크리스트 확인
3. 프로젝트 목록에서 과거 점검 이력 조회

#### 3. 의료시설 재난 대응 매뉴얼
1. 홈 페이지에서 입력:
   - 키워드: "◇◇ 의료시설"
   - 시설 유형: 의료시설
   - 점검 단계: 재난 발생 시
   - 중점 영역: 대응 중심
2. 비상 대응 중심 체크리스트 생성
3. 결과 페이지에서 재난 대응 조직, 외부 지원 절차 등 확인

### 기술 스택

- **백엔드**: FastAPI 0.104.1
- **템플릿 엔진**: Jinja2 3.1.2
- **데이터베이스**: SQLite
- **프론트엔드**: Bootstrap 5, Chart.js 4.4.0
- **서버**: Uvicorn (ASGI)
- **아이콘**: Bootstrap Icons

### 파일 구조

```
dashboard/
├── app.py              # FastAPI 앱 메인
├── database.py         # SQLite 데이터베이스 관리 클래스
└── templates/          # Jinja2 템플릿
    ├── base.html      # 공통 레이아웃
    ├── index.html     # 홈 (통계 + 생성 폼)
    ├── list.html      # 프로젝트 목록
    └── result.html    # 결과 페이지 (체크리스트 미리보기)
```

### 환경 설정

#### 포트 변경
`run_dashboard.py` 수정:
```python
uvicorn.run(
    app,
    host="127.0.0.1",
    port=8080,  # 원하는 포트로 변경
    log_level="info"
)
```

#### 데이터베이스 경로 변경
`dashboard/database.py` 수정:
```python
def __init__(self, db_path: str = None):
    if db_path is None:
        db_path = Path(__file__).parent.parent / "custom_path" / "projects.db"
```

### 문제 해결

#### 브라우저가 자동으로 열리지 않는 경우
수동으로 `http://localhost:8000` 접속

#### 포트 충돌
다른 프로그램이 8000번 포트를 사용 중이라면 위의 "포트 변경" 참조

#### 데이터베이스 초기화
```bash
rm data/projects.db
python run_dashboard.py  # 재실행 시 자동 생성
```

### v2.0 계획 기능

- 사용자 인증 및 권한 관리
- 프로젝트 편집 기능 (수정)
- 점검 결과 입력 및 이력 관리 (완료/미완료 체크)
- 실시간 알림 (점검일 임박, 위험 알림)
- 대시보드 차트 고도화 (시계열 분석, 위험도 히트맵)
- 모바일 반응형 개선 및 PWA 지원
- 프로젝트 공유 및 협업 기능

---

**Generated by 재난·안전 체크리스트 시스템 v1.0**
