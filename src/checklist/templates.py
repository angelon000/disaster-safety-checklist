"""
체크리스트 템플릿 정의
"""
from typing import Dict, List, Any
from enum import Enum


class FacilityType(str, Enum):
    """시설 유형"""
    LOCAL_GOV = "지자체"
    CONSTRUCTION = "건설현장"
    MANUFACTURING = "제조사업장"
    WAREHOUSE = "물류창고"
    COMMERCIAL = "상업시설"
    EDUCATIONAL = "교육시설"
    MEDICAL = "의료시설"
    RESIDENTIAL = "주거시설"
    OTHER = "기타"


class CheckPhase(str, Enum):
    """점검 단계"""
    INITIAL = "초기 평가"
    REGULAR = "정기 점검"
    EMERGENCY = "재난 발생 시"
    RECOVERY = "복구 후"
    ANNUAL = "연간 종합"


class FocusArea(str, Enum):
    """관심 영역"""
    SAFETY = "안전 중심"
    LEGAL = "법규 중심"
    PREVENTION = "예방 중심"
    RESPONSE = "대응 중심"


class ChecklistTemplates:
    """체크리스트 템플릿 관리"""

    def __init__(self):
        self.categories = self._define_categories()
        self.templates = self._define_templates()

    def _define_categories(self) -> Dict[str, Dict[str, Any]]:
        """체크리스트 카테고리 정의"""
        return {
            "risk_assessment": {
                "name": "위험도 평가",
                "description": "과거 재난 이력, 지리적 위험, 취약성 분석",
                "priority": 10,
                "icon": "⚠️"
            },
            "disaster_prep": {
                "name": "재난 대비",
                "description": "대피 계획, 비상 물품, 교육·훈련",
                "priority": 9,
                "icon": "🛡️"
            },
            "safety_check": {
                "name": "안전 점검",
                "description": "시설물 점검, 장비 관리, 위험물 관리",
                "priority": 9,
                "icon": "🔍"
            },
            "emergency_response": {
                "name": "비상 대응",
                "description": "비상연락망, 대응 조직, 실시간 모니터링",
                "priority": 10,
                "icon": "🚨"
            },
            "legal_compliance": {
                "name": "법규·인증",
                "description": "안전 관련 법규, 의무 인증, 정기 보고",
                "priority": 8,
                "icon": "📋"
            },
            "organization": {
                "name": "조직·책임",
                "description": "안전 관리자, 역할 분담, 예산 확보",
                "priority": 7,
                "icon": "👥"
            },
            "monitoring": {
                "name": "모니터링·개선",
                "description": "점검 이력 관리, 사후 조치, 개선 활동",
                "priority": 6,
                "icon": "📊"
            },
            "cooperation": {
                "name": "지역 협력",
                "description": "소방서·경찰서 협력, 지역 공동 대응, 정보 공유",
                "priority": 5,
                "icon": "🤝"
            }
        }

    def _define_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """카테고리별 질문 템플릿 정의"""
        return {
            "risk_assessment": [
                {
                    "id": "risk_01",
                    "question": "최근 5년간 발생한 주요 재난은 무엇인가요? (화재, 침수, 지진 등)",
                    "type": "text",
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["재난이력", "과거사고", "재해현황"]
                },
                {
                    "id": "risk_02",
                    "question": "해당 지역의 재난 위험도는? (홍수·지진·산사태 등)",
                    "type": "select",
                    "options": ["높음", "중간", "낮음", "미파악"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["재난위험지도", "지역위험도", "재해위험"]
                },
                {
                    "id": "risk_03",
                    "question": "시설의 구조적 취약점은 파악되었나요?",
                    "type": "select",
                    "options": ["파악 완료", "파악 중", "미파악"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["구조안전", "내진설계", "노후건물"]
                },
                {
                    "id": "risk_04",
                    "question": "인근 위험 요소는? (위험물 저장소, 가스 시설 등)",
                    "type": "text",
                    "importance": "medium",
                    "required": False,
                    "research_keywords": ["위험요소", "주변환경", "위험시설"]
                }
            ],
            "disaster_prep": [
                {
                    "id": "prep_01",
                    "question": "대피 계획이 수립되어 있나요? (경로, 대피소, 안내판)",
                    "type": "select",
                    "options": ["수립 완료", "수립 중", "미수립"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["대피계획", "대피로", "대피소"]
                },
                {
                    "id": "prep_02",
                    "question": "비상 물품은 확보되어 있나요? (구호품, 비상식량, 구급약)",
                    "type": "select",
                    "options": ["충분", "부족", "없음"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["비상물품", "구호물자", "재난용품"]
                },
                {
                    "id": "prep_03",
                    "question": "재난 대응 교육·훈련을 실시하고 있나요?",
                    "type": "select",
                    "options": ["정기 실시", "비정기 실시", "미실시"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["재난훈련", "안전교육", "대피훈련"]
                },
                {
                    "id": "prep_04",
                    "question": "소화 설비(소화기, 스프링클러)는 정상 작동하나요?",
                    "type": "select",
                    "options": ["정상", "일부 고장", "점검 필요"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["소화설비", "소화기", "스프링클러"]
                }
            ],
            "safety_check": [
                {
                    "id": "safety_01",
                    "question": "시설물(건물, 구조물) 안전 점검 주기는?",
                    "type": "select",
                    "options": ["월 1회", "분기 1회", "연 1회", "미실시"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["시설물안전", "정기점검", "구조물점검"]
                },
                {
                    "id": "safety_02",
                    "question": "전기·가스 설비 점검을 정기적으로 하고 있나요?",
                    "type": "select",
                    "options": ["정기 점검", "비정기 점검", "미실시"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["전기안전", "가스점검", "설비관리"]
                },
                {
                    "id": "safety_03",
                    "question": "위험물(화학물질, 인화물)은 안전하게 보관되고 있나요?",
                    "type": "select",
                    "options": ["안전 보관", "일부 미흡", "해당 없음"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["위험물관리", "화학물질", "안전보관"]
                },
                {
                    "id": "safety_04",
                    "question": "CCTV·경보 시스템은 정상 작동하나요?",
                    "type": "select",
                    "options": ["정상", "일부 고장", "없음"],
                    "importance": "medium",
                    "required": False,
                    "research_keywords": ["CCTV", "경보시스템", "감시장비"]
                }
            ],
            "emergency_response": [
                {
                    "id": "emerg_01",
                    "question": "비상연락망(24시간 대응)이 구축되어 있나요?",
                    "type": "select",
                    "options": ["구축 완료", "구축 중", "미구축"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["비상연락망", "긴급연락", "24시간대응"]
                },
                {
                    "id": "emerg_02",
                    "question": "재난 대응 조직 및 역할 분담이 명확한가요?",
                    "type": "select",
                    "options": ["명확함", "일부 불명확", "불명확"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["재난조직", "역할분담", "지휘체계"]
                },
                {
                    "id": "emerg_03",
                    "question": "재난 상황을 실시간 모니터링할 수 있나요?",
                    "type": "select",
                    "options": ["가능", "부분 가능", "불가능"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["실시간모니터링", "재난감지", "상황파악"]
                },
                {
                    "id": "emerg_04",
                    "question": "외부 지원 요청 절차가 마련되어 있나요? (119, 112, 지자체)",
                    "type": "select",
                    "options": ["마련됨", "검토 중", "미마련"],
                    "importance": "medium",
                    "required": False,
                    "research_keywords": ["외부지원", "구조요청", "협력절차"]
                }
            ],
            "legal_compliance": [
                {
                    "id": "legal_01",
                    "question": "관련 안전 법규는 준수하고 있나요? (재난안전법, 소방법 등)",
                    "type": "select",
                    "options": ["준수", "일부 미흡", "미준수", "모름"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["재난안전법", "소방법", "안전법규"]
                },
                {
                    "id": "legal_02",
                    "question": "필요한 안전 인증을 취득했나요? (소방, 가스, 전기)",
                    "type": "select",
                    "options": ["취득 완료", "진행 중", "미취득", "해당 없음"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["안전인증", "소방인증", "법정인증"]
                },
                {
                    "id": "legal_03",
                    "question": "정기 안전 보고는 제출하고 있나요?",
                    "type": "select",
                    "options": ["정기 제출", "미제출", "해당 없음"],
                    "importance": "medium",
                    "required": False,
                    "research_keywords": ["안전보고", "정기보고", "법정보고"]
                }
            ],
            "organization": [
                {
                    "id": "org_01",
                    "question": "전담 안전관리자가 지정되어 있나요?",
                    "type": "select",
                    "options": ["지정됨", "겸직", "미지정"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["안전관리자", "안전담당", "책임자"]
                },
                {
                    "id": "org_02",
                    "question": "안전 관련 예산은 확보되어 있나요?",
                    "type": "select",
                    "options": ["충분", "부족", "없음"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["안전예산", "재난예산", "투자"]
                },
                {
                    "id": "org_03",
                    "question": "재난 대응 매뉴얼이 작성되어 있나요?",
                    "type": "select",
                    "options": ["작성 완료", "작성 중", "미작성"],
                    "importance": "medium",
                    "required": False,
                    "research_keywords": ["대응매뉴얼", "행동요령", "절차서"]
                }
            ],
            "monitoring": [
                {
                    "id": "mon_01",
                    "question": "점검 이력을 체계적으로 관리하고 있나요?",
                    "type": "select",
                    "options": ["관리 중", "부분 관리", "미관리"],
                    "importance": "medium",
                    "required": True,
                    "research_keywords": ["점검이력", "기록관리", "이력추적"]
                },
                {
                    "id": "mon_02",
                    "question": "발견된 문제점에 대한 사후 조치는 이루어지고 있나요?",
                    "type": "select",
                    "options": ["즉시 조치", "지연 조치", "미조치"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["사후조치", "개선조치", "후속관리"]
                },
                {
                    "id": "mon_03",
                    "question": "정기적인 안전 개선 활동을 하고 있나요?",
                    "type": "select",
                    "options": ["정기 실시", "비정기 실시", "미실시"],
                    "importance": "medium",
                    "required": False,
                    "research_keywords": ["개선활동", "지속개선", "안전향상"]
                }
            ],
            "cooperation": [
                {
                    "id": "coop_01",
                    "question": "소방서·경찰서와 협력 체계가 있나요?",
                    "type": "select",
                    "options": ["구축됨", "구축 중", "미구축"],
                    "importance": "high",
                    "required": True,
                    "research_keywords": ["소방협력", "경찰협력", "유관기관"]
                },
                {
                    "id": "coop_02",
                    "question": "주변 시설과 공동 대응 체계를 갖추고 있나요?",
                    "type": "select",
                    "options": ["구축됨", "논의 중", "미구축"],
                    "importance": "medium",
                    "required": False,
                    "research_keywords": ["공동대응", "지역협력", "상호지원"]
                },
                {
                    "id": "coop_03",
                    "question": "재난 정보를 지역사회와 공유하고 있나요?",
                    "type": "select",
                    "options": ["공유 중", "부분 공유", "미공유"],
                    "importance": "low",
                    "required": False,
                    "research_keywords": ["정보공유", "지역공유", "재난정보"]
                }
            ]
        }

    def get_template_by_type_and_stage(
        self,
        facility_type: str,
        check_phase: str,
        focus_area: str = None
    ) -> Dict[str, Any]:
        """
        시설 유형과 점검 단계에 맞는 템플릿 반환

        Args:
            facility_type: 시설 유형
            check_phase: 점검 단계
            focus_area: 관심 영역 (선택)

        Returns:
            맞춤형 체크리스트 템플릿
        """
        # 모든 카테고리의 질문을 기본으로 포함
        checklist = {}

        for category_id, questions in self.templates.items():
            category_info = self.categories[category_id]

            # 점검 단계에 따른 필터링
            filtered_questions = self._filter_by_phase(questions, check_phase)

            # 관심 영역에 따른 우선순위 조정
            if focus_area:
                filtered_questions = self._adjust_priority_by_focus(
                    filtered_questions,
                    category_id,
                    focus_area
                )

            checklist[category_id] = {
                "info": category_info,
                "questions": filtered_questions
            }

        return checklist

    def _filter_by_phase(
        self,
        questions: List[Dict[str, Any]],
        phase: str
    ) -> List[Dict[str, Any]]:
        """점검 단계에 따른 질문 필터링"""
        # 점검 단계별로 특정 질문 제외
        if phase == CheckPhase.INITIAL.value:
            # 초기 평가 단계에서는 중요도 높은 질문 위주
            return [q for q in questions if q.get('importance') != 'low']
        elif phase == CheckPhase.ANNUAL.value:
            # 연간 종합 단계에서는 모든 질문 포함
            return questions
        else:
            return questions

    def _adjust_priority_by_focus(
        self,
        questions: List[Dict[str, Any]],
        category_id: str,
        focus_area: str
    ) -> List[Dict[str, Any]]:
        """관심 영역에 따른 우선순위 조정"""
        # 관심 영역과 카테고리 매칭
        focus_category_map = {
            FocusArea.SAFETY.value: ["safety_check", "disaster_prep"],
            FocusArea.LEGAL.value: ["legal_compliance"],
            FocusArea.PREVENTION.value: ["risk_assessment", "monitoring"],
            FocusArea.RESPONSE.value: ["emergency_response", "cooperation"]
        }

        # 해당 관심 영역의 카테고리라면 우선순위 상향
        for focus, categories in focus_category_map.items():
            if focus == focus_area and category_id in categories:
                for question in questions:
                    if question.get('importance') == 'medium':
                        question['importance'] = 'high'

        return questions

    def get_research_keywords(self, category_id: str = None) -> List[str]:
        """카테고리별 리서치 키워드 추출"""
        keywords = []

        if category_id:
            questions = self.templates.get(category_id, [])
            for q in questions:
                keywords.extend(q.get('research_keywords', []))
        else:
            # 모든 카테고리의 키워드
            for questions in self.templates.values():
                for q in questions:
                    keywords.extend(q.get('research_keywords', []))

        return list(set(keywords))  # 중복 제거
