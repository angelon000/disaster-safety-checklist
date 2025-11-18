"""
대시보드용 SQLite 데이터베이스 관리
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class Database:
    """프로젝트 관리용 데이터베이스"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "projects.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_db()

    def _init_db(self):
        """데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    facility_type TEXT,
                    check_phase TEXT,
                    content_type TEXT,
                    business_stage TEXT,
                    focus_area TEXT,
                    data_collected BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    checklist_data TEXT,
                    research_summary TEXT,
                    output_path_md TEXT,
                    output_path_json TEXT
                )
            """)

            # 기존 테이블에 새 컬럼 추가 (있으면 무시)
            try:
                conn.execute("ALTER TABLE projects ADD COLUMN facility_type TEXT")
            except sqlite3.OperationalError:
                pass  # 컬럼이 이미 존재

            try:
                conn.execute("ALTER TABLE projects ADD COLUMN check_phase TEXT")
            except sqlite3.OperationalError:
                pass  # 컬럼이 이미 존재

            conn.commit()

    def save_project(self, project_data: Dict[str, Any]) -> int:
        """프로젝트 저장"""
        with sqlite3.connect(self.db_path) as conn:
            # 새 필드와 구 필드 모두 지원
            facility_type = project_data.get('facility_type') or project_data.get('content_type')
            check_phase = project_data.get('check_phase') or project_data.get('business_stage')

            cursor = conn.execute("""
                INSERT INTO projects (
                    keyword, facility_type, check_phase, content_type, business_stage,
                    focus_area, data_collected, metadata, checklist_data, research_summary,
                    output_path_md, output_path_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project_data.get('keyword'),
                facility_type,
                check_phase,
                facility_type,  # 하위 호환성을 위해 content_type에도 저장
                check_phase,    # 하위 호환성을 위해 business_stage에도 저장
                project_data.get('focus_area'),
                project_data.get('data_collected', False),
                json.dumps(project_data.get('metadata', {}), ensure_ascii=False),
                json.dumps(project_data.get('checklist', {}), ensure_ascii=False),
                json.dumps(project_data.get('research_summary', {}), ensure_ascii=False),
                project_data.get('output_path_md'),
                project_data.get('output_path_json')
            ))
            conn.commit()
            return cursor.lastrowid

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """프로젝트 조회"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM projects WHERE id = ?",
                (project_id,)
            )
            row = cursor.fetchone()

            if row:
                return self._row_to_dict(row)
            return None

    def get_all_projects(
        self,
        limit: int = 50,
        offset: int = 0,
        keyword_filter: str = None
    ) -> List[Dict[str, Any]]:
        """모든 프로젝트 목록 조회"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            query = "SELECT * FROM projects"
            params = []

            if keyword_filter:
                query += " WHERE keyword LIKE ?"
                params.append(f"%{keyword_filter}%")

            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

            return [self._row_to_dict(row) for row in rows]

    def delete_project(self, project_id: int) -> bool:
        """프로젝트 삭제"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM projects WHERE id = ?",
                (project_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_project_count(self, keyword_filter: str = None) -> int:
        """전체 프로젝트 수"""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT COUNT(*) FROM projects"
            params = []

            if keyword_filter:
                query += " WHERE keyword LIKE ?"
                params.append(f"%{keyword_filter}%")

            cursor = conn.execute(query, params)
            return cursor.fetchone()[0]

    def get_stats(self) -> Dict[str, Any]:
        """통계 정보"""
        with sqlite3.connect(self.db_path) as conn:
            # 전체 프로젝트 수
            total = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]

            # 시설 유형별 분포 (새 필드 우선, 없으면 구 필드)
            facility_types = conn.execute("""
                SELECT COALESCE(facility_type, content_type) as type, COUNT(*) as count
                FROM projects
                GROUP BY type
                ORDER BY count DESC
            """).fetchall()

            # 점검 단계별 분포 (새 필드 우선, 없으면 구 필드)
            check_phases = conn.execute("""
                SELECT COALESCE(check_phase, business_stage) as phase, COUNT(*) as count
                FROM projects
                GROUP BY phase
                ORDER BY count DESC
            """).fetchall()

            # 최근 7일 생성 수
            recent = conn.execute("""
                SELECT COUNT(*) FROM projects
                WHERE created_at >= datetime('now', '-7 days')
            """).fetchone()[0]

            return {
                'total_projects': total,
                'facility_types': dict(facility_types),
                'check_phases': dict(check_phases),
                # 하위 호환성을 위해 유지
                'content_types': dict(facility_types),
                'business_stages': dict(check_phases),
                'recent_7days': recent
            }

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """SQLite Row를 딕셔너리로 변환"""
        data = dict(row)

        # JSON 필드 파싱
        if data.get('metadata'):
            data['metadata'] = json.loads(data['metadata'])
        if data.get('checklist_data'):
            data['checklist_data'] = json.loads(data['checklist_data'])
        if data.get('research_summary'):
            data['research_summary'] = json.loads(data['research_summary'])

        return data
