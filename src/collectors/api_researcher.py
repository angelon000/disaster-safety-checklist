"""
공공 API 리서치 모듈: 공공데이터포털, 국제 오픈데이터 API 정보 수집
"""
import requests
from typing import List, Dict, Any
from datetime import datetime


class APIResearcher:
    """공공/오픈 API 정보 수집기"""

    def __init__(self, public_data_api_key: str = None):
        self.public_data_api_key = public_data_api_key
        self.public_data_portal = "https://www.data.go.kr/data/15000001/openapi.do"

    def search(self, keyword: str, category: str = None) -> List[Dict[str, Any]]:
        """
        키워드 기반 공공/오픈 API 검색

        Args:
            keyword: 검색 키워드
            category: API 카테고리 (문화, 관광, 지역, 인구 등)

        Returns:
            API 정보 리스트
        """
        results = []

        # 한국 공공데이터포털
        results.extend(self._get_korean_public_apis(keyword, category))

        # 국제 오픈데이터
        results.extend(self._get_international_apis(keyword, category))

        # 기타 유용한 무료 API
        results.extend(self._get_popular_free_apis(keyword, category))

        return results

    def _get_korean_public_apis(self, keyword: str, category: str = None) -> List[Dict[str, Any]]:
        """한국 공공데이터포털 API 목록"""
        apis = []

        # 주요 공공데이터 API 카탈로그 (실제로는 공공데이터포털 API로 검색)
        public_apis_catalog = [
            {
                'name': '한국콘텐츠진흥원_콘텐츠산업통계조사',
                'category': '문화',
                'description': '콘텐츠 산업 관련 통계 데이터 제공',
                'provider': 'KOCCA',
                'url': 'https://www.data.go.kr/data/15000001/openapi.do',
                'data_format': 'JSON, XML',
                'usage_policy': '오픈API (키 필요)',
                'commercial_use': True,
                'keywords': ['콘텐츠', '산업', '통계', '문화']
            },
            {
                'name': '문화체육관광부_문화데이터광장_공연전시정보',
                'category': '문화',
                'description': '전국 공연 및 전시 정보 제공',
                'provider': '문화체육관광부',
                'url': 'http://www.culture.go.kr/openapi',
                'data_format': 'JSON, XML',
                'usage_policy': '오픈API (키 필요)',
                'commercial_use': True,
                'keywords': ['공연', '전시', '문화', '이벤트']
            },
            {
                'name': '한국저작권위원회_저작권등록정보',
                'category': 'IP/저작권',
                'description': '저작권 등록 정보 조회',
                'provider': '한국저작권위원회',
                'url': 'https://www.copyright.or.kr/openapi',
                'data_format': 'JSON, XML',
                'usage_policy': '오픈API (키 필요)',
                'commercial_use': True,
                'keywords': ['저작권', 'IP', '등록', '법률']
            },
            {
                'name': '한국관광공사_관광지정보',
                'category': '관광',
                'description': '전국 관광지 정보 제공',
                'provider': '한국관광공사',
                'url': 'http://api.visitkorea.or.kr',
                'data_format': 'JSON, XML',
                'usage_policy': '오픈API (키 필요)',
                'commercial_use': True,
                'keywords': ['관광', '여행', '지역', '명소']
            },
            {
                'name': '통계청_인구총조사',
                'category': '인구/통계',
                'description': '인구 및 가구 통계 데이터',
                'provider': '통계청',
                'url': 'https://kosis.kr/openapi',
                'data_format': 'JSON, XML',
                'usage_policy': '오픈API (키 필요)',
                'commercial_use': True,
                'keywords': ['인구', '통계', '가구', '인구통계']
            }
        ]

        # 키워드 매칭
        keyword_lower = keyword.lower()
        for api in public_apis_catalog:
            # 키워드가 API의 키워드 리스트에 있는지 확인
            if any(kw in keyword_lower for kw in api['keywords']) or \
               keyword_lower in api['name'].lower() or \
               keyword_lower in api['description'].lower():

                apis.append({
                    'name': api['name'],
                    'category': api['category'],
                    'description': api['description'],
                    'provider': api['provider'],
                    'url': api['url'],
                    'data_format': api['data_format'],
                    'usage_policy': api['usage_policy'],
                    'commercial_use': api['commercial_use'],
                    'api_key_required': True,
                    'cost': 'Free',
                    'source': '공공데이터포털',
                    'relevance_score': self._calculate_relevance(api, keyword)
                })

        return apis

    def _get_international_apis(self, keyword: str, category: str = None) -> List[Dict[str, Any]]:
        """국제 오픈데이터 API 목록"""
        apis = []

        international_apis = [
            {
                'name': 'World Bank Open Data API',
                'category': '경제/통계',
                'description': '세계 각국의 경제, 인구, 개발 지표 데이터',
                'provider': 'World Bank',
                'url': 'https://data.worldbank.org/developers',
                'data_format': 'JSON, XML',
                'usage_policy': 'Open Data (무료)',
                'commercial_use': True,
                'keywords': ['경제', '통계', '국제', '인구', 'GDP']
            },
            {
                'name': 'UN Data API',
                'category': '국제통계',
                'description': 'UN 통계 데이터베이스',
                'provider': 'United Nations',
                'url': 'https://data.un.org',
                'data_format': 'JSON, CSV',
                'usage_policy': 'Open Data (무료)',
                'commercial_use': True,
                'keywords': ['국제', '통계', 'UN', '개발', '사회']
            },
            {
                'name': 'OECD Data API',
                'category': '경제/통계',
                'description': 'OECD 회원국 경제 및 사회 지표',
                'provider': 'OECD',
                'url': 'https://data.oecd.org/api',
                'data_format': 'JSON, XML',
                'usage_policy': 'Open Data (무료)',
                'commercial_use': True,
                'keywords': ['경제', 'OECD', '통계', '정책']
            }
        ]

        keyword_lower = keyword.lower()
        for api in international_apis:
            if any(kw in keyword_lower for kw in api['keywords']):
                apis.append({
                    'name': api['name'],
                    'category': api['category'],
                    'description': api['description'],
                    'provider': api['provider'],
                    'url': api['url'],
                    'data_format': api['data_format'],
                    'usage_policy': api['usage_policy'],
                    'commercial_use': api['commercial_use'],
                    'api_key_required': False,
                    'cost': 'Free',
                    'source': 'International Open Data',
                    'relevance_score': self._calculate_relevance(api, keyword)
                })

        return apis

    def _get_popular_free_apis(self, keyword: str, category: str = None) -> List[Dict[str, Any]]:
        """기타 유용한 무료 API"""
        apis = []

        popular_apis = [
            {
                'name': 'YouTube Data API',
                'category': '미디어',
                'description': 'YouTube 동영상, 채널, 재생목록 데이터',
                'provider': 'Google',
                'url': 'https://developers.google.com/youtube/v3',
                'data_format': 'JSON',
                'usage_policy': '무료 할당량 (키 필요)',
                'commercial_use': True,
                'keywords': ['동영상', '미디어', 'youtube', '콘텐츠', '비디오']
            },
            {
                'name': 'Twitter API',
                'category': 'SNS',
                'description': '트위터 트윗, 사용자, 트렌드 데이터',
                'provider': 'Twitter (X)',
                'url': 'https://developer.twitter.com/en/docs',
                'data_format': 'JSON',
                'usage_policy': '무료/유료 플랜',
                'commercial_use': True,
                'keywords': ['SNS', 'twitter', '소셜미디어', '트렌드']
            },
            {
                'name': 'News API',
                'category': '뉴스',
                'description': '전세계 뉴스 헤드라인 및 기사',
                'provider': 'NewsAPI.org',
                'url': 'https://newsapi.org',
                'data_format': 'JSON',
                'usage_policy': '무료 플랜 (키 필요)',
                'commercial_use': False,  # 무료 플랜은 비상업용
                'keywords': ['뉴스', '기사', '언론', '미디어']
            },
            {
                'name': 'OpenWeatherMap API',
                'category': '날씨',
                'description': '현재 날씨 및 예보 데이터',
                'provider': 'OpenWeatherMap',
                'url': 'https://openweathermap.org/api',
                'data_format': 'JSON, XML',
                'usage_policy': '무료 플랜 (키 필요)',
                'commercial_use': True,
                'keywords': ['날씨', '기상', '예보']
            }
        ]

        keyword_lower = keyword.lower()
        for api in popular_apis:
            if any(kw in keyword_lower for kw in api['keywords']):
                apis.append({
                    'name': api['name'],
                    'category': api['category'],
                    'description': api['description'],
                    'provider': api['provider'],
                    'url': api['url'],
                    'data_format': api['data_format'],
                    'usage_policy': api['usage_policy'],
                    'commercial_use': api['commercial_use'],
                    'api_key_required': True,
                    'cost': 'Free (with limits)',
                    'source': 'Third-party API',
                    'relevance_score': self._calculate_relevance(api, keyword)
                })

        return apis

    def _calculate_relevance(self, api: Dict[str, Any], keyword: str) -> float:
        """API 관련성 점수 계산"""
        score = 0.0
        keyword_lower = keyword.lower()

        # 이름에 키워드 포함
        if keyword_lower in api['name'].lower():
            score += 0.4

        # 설명에 키워드 포함
        if keyword_lower in api['description'].lower():
            score += 0.3

        # 키워드 리스트에 포함
        if any(kw in keyword_lower for kw in api.get('keywords', [])):
            score += 0.3

        return min(score, 1.0)

    def get_api_examples(self, api_name: str) -> Dict[str, Any]:
        """
        특정 API의 사용 예시 코드 제공

        Args:
            api_name: API 이름

        Returns:
            예시 코드 및 설명
        """
        examples = {
            'YouTube Data API': {
                'description': 'YouTube 동영상 검색 예시',
                'code': '''
import requests

api_key = 'YOUR_API_KEY'
url = 'https://www.googleapis.com/youtube/v3/search'

params = {
    'part': 'snippet',
    'q': 'K-POP',
    'key': api_key,
    'maxResults': 10
}

response = requests.get(url, params=params)
data = response.json()
                ''',
                'documentation': 'https://developers.google.com/youtube/v3/docs'
            }
        }

        return examples.get(api_name, {
            'description': '예시 코드가 준비되지 않았습니다.',
            'code': '',
            'documentation': ''
        })
