"""
기술 트렌드 모듈: GitHub API, 패키지 레지스트리, Product Hunt 등
"""
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta
import time


class TechResearcher:
    """기술 트렌드 및 오픈소스 수집기"""

    def __init__(self, github_token: str = None, max_results: int = 10, min_stars: int = 10):
        self.github_token = github_token
        self.max_results = max_results
        self.min_stars = min_stars
        self.github_api = "https://api.github.com"

        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'

    def search(self, keyword: str, sources: List[str] = None) -> List[Dict[str, Any]]:
        """
        키워드 기반 기술 트렌드 검색

        Args:
            keyword: 검색 키워드
            sources: 검색할 소스 리스트

        Returns:
            기술 정보 리스트
        """
        results = []

        if sources is None or 'github' in sources:
            results.extend(self._search_github(keyword))

        if sources is None or 'npm' in sources:
            results.extend(self._search_npm(keyword))

        if sources is None or 'pypi' in sources:
            results.extend(self._search_pypi(keyword))

        # 인기도 기준 정렬
        results.sort(key=lambda x: x.get('popularity_score', 0), reverse=True)

        return results[:self.max_results]

    def _search_github(self, keyword: str) -> List[Dict[str, Any]]:
        """GitHub 레포지토리 검색"""
        results = []

        try:
            url = f"{self.github_api}/search/repositories"
            params = {
                'q': f'{keyword} stars:>={self.min_stars}',
                'sort': 'stars',
                'order': 'desc',
                'per_page': min(self.max_results, 30)
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                for repo in data.get('items', []):
                    # 최근 업데이트 날짜
                    updated_at = datetime.strptime(
                        repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ'
                    )

                    # 활성도 계산
                    days_since_update = (datetime.now() - updated_at).days
                    is_active = days_since_update < 180  # 6개월 이내 업데이트

                    # 인기도 점수 계산
                    popularity_score = self._calculate_github_popularity(repo)

                    # 주요 언어
                    language = repo.get('language', 'Unknown')

                    # 토픽/태그
                    topics = repo.get('topics', [])

                    results.append({
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'description': repo.get('description', ''),
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'forks': repo['forks_count'],
                        'watchers': repo['watchers_count'],
                        'open_issues': repo['open_issues_count'],
                        'language': language,
                        'topics': topics,
                        'created_at': repo['created_at'],
                        'updated_at': repo['updated_at'],
                        'is_active': is_active,
                        'license': repo.get('license', {}).get('name', 'No License'),
                        'popularity_score': popularity_score,
                        'source': 'GitHub',
                        'type': 'repository'
                    })

            # GitHub API Rate limit 확인
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                if remaining < 10:
                    print(f"Warning: GitHub API rate limit low ({remaining} remaining)")

            time.sleep(1)  # Rate limit 고려

        except Exception as e:
            print(f"Error searching GitHub: {e}")

        return results

    def _search_npm(self, keyword: str) -> List[Dict[str, Any]]:
        """npm 패키지 검색"""
        results = []

        try:
            url = "https://registry.npmjs.org/-/v1/search"
            params = {
                'text': keyword,
                'size': min(self.max_results, 20)
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                for pkg in data.get('objects', []):
                    package = pkg.get('package', {})

                    # 인기도 점수
                    score = pkg.get('score', {})
                    popularity = score.get('detail', {}).get('popularity', 0)

                    results.append({
                        'name': package.get('name', ''),
                        'description': package.get('description', ''),
                        'version': package.get('version', ''),
                        'url': package.get('links', {}).get('npm', ''),
                        'repository': package.get('links', {}).get('repository', ''),
                        'author': package.get('author', {}).get('name', ''),
                        'keywords': package.get('keywords', []),
                        'popularity_score': popularity,
                        'source': 'npm',
                        'type': 'package'
                    })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error searching npm: {e}")

        return results

    def _search_pypi(self, keyword: str) -> List[Dict[str, Any]]:
        """PyPI 패키지 검색"""
        results = []

        try:
            url = "https://pypi.org/pypi"

            # PyPI 검색 (간단한 예시, 실제로는 더 복잡한 검색 필요)
            search_url = f"https://pypi.org/search/?q={keyword}"

            # 직접 API 대신 주요 패키지만 메타데이터로 제공
            # 실제 구현에서는 BeautifulSoup으로 크롤링하거나 다른 방법 사용

            # 예시 데이터
            popular_packages = [
                {'name': f'{keyword}-related-package', 'description': f'{keyword} 관련 Python 패키지'}
            ]

            for pkg in popular_packages:
                results.append({
                    'name': pkg['name'],
                    'description': pkg['description'],
                    'url': f"https://pypi.org/project/{pkg['name']}/",
                    'popularity_score': 0.5,
                    'source': 'PyPI',
                    'type': 'package'
                })

        except Exception as e:
            print(f"Error searching PyPI: {e}")

        return results

    def _calculate_github_popularity(self, repo: Dict[str, Any]) -> float:
        """GitHub 레포지토리 인기도 점수 계산"""
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        watchers = repo.get('watchers_count', 0)

        # 가중치 적용
        score = (stars * 1.0) + (forks * 2.0) + (watchers * 0.5)

        # 최근 업데이트 보너스
        updated_at = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        days_since_update = (datetime.now() - updated_at).days

        if days_since_update < 30:
            score *= 1.2
        elif days_since_update < 90:
            score *= 1.1

        # 로그 스케일로 정규화 (0-1 범위)
        import math
        normalized_score = min(math.log10(score + 1) / 5.0, 1.0)

        return round(normalized_score, 3)

    def analyze_tech_maturity(self, tech_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        기술 성숙도 분석

        Returns:
            성숙도 분석 결과
        """
        if not tech_items:
            return {
                'maturity_level': 'unknown',
                'total_projects': 0,
                'active_projects': 0,
                'average_stars': 0
            }

        total_projects = len(tech_items)

        # GitHub 프로젝트만 필터링
        github_projects = [item for item in tech_items if item.get('source') == 'GitHub']

        # 활성 프로젝트 (최근 6개월 이내 업데이트)
        active_projects = len([p for p in github_projects if p.get('is_active', False)])

        # 평균 스타 수
        total_stars = sum(p.get('stars', 0) for p in github_projects)
        avg_stars = total_stars / len(github_projects) if github_projects else 0

        # 성숙도 레벨 판단
        maturity_level = 'emerging'
        if total_projects > 20 and avg_stars > 1000:
            maturity_level = 'mature'
        elif total_projects > 10 and avg_stars > 100:
            maturity_level = 'growing'

        # 주요 프로그래밍 언어 분석
        languages = {}
        for project in github_projects:
            lang = project.get('language', 'Unknown')
            languages[lang] = languages.get(lang, 0) + 1

        return {
            'maturity_level': maturity_level,
            'total_projects': total_projects,
            'active_projects': active_projects,
            'average_stars': round(avg_stars, 2),
            'top_languages': dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]),
            'recommended_stacks': self._get_recommended_stacks(github_projects)
        }

    def _get_recommended_stacks(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """추천 기술 스택 추출"""
        stacks = []

        # 상위 3개 프로젝트에서 추천
        for project in projects[:3]:
            stacks.append({
                'name': project.get('name', ''),
                'url': project.get('url', ''),
                'stars': project.get('stars', 0),
                'language': project.get('language', ''),
                'description': project.get('description', '')
            })

        return stacks
