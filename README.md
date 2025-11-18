# 재난·안전 체크리스트 시스템

> 지자체·건설현장·사업장을 위한 재난·안전 맞춤형 체크리스트 자동 생성 시스템

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/angelon000/disaster-safety-checklist/codespaces/new)

## 🚀 빠른 시작

### ☁️ GitHub Codespaces (가장 빠름!)

**클릭 한 번으로 바로 실행!** 외부 접속 자동 지원 ⚡

[![Open in Codespaces](https://img.shields.io/badge/Open%20in-Codespaces-blue?logo=github)](https://github.com/angelon000/disaster-safety-checklist/codespaces/new)

1. 위 배지 클릭
2. 1분 대기 (자동 설치)
3. 터미널에서 `python dashboard/app.py`
4. 자동 생성된 URL로 접속!

**무료**: 월 60시간 무료 | **HTTPS 자동** | **외부 접속 OK**

자세한 설명: [CODESPACES.md](CODESPACES.md)

---

### ☁️ 무료 클라우드 배포 (24/7 실행)

**Codespaces가 닫히는 게 불편하다면?** 항상 켜져있는 무료 서버!

#### 🎯 Render.com (가장 추천!)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/angelon000/disaster-safety-checklist)

1. 위 버튼 클릭
2. GitHub 계정 연결
3. **Apply** 클릭
4. 5분 대기 → 완료!

**무료**: 월 750시간 | **HTTPS 자동** | **GitHub 자동 배포** | **재시작 없음**

#### 🚂 Railway.app (더 빠른 시작)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/disaster-safety-checklist)

**무료**: 월 $5 크레딧 | 더 빠른 콜드 스타트

#### ⚡ 비교

| 서비스 | 무료 한도 | 콜드 스타트 | 설정 난이도 |
|--------|----------|------------|-----------|
| **Render** | 750h/월 | 30초 | ⭐⭐⭐⭐⭐ 매우 쉬움 |
| **Railway** | $5/월 | 10초 | ⭐⭐⭐⭐⭐ 매우 쉬움 |
| **Codespaces** | 60h/월 | 즉시 | ⭐⭐⭐⭐ 쉬움 |

📘 자세한 배포 가이드: [RENDER_DEPLOY.md](RENDER_DEPLOY.md)

---

### 웹 대시보드 (로컬 실행)

#### Windows
```bash
# 간편 실행 (의존성 자동 설치)
run_server.bat
```

#### Linux/macOS
```bash
# 간편 실행 (의존성 자동 설치)
./run_server.sh
```

#### 수동 실행
```bash
# 의존성 설치
pip install -r requirements.txt

# 대시보드 실행
python dashboard/app.py
```

브라우저에서 접속:
- 🌐 로컬: `http://localhost:8000`
- 🌍 네트워크: `http://[서버IP]:8000` (같은 Wi-Fi 내 다른 기기)

### CLI 인터페이스
```bash
# 간단한 체크리스트 생성
python src/main.py generate "○○시 지자체 재난안전" --type "지자체" --stage "초기 평가"
```

### 외부 배포
인터넷을 통한 외부 접속 설정은 [DEPLOYMENT.md](DEPLOYMENT.md)를 참고하세요.

## 목표

지자체, 건설현장, 사업장, 공공시설을 대상으로 **시설 유형·점검 단계별 맞춤형 재난·안전 체크리스트**를 자동 생성하고, 각 항목마다 참고할 **웹자료·논문·기술·공공 API 근거**를 제공합니다.

## 주요 기능

### 1. 8가지 카테고리 체크리스트
- ⚠️ **위험도 평가**: 과거 재난 이력, 지리적 위험, 취약성 분석
- 🛡️ **재난 대비**: 대피 계획, 비상 물품, 교육·훈련, 소화 설비
- 🔍 **안전 점검**: 시설물 점검, 전기·가스 설비, 위험물 관리, CCTV·경보
- 🚨 **비상 대응**: 비상연락망, 대응 조직, 실시간 모니터링, 외부 지원
- 📋 **법규·인증**: 안전 법규 준수, 필요 인증, 정기 보고
- 👥 **조직·책임**: 안전관리자 지정, 예산 확보, 대응 매뉴얼
- 📊 **모니터링·개선**: 점검 이력 관리, 사후 조치, 개선 활동
- 🤝 **지역 협력**: 소방·경찰 협력, 지역 공동 대응, 정보 공유

**총 28개 질문** (카테고리당 평균 3.5개)

### 2. 4가지 데이터 수집 모듈 (v1.0: 카탈로그 수준)
- 🌐 **웹 리서치**: 행정안전부, 지자체 공지사항, 재난 뉴스 (v1.0: 더미 데이터)
- 📄 **논문 리서치**: Semantic Scholar, CrossRef, arXiv API (v1.0: 샘플 카탈로그)
- 💻 **기술 트렌드**: GitHub API, PyPI, npm (v1.0: 예시 데이터)
- 🔌 **공공 API**: 재난안전데이터공유플랫폼, 안전한국 (v1.0: API 목록 추천)

### 3. 맞춤형 체크리스트 생성
- **시설 유형별** (9가지): 지자체, 건설현장, 제조사업장, 물류창고, 상업시설, 교육시설, 의료시설, 주거시설, 기타
- **점검 단계별** (5가지): 초기 평가, 정기 점검, 재난 발생 시, 복구 후, 연간 종합
- **관심 영역별** (4가지): 안전 중심, 법규 중심, 예방 중심, 대응 중심

## 설치

### 요구사항
- Python 3.9 이상

### 의존성 설치
```bash
pip install -r requirements.txt
```

## 사용 방법

### 🌐 웹 대시보드 (권장)

#### 실행
```bash
python run_dashboard.py
```

브라우저가 자동으로 열립니다: `http://localhost:8000`

#### 주요 화면
1. **홈**: 체크리스트 생성 폼 + 통계 대시보드
2. **결과**: 생성된 체크리스트 미리보기 + 파일 다운로드
3. **프로젝트 목록**: 과거 체크리스트 관리

**자세한 내용**: [DASHBOARD.md](DASHBOARD.md)

### 💻 CLI 인터페이스

#### 1. 체크리스트 생성

##### 기본 사용 (데이터 수집 없음)
```bash
python src/main.py generate "○○시 지자체" --type "지자체" --stage "초기 평가"
```

##### 데이터 수집 포함 체크리스트 생성
```bash
python src/main.py generate "△△ 건설현장" --type "건설현장" --stage "정기 점검" --collect
```

##### JSON 형식으로 출력
```bash
python src/main.py generate "□□ 제조사업장" --type "제조사업장" --stage "연간 종합" --format json
```

##### Markdown + JSON 둘 다 출력
```bash
python src/main.py generate "◇◇ 의료시설" --type "의료시설" --stage "재난 발생 시" --format both --collect
```

##### 관심 영역 지정
```bash
python src/main.py generate "▽▽ 상업시설" \
  --type "상업시설" \
  --stage "정기 점검" \
  --focus "법규 중심" \
  --collect
```

#### 2. 템플릿 및 옵션 확인

##### 전체 카테고리 목록 보기
```bash
python src/main.py list
```

##### 특정 카테고리 상세 보기
```bash
python src/main.py list --category risk_assessment
```

#### 3. 설정 관리

##### 현재 설정 보기
```bash
python src/main.py config --show
```

##### API 키 설정
```bash
python src/main.py config --set api_keys.github YOUR_GITHUB_TOKEN
```

## 프로젝트 구조

```
kcl/
├── src/
│   ├── collectors/          # 데이터 수집 모듈
│   │   ├── web_researcher.py      # 웹 리서치
│   │   ├── paper_researcher.py    # 논문 리서치
│   │   ├── tech_researcher.py     # 기술 트렌드
│   │   └── api_researcher.py      # 공공 API
│   ├── checklist/           # 체크리스트 관리
│   │   ├── templates.py           # 템플릿 정의 (8카테고리, 28질문)
│   │   └── generator.py           # 생성 엔진
│   ├── utils/               # 유틸리티
│   │   └── config.py              # 설정 관리
│   └── main.py              # CLI 인터페이스
├── dashboard/               # 웹 대시보드 (FastAPI)
│   ├── app.py                      # FastAPI 앱 메인
│   ├── database.py                 # SQLite 데이터베이스
│   └── templates/                  # Jinja2 템플릿
│       ├── base.html
│       ├── index.html
│       ├── list.html
│       └── result.html
├── config/
│   └── settings.json        # 설정 파일
├── data/                    # 수집 데이터 저장 + SQLite DB
│   └── projects.db                 # 프로젝트 관리 DB
├── output/                  # 생성된 체크리스트 출력
├── plan.md                  # 프로젝트 계획서 (v1.0/v2.0 로드맵)
├── requirements.txt         # 의존성
├── run_dashboard.py         # 대시보드 실행 스크립트
└── README.md               # 문서
```

## 설정 파일 (config/settings.json)

첫 실행 시 자동으로 생성됩니다. 필요에 따라 수정하세요.

```json
{
  "api_keys": {
    "github": "",
    "public_data": ""
  },
  "max_results_per_source": 10,
  "web_search": {
    "enabled": true,
    "max_pages": 5
  },
  "paper_search": {
    "enabled": true,
    "sources": ["semantic_scholar", "crossref", "arxiv"]
  }
}
```

### API 키 설정 (선택사항)

#### GitHub API
더 많은 요청을 위해 GitHub Personal Access Token 설정:
1. GitHub Settings → Developer settings → Personal access tokens
2. 토큰 생성 (public_repo 권한)
3. 환경변수 설정: `GITHUB_TOKEN=your_token`
   또는 설정 파일에 직접 입력

#### 공공데이터포털 API
재난안전데이터 활용 시:
1. [재난안전데이터공유플랫폼](https://www.safetydata.go.kr) 또는 [공공데이터포털](https://www.data.go.kr) 회원가입
2. 원하는 API 신청 (재난 이력, 위험 정보 등)
3. 발급받은 키를 `PUBLIC_DATA_API_KEY` 환경변수로 설정

## 출력 예시

### Markdown 출력 (output/checklist_*.md)
```markdown
# ○○시 지자체 - 재난·안전 체크리스트

**시설 유형**: 지자체
**점검 단계**: 초기 평가
**생성일시**: 2025-11-18T14:30:00

---

## 📊 리서치 요약
- 웹 자료: 10건
- 논문: 8건
- 기술 프로젝트: 5건
- API: 3건

## 💡 추천 사항
✅ 충분한 연구 자료가 있어 검증된 안전 기준을 참고할 수 있습니다.
💡 3개의 공공 API를 활용하여 실시간 재난 정보를 모니터링할 수 있습니다.

---

## ⚠️ 위험도 평가

### 1. 최근 5년간 발생한 주요 재난은 무엇인가요? (화재, 침수, 지진 등) 🔴
**답변:**
```

```

**참고 자료:**
- [재난이력 통계](https://www.safetydata.go.kr) - 재난안전데이터공유플랫폼
- 📄 [과거 사례분석을 통한 재난 의사결정 체크리스트 구성](https://www.kci.go.kr/...) (2023)

...
```

## 활용 시나리오

### 시나리오 1: 지자체 재난안전 점검
```bash
python src/main.py generate "○○시 지자체 재난안전" \
  --type "지자체" \
  --stage "초기 평가" \
  --focus "법규 준수" \
  --collect \
  --format both
```

**결과**: 법규 준수에 초점을 맞춘 체크리스트 + 재난안전법·소방법 관련 자료

### 시나리오 2: 건설현장 정기 점검
```bash
python src/main.py generate "△△ 건설현장" \
  --type "건설현장" \
  --stage "정기 점검" \
  --focus "안전 중심" \
  --collect
```

**결과**: 안전 점검 중심 체크리스트 + 건설 안전 기술·논문 자료

### 시나리오 3: 의료시설 재난 대응
```bash
python src/main.py generate "◇◇ 의료시설" \
  --type "의료시설" \
  --stage "재난 발생 시" \
  --focus "대응 중심" \
  --collect
```

**결과**: 비상 대응 중심 체크리스트 + 의료시설 재난 대응 매뉴얼·사례

## 현재 구현 상태 (v1.0)

### ✅ 구현 완료
- 8개 카테고리, 28개 질문 템플릿 기반 체크리스트 자동 생성
- 9개 시설 유형, 5개 점검 단계 지원
- CLI 도구 (`generate`, `list`, `config`)
- 웹 대시보드 (FastAPI + Jinja2 + Bootstrap 5 + Chart.js)
- SQLite 기반 프로젝트 관리
- Markdown/JSON 형식 출력

### 🔄 부분 구현 (카탈로그/더미 데이터 수준)
- 웹·논문·기술·API 리서치 (더미 데이터 제공)
- 목적: UI/UX 테스트 및 데이터 구조 검증

### ⏳ 미구현 (v2.0 계획)
- 실제 웹 크롤링 및 RSS 피드 연동
- Semantic Scholar/arXiv 등 논문 API 실제 연동
- GitHub API 실제 호출 및 분석
- 재난안전데이터공유플랫폼 API 실제 연동
- 시설 유형별 차별화된 질문 세트
- AI 기반 위험도 분석 및 우선순위 산정
- 실시간 알림 및 점검 일정 관리
- 사용자 인증 및 권한 관리

**자세한 로드맵**: [plan.md](plan.md)

## 기술 스택

### v1.0 구현
- **언어**: Python 3.9+
- **웹 프레임워크**: FastAPI 0.104.1, Uvicorn
- **템플릿**: Jinja2 3.1.2
- **데이터베이스**: SQLite
- **프론트엔드**: Bootstrap 5, Chart.js
- **CLI**: argparse

### v2.0 추가 예정
- PostgreSQL (데이터베이스)
- Celery + Redis (비동기 작업)
- BeautifulSoup4/Scrapy (웹 크롤링)
- Semantic Scholar API, arXiv API (논문)
- PyGithub (GitHub API)
- LLM API (GPT-4/Claude) - 요약 및 분석

## 문서

- [plan.md](plan.md) - 프로젝트 계획서 (v1.0/v2.0 로드맵)
- [DASHBOARD.md](DASHBOARD.md) - 웹 대시보드 사용 가이드
- [plan_content_archived.md](plan_content_archived.md) - 과거 콘텐츠 도메인 설계 (아카이브)

## 라이선스

이 프로젝트는 재난·안전 관리 목적으로 개발되었습니다.

---

**Generated by 재난·안전 체크리스트 시스템 v1.0**
