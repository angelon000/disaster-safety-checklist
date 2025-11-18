"""
웹 리서치 모듈: 뉴스, 블로그, 공공기관 자료 수집
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import time
from urllib.parse import quote_plus


class WebResearcher:
    """웹 기반 리서치 수집기"""

    def __init__(self, max_results: int = 10, timeout: int = 10):
        self.max_results = max_results
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def search(self, keyword: str, sources: List[str] = None) -> List[Dict[str, Any]]:
        """
        키워드 기반 웹 검색

        Args:
            keyword: 검색 키워드
            sources: 특정 출처 리스트 (None이면 모든 출처)

        Returns:
            검색 결과 리스트
        """
        results = []

        # 한국 정부/공공기관 사이트
        if sources is None or 'government' in sources:
            results.extend(self._search_government_sites(keyword))

        # 산업/시장 리포트
        if sources is None or 'industry' in sources:
            results.extend(self._search_industry_reports(keyword))

        # 기술 블로그 및 커뮤니티
        if sources is None or 'community' in sources:
            results.extend(self._search_tech_blogs(keyword))

        # 결과 정렬 (최신순)
        results.sort(key=lambda x: x.get('published_date', ''), reverse=True)

        return results[:self.max_results]

    def _search_government_sites(self, keyword: str) -> List[Dict[str, Any]]:
        """정부/공공기관 사이트 검색"""
        results = []

        # 주요 정부 사이트 목록
        government_sites = [
            {
                'name': '문화체육관광부',
                'url': 'https://www.mcst.go.kr',
                'search_path': '/kor/s_notice/notice/noticeList.jsp'
            },
            {
                'name': 'KOCCA (한국콘텐츠진흥원)',
                'url': 'https://www.kocca.kr',
                'search_path': '/cop/bbs/list/B0000146.do'
            },
            {
                'name': 'KISA (한국인터넷진흥원)',
                'url': 'https://www.kisa.or.kr',
                'search_path': '/2060204'
            }
        ]

        for site in government_sites:
            try:
                # 실제 크롤링 대신 메타데이터만 반환 (예시)
                # 실제 구현에서는 각 사이트의 검색 API나 크롤링 로직 필요
                results.append({
                    'title': f'{site["name"]} - {keyword} 관련 자료',
                    'url': f'{site["url"]}{site["search_path"]}',
                    'source': site['name'],
                    'source_type': 'government',
                    'summary': f'{site["name"]}에서 {keyword}와 관련된 공지사항 및 자료',
                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                    'credibility_score': 0.95  # 정부 사이트는 높은 신뢰도
                })
            except Exception as e:
                print(f"Error searching {site['name']}: {e}")
                continue

        return results

    def _search_industry_reports(self, keyword: str) -> List[Dict[str, Any]]:
        """산업/시장 리포트 검색"""
        results = []

        # 주요 산업 리포트 사이트
        industry_sites = [
            {
                'name': 'KISDI (정보통신정책연구원)',
                'url': 'https://www.kisdi.re.kr',
                'type': 'research'
            },
            {
                'name': '통계청',
                'url': 'https://kostat.go.kr',
                'type': 'statistics'
            }
        ]

        for site in industry_sites:
            try:
                results.append({
                    'title': f'{keyword} 관련 {site["name"]} 보고서',
                    'url': site['url'],
                    'source': site['name'],
                    'source_type': 'industry',
                    'summary': f'{keyword}에 대한 산업 동향 및 시장 분석',
                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                    'credibility_score': 0.85
                })
            except Exception as e:
                print(f"Error searching {site['name']}: {e}")
                continue

        return results

    def _search_tech_blogs(self, keyword: str) -> List[Dict[str, Any]]:
        """기술 블로그 및 커뮤니티 검색"""
        results = []

        # 주요 기술 블로그 플랫폼
        blog_platforms = [
            {'name': '브런치', 'url': 'https://brunch.co.kr'},
            {'name': '미디엄', 'url': 'https://medium.com'},
            {'name': 'GeekNews', 'url': 'https://news.hada.io'}
        ]

        for platform in blog_platforms:
            try:
                results.append({
                    'title': f'{keyword} - {platform["name"]} 기술 블로그',
                    'url': platform['url'],
                    'source': platform['name'],
                    'source_type': 'community',
                    'summary': f'{keyword}에 대한 기술 블로그 및 커뮤니티 글',
                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                    'credibility_score': 0.70
                })
            except Exception as e:
                print(f"Error searching {platform['name']}: {e}")
                continue

        return results

    def fetch_content(self, url: str) -> Dict[str, Any]:
        """URL에서 실제 콘텐츠 가져오기"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # 제목 추출
            title = soup.find('title')
            title_text = title.get_text() if title else ''

            # 본문 추출 (간단한 예시)
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs[:5]])

            return {
                'title': title_text,
                'content': content[:500],  # 처음 500자
                'url': url,
                'fetched_at': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'error': str(e),
                'url': url
            }
