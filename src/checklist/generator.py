"""
체크리스트 생성 엔진
"""
import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

from checklist.templates import ChecklistTemplates
from collectors.web_researcher import WebResearcher
from collectors.paper_researcher import PaperResearcher
from collectors.tech_researcher import TechResearcher
from collectors.api_researcher import APIResearcher


class ChecklistGenerator:
    """체크리스트 자동 생성기"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.templates = ChecklistTemplates()

        # 데이터 수집기 초기화
        self.web_researcher = WebResearcher(
            max_results=self.config.get('max_results_per_source', 10)
        )
        self.paper_researcher = PaperResearcher(
            max_results=self.config.get('max_results_per_source', 10)
        )
        self.tech_researcher = TechResearcher(
            github_token=self.config.get('api_keys', {}).get('github'),
            max_results=self.config.get('max_results_per_source', 10)
        )
        self.api_researcher = APIResearcher(
            public_data_api_key=self.config.get('api_keys', {}).get('public_data')
        )

    def generate(
        self,
        keyword: str,
        facility_type: str,
        check_phase: str,
        focus_area: str = None,
        collect_data: bool = True
    ) -> Dict[str, Any]:
        """
        맞춤형 체크리스트 생성

        Args:
            keyword: 시설/사업장 키워드
            facility_type: 시설 유형
            check_phase: 점검 단계
            focus_area: 관심 영역
            collect_data: 데이터 수집 실행 여부

        Returns:
            생성된 체크리스트 및 참고자료
        """
        print(f"\n{'='*60}")
        print(f"체크리스트 생성 시작: {keyword}")
        print(f"시설 유형: {facility_type}, 점검 단계: {check_phase}")
        print(f"{'='*60}\n")

        # 1. 템플릿 가져오기
        template = self.templates.get_template_by_type_and_stage(
            facility_type, check_phase, focus_area
        )

        # 2. 데이터 수집 (선택)
        research_data = {}
        if collect_data:
            print("📚 리서치 데이터 수집 중...\n")
            research_data = self._collect_research_data(keyword)

        # 3. 체크리스트와 리서치 매핑
        enriched_checklist = self._enrich_checklist_with_research(
            template, research_data, keyword
        )

        # 4. 메타데이터 추가
        result = {
            'metadata': {
                'keyword': keyword,
                'facility_type': facility_type,
                'check_phase': check_phase,
                'focus_area': focus_area,
                'generated_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'checklist': enriched_checklist,
            'research_summary': self._create_research_summary(research_data),
            'recommendations': self._generate_recommendations(research_data)
        }

        print("\n✅ 체크리스트 생성 완료!\n")

        return result

    def _collect_research_data(self, keyword: str) -> Dict[str, Any]:
        """리서치 데이터 수집"""
        data = {
            'web': [],
            'papers': [],
            'tech': [],
            'apis': []
        }

        try:
            # 웹 리서치
            print("  🌐 웹 리서치...")
            data['web'] = self.web_researcher.search(keyword)
            print(f"     ✓ {len(data['web'])} 건 수집")

            # 논문 리서치
            print("  📄 논문 리서치...")
            data['papers'] = self.paper_researcher.search(keyword)
            print(f"     ✓ {len(data['papers'])} 건 수집")

            # 기술 리서치
            print("  💻 기술 트렌드...")
            data['tech'] = self.tech_researcher.search(keyword)
            print(f"     ✓ {len(data['tech'])} 건 수집")

            # API 리서치
            print("  🔌 API 정보...")
            data['apis'] = self.api_researcher.search(keyword)
            print(f"     ✓ {len(data['apis'])} 건 수집")

        except Exception as e:
            print(f"  ⚠️  데이터 수집 중 오류: {e}")

        return data

    def _enrich_checklist_with_research(
        self,
        template: Dict[str, Any],
        research_data: Dict[str, Any],
        keyword: str
    ) -> Dict[str, Any]:
        """체크리스트에 리서치 데이터 매핑"""
        enriched = {}

        for category_id, category_data in template.items():
            questions = category_data['questions']

            # 각 질문에 관련 리서치 자료 연결
            enriched_questions = []
            for question in questions:
                question_keywords = question.get('research_keywords', [])

                # 관련 자료 찾기
                related_resources = self._find_related_resources(
                    question_keywords,
                    research_data,
                    keyword
                )

                enriched_question = {
                    **question,
                    'related_resources': related_resources,
                    'resource_count': len(related_resources),
                    'needs_more_research': len(related_resources) < 3
                }

                enriched_questions.append(enriched_question)

            enriched[category_id] = {
                'info': category_data['info'],
                'questions': enriched_questions,
                'total_resources': sum(q['resource_count'] for q in enriched_questions)
            }

        return enriched

    def _find_related_resources(
        self,
        keywords: List[str],
        research_data: Dict[str, Any],
        main_keyword: str
    ) -> List[Dict[str, Any]]:
        """키워드와 관련된 리서치 자료 찾기"""
        resources = []

        # 웹 자료
        for item in research_data.get('web', []):
            if self._is_relevant(item, keywords, main_keyword):
                resources.append({
                    'type': 'web',
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'source': item.get('source', ''),
                    'summary': item.get('summary', ''),
                    'credibility': item.get('credibility_score', 0.5)
                })

        # 논문
        for item in research_data.get('papers', []):
            if self._is_relevant(item, keywords, main_keyword):
                resources.append({
                    'type': 'paper',
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'authors': item.get('authors', []),
                    'year': item.get('year'),
                    'citations': item.get('citations', 0),
                    'source': item.get('source', '')
                })

        # 기술 자료
        for item in research_data.get('tech', []):
            if self._is_relevant(item, keywords, main_keyword):
                resources.append({
                    'type': 'tech',
                    'name': item.get('name', ''),
                    'url': item.get('url', ''),
                    'description': item.get('description', ''),
                    'stars': item.get('stars', 0),
                    'language': item.get('language', ''),
                    'source': item.get('source', '')
                })

        # API 자료
        for item in research_data.get('apis', []):
            if self._is_relevant(item, keywords, main_keyword):
                resources.append({
                    'type': 'api',
                    'name': item.get('name', ''),
                    'url': item.get('url', ''),
                    'description': item.get('description', ''),
                    'provider': item.get('provider', ''),
                    'usage_policy': item.get('usage_policy', '')
                })

        # 관련성 점수로 정렬
        resources.sort(key=lambda x: x.get('credibility', 0.5), reverse=True)

        return resources[:5]  # 상위 5개만

    def _is_relevant(
        self,
        item: Dict[str, Any],
        keywords: List[str],
        main_keyword: str
    ) -> bool:
        """항목이 키워드와 관련있는지 확인"""
        # 제목이나 설명에서 키워드 검색
        text = (
            item.get('title', '') + ' ' +
            item.get('description', '') + ' ' +
            item.get('summary', '') + ' ' +
            item.get('name', '')
        ).lower()

        # 메인 키워드 포함 확인
        if main_keyword.lower() in text:
            return True

        # 관련 키워드 확인
        for keyword in keywords:
            if keyword.lower() in text:
                return True

        return False

    def _create_research_summary(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """리서치 요약 생성"""
        return {
            'web_sources': len(research_data.get('web', [])),
            'papers': len(research_data.get('papers', [])),
            'tech_projects': len(research_data.get('tech', [])),
            'apis': len(research_data.get('apis', [])),
            'total_resources': sum([
                len(research_data.get('web', [])),
                len(research_data.get('papers', [])),
                len(research_data.get('tech', [])),
                len(research_data.get('apis', []))
            ]),
            'maturity_analysis': {
                'papers': self.paper_researcher.analyze_maturity(
                    research_data.get('papers', [])
                ),
                'tech': self.tech_researcher.analyze_tech_maturity(
                    research_data.get('tech', [])
                )
            }
        }

    def _generate_recommendations(self, research_data: Dict[str, Any]) -> List[str]:
        """추천 사항 생성"""
        recommendations = []

        # 논문 기반 추천
        papers = research_data.get('papers', [])
        if len(papers) < 5:
            recommendations.append(
                "⚠️  관련 연구 자료가 부족합니다. 최신 안전 기준을 별도로 확인하시기 바랍니다."
            )
        elif len(papers) > 20:
            recommendations.append(
                "✅ 충분한 연구 자료가 있어 검증된 안전 기준을 참고할 수 있습니다."
            )

        # 기술 프로젝트 기반 추천
        tech = research_data.get('tech', [])
        if tech:
            avg_stars = sum(t.get('stars', 0) for t in tech) / len(tech)
            if avg_stars > 500:
                recommendations.append(
                    "✅ 관련 오픈소스 도구들이 있어 재난 관리 시스템 구축이 용이합니다."
                )

        # API 기반 추천
        apis = research_data.get('apis', [])
        if apis:
            recommendations.append(
                f"💡 {len(apis)}개의 공공 API를 활용하여 실시간 재난 정보를 모니터링할 수 있습니다."
            )

        return recommendations

    def export_to_markdown(self, checklist_data: Dict[str, Any], output_path: str = None):
        """체크리스트를 Markdown 파일로 내보내기"""
        if output_path is None:
            output_dir = Path(self.config.get('output_dir', 'output'))
            output_dir.mkdir(exist_ok=True, parents=True)
            filename = f"checklist_{checklist_data['metadata']['keyword']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_path = output_dir / filename

        md_content = self._generate_markdown(checklist_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"📄 Markdown 파일 생성: {output_path}")
        return str(output_path)

    def export_to_json(self, checklist_data: Dict[str, Any], output_path: str = None):
        """체크리스트를 JSON 파일로 내보내기"""
        if output_path is None:
            output_dir = Path(self.config.get('output_dir', 'output'))
            output_dir.mkdir(exist_ok=True, parents=True)
            filename = f"checklist_{checklist_data['metadata']['keyword']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(checklist_data, f, indent=2, ensure_ascii=False)

        print(f"📄 JSON 파일 생성: {output_path}")
        return str(output_path)

    def _generate_markdown(self, data: Dict[str, Any]) -> str:
        """Markdown 형식으로 변환"""
        md = []

        # 헤더
        metadata = data['metadata']
        md.append(f"# {metadata['keyword']} - 재난·안전 체크리스트\n")
        md.append(f"**시설 유형**: {metadata.get('facility_type', metadata.get('content_type', 'N/A'))}\n")
        md.append(f"**점검 단계**: {metadata.get('check_phase', metadata.get('business_stage', 'N/A'))}\n")
        md.append(f"**생성일시**: {metadata['generated_at']}\n")
        md.append("\n---\n")

        # 리서치 요약
        summary = data['research_summary']
        md.append("## 📊 리서치 요약\n")
        md.append(f"- 웹 자료: {summary['web_sources']}건\n")
        md.append(f"- 논문: {summary['papers']}건\n")
        md.append(f"- 기술 프로젝트: {summary['tech_projects']}건\n")
        md.append(f"- API: {summary['apis']}건\n")
        md.append("\n")

        # 추천 사항
        if data['recommendations']:
            md.append("## 💡 추천 사항\n")
            for rec in data['recommendations']:
                md.append(f"{rec}\n")
            md.append("\n")

        md.append("---\n\n")

        # 체크리스트
        checklist = data['checklist']
        for category_id, category_data in checklist.items():
            info = category_data['info']
            md.append(f"## {info['icon']} {info['name']}\n")
            md.append(f"*{info['description']}*\n\n")

            for i, question in enumerate(category_data['questions'], 1):
                importance_badge = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(question['importance'], '')

                md.append(f"### {i}. {question['question']} {importance_badge}\n")

                if question['type'] == 'select':
                    md.append("**선택지:**\n")
                    for option in question.get('options', []):
                        md.append(f"- [ ] {option}\n")
                else:
                    md.append("**답변:**\n\n")
                    md.append("```\n\n```\n")

                # 관련 자료
                resources = question.get('related_resources', [])
                if resources:
                    md.append("\n**참고 자료:**\n")
                    for res in resources[:3]:  # 상위 3개만
                        if res['type'] == 'web':
                            md.append(f"- [{res['title']}]({res['url']}) - {res['source']}\n")
                        elif res['type'] == 'paper':
                            md.append(f"- 📄 [{res['title']}]({res['url']}) ({res.get('year', 'N/A')})\n")
                        elif res['type'] == 'tech':
                            md.append(f"- 💻 [{res['name']}]({res['url']}) - ⭐ {res.get('stars', 0)}\n")
                        elif res['type'] == 'api':
                            md.append(f"- 🔌 [{res['name']}]({res['url']}) - {res.get('provider', '')}\n")

                if question.get('needs_more_research'):
                    md.append("\n⚠️ *추가 리서치가 필요합니다.*\n")

                md.append("\n")

            md.append("---\n\n")

        return ''.join(md)
