"""
논문 리서치 모듈: Semantic Scholar, CrossRef, arXiv API를 통한 논문 검색
"""
import requests
from typing import List, Dict, Any
from datetime import datetime
import time
from urllib.parse import quote_plus


class PaperResearcher:
    """학술 논문 검색 및 수집기"""

    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        self.semantic_scholar_api = "https://api.semanticscholar.org/graph/v1"
        self.crossref_api = "https://api.crossref.org/works"
        self.arxiv_api = "http://export.arxiv.org/api/query"

    def search(self, keyword: str, sources: List[str] = None) -> List[Dict[str, Any]]:
        """
        키워드 기반 논문 검색

        Args:
            keyword: 검색 키워드
            sources: 검색할 소스 리스트 (None이면 모든 소스)

        Returns:
            논문 결과 리스트
        """
        results = []

        if sources is None or 'semantic_scholar' in sources:
            results.extend(self._search_semantic_scholar(keyword))

        if sources is None or 'crossref' in sources:
            results.extend(self._search_crossref(keyword))

        if sources is None or 'arxiv' in sources:
            results.extend(self._search_arxiv(keyword))

        # 연도 기준 정렬 (최신순)
        results.sort(key=lambda x: x.get('year', 0), reverse=True)

        return results[:self.max_results]

    def _search_semantic_scholar(self, keyword: str) -> List[Dict[str, Any]]:
        """Semantic Scholar API를 통한 논문 검색"""
        results = []

        try:
            url = f"{self.semantic_scholar_api}/paper/search"
            params = {
                'query': keyword,
                'limit': min(self.max_results, 10),
                'fields': 'title,authors,year,abstract,citationCount,venue,url'
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                for paper in data.get('data', []):
                    authors = [author.get('name', '') for author in paper.get('authors', [])]

                    results.append({
                        'title': paper.get('title', ''),
                        'authors': authors,
                        'year': paper.get('year'),
                        'abstract': paper.get('abstract', '')[:500],  # 처음 500자
                        'citations': paper.get('citationCount', 0),
                        'venue': paper.get('venue', ''),
                        'url': paper.get('url', ''),
                        'source': 'Semantic Scholar',
                        'relevance_score': self._calculate_relevance(paper, keyword)
                    })

            time.sleep(0.5)  # API Rate limit 고려

        except Exception as e:
            print(f"Error searching Semantic Scholar: {e}")

        return results

    def _search_crossref(self, keyword: str) -> List[Dict[str, Any]]:
        """CrossRef API를 통한 논문 검색"""
        results = []

        try:
            params = {
                'query': keyword,
                'rows': min(self.max_results, 10),
                'sort': 'relevance',
                'order': 'desc'
            }

            response = requests.get(self.crossref_api, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                for item in data.get('message', {}).get('items', []):
                    # 저자 정보 추출
                    authors = []
                    for author in item.get('author', []):
                        name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                        if name:
                            authors.append(name)

                    # 발행 연도 추출
                    year = None
                    pub_date = item.get('published-print') or item.get('published-online')
                    if pub_date and 'date-parts' in pub_date:
                        date_parts = pub_date['date-parts'][0]
                        if date_parts:
                            year = date_parts[0]

                    results.append({
                        'title': item.get('title', [''])[0],
                        'authors': authors,
                        'year': year,
                        'abstract': item.get('abstract', '')[:500],
                        'citations': item.get('is-referenced-by-count', 0),
                        'venue': item.get('container-title', [''])[0],
                        'url': item.get('URL', ''),
                        'doi': item.get('DOI', ''),
                        'source': 'CrossRef',
                        'relevance_score': 0.8
                    })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error searching CrossRef: {e}")

        return results

    def _search_arxiv(self, keyword: str) -> List[Dict[str, Any]]:
        """arXiv API를 통한 논문 검색"""
        results = []

        try:
            params = {
                'search_query': f'all:{keyword}',
                'start': 0,
                'max_results': min(self.max_results, 10),
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }

            response = requests.get(self.arxiv_api, params=params, timeout=10)

            if response.status_code == 200:
                # arXiv는 XML 응답을 반환
                import xml.etree.ElementTree as ET

                root = ET.fromstring(response.content)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}

                for entry in root.findall('atom:entry', ns):
                    title = entry.find('atom:title', ns)
                    title_text = title.text.strip() if title is not None else ''

                    # 저자 추출
                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name = author.find('atom:name', ns)
                        if name is not None:
                            authors.append(name.text)

                    # 발행 날짜
                    published = entry.find('atom:published', ns)
                    year = None
                    if published is not None:
                        year = int(published.text[:4])

                    # 초록
                    summary = entry.find('atom:summary', ns)
                    abstract = summary.text[:500] if summary is not None else ''

                    # URL
                    link = entry.find('atom:id', ns)
                    url = link.text if link is not None else ''

                    results.append({
                        'title': title_text,
                        'authors': authors,
                        'year': year,
                        'abstract': abstract,
                        'citations': 0,  # arXiv는 citation 정보 제공 안함
                        'venue': 'arXiv',
                        'url': url,
                        'source': 'arXiv',
                        'relevance_score': 0.75
                    })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error searching arXiv: {e}")

        return results

    def _calculate_relevance(self, paper: Dict[str, Any], keyword: str) -> float:
        """논문 관련성 점수 계산"""
        score = 0.0

        # 제목에 키워드 포함
        title = paper.get('title', '').lower()
        if keyword.lower() in title:
            score += 0.5

        # 초록에 키워드 포함
        abstract = paper.get('abstract', '').lower()
        if keyword.lower() in abstract:
            score += 0.3

        # 인용 수 반영 (정규화)
        citations = paper.get('citationCount', 0)
        if citations > 100:
            score += 0.2
        elif citations > 10:
            score += 0.1

        return min(score, 1.0)

    def analyze_maturity(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        논문 데이터를 기반으로 기술/시장 성숙도 분석

        Returns:
            성숙도 분석 결과
        """
        if not papers:
            return {
                'maturity_level': 'unknown',
                'total_papers': 0,
                'recent_papers': 0,
                'average_citations': 0
            }

        total_papers = len(papers)
        current_year = datetime.now().year

        # 최근 3년 논문 수
        recent_papers = len([p for p in papers if p.get('year', 0) >= current_year - 3])

        # 평균 인용 수
        total_citations = sum(p.get('citations', 0) for p in papers)
        avg_citations = total_citations / total_papers if total_papers > 0 else 0

        # 성숙도 레벨 판단
        maturity_level = 'emerging'
        if total_papers > 50 and recent_papers > 10:
            maturity_level = 'mature'
        elif total_papers > 20:
            maturity_level = 'growing'

        return {
            'maturity_level': maturity_level,
            'total_papers': total_papers,
            'recent_papers': recent_papers,
            'average_citations': round(avg_citations, 2),
            'year_distribution': self._get_year_distribution(papers)
        }

    def _get_year_distribution(self, papers: List[Dict[str, Any]]) -> Dict[int, int]:
        """연도별 논문 분포"""
        distribution = {}
        for paper in papers:
            year = paper.get('year')
            if year:
                distribution[year] = distribution.get(year, 0) + 1

        return dict(sorted(distribution.items(), reverse=True))
