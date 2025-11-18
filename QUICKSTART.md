# 빠른 시작 가이드

## 1. 설치

```bash
# 1. 저장소 클론 (또는 다운로드)
cd d:\dev\kcl

# 2. 의존성 설치
pip install -r requirements.txt
```

## 2. 첫 실행

### 간단한 체크리스트 생성 (데이터 수집 없음)
```bash
python src/main.py generate "K-POP 팬덤 플랫폼" --type "K-POP" --stage "아이디어"
```

**결과**: `output/checklist_K-POP 팬덤 플랫폼_[날짜].md` 파일 생성

### 템플릿 확인
```bash
python src/main.py list
```

## 3. 데이터 수집 포함 실행

```bash
python src/main.py generate "웹툰 플랫폼" \
  --type "웹툰" \
  --stage "아이디어" \
  --collect
```

**참고**: 데이터 수집은 다음 API를 호출합니다:
- Semantic Scholar (논문)
- CrossRef (논문)
- arXiv (논문)
- GitHub (기술)
- 공공데이터 정보 (메타데이터)

## 4. 예시 스크립트 실행

대화형 방식으로 여러 예시를 실행:

```bash
python example_usage.py
```

## 5. 옵션 설명

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--type` | 콘텐츠 유형 | 게임, 웹툰, OTT, 메타버스, K-POP 등 |
| `--stage` | 사업 단계 | 아이디어, PoC, 런칭, 성장, 해외진출 |
| `--focus` | 관심 영역 | 시장 중심, 기술 중심, 정책 중심 |
| `--collect` | 데이터 수집 | 플래그 (있으면 수집) |
| `--format` | 출력 형식 | markdown, json, both |

## 6. 출력 파일 확인

생성된 파일은 `output/` 폴더에 저장됩니다:
- Markdown: `checklist_[키워드]_[날짜].md`
- JSON: `checklist_[키워드]_[날짜].json`

## 7. API 키 설정 (선택사항)

더 나은 성능을 위해 API 키 설정:

### GitHub API 키
```bash
# 환경변수로 설정
set GITHUB_TOKEN=your_token_here

# 또는 설정 파일 수정
python src/main.py config --set api_keys.github your_token_here
```

### 공공데이터 API 키
```bash
set PUBLIC_DATA_API_KEY=your_key_here
```

## 8. 문제 해결

### 오류: ModuleNotFoundError
```bash
# 의존성 재설치
pip install -r requirements.txt
```

### 오류: API Rate Limit
- GitHub: API 키 설정으로 제한 증가
- 기타 API: 잠시 후 재시도

### 데이터가 수집되지 않음
- 인터넷 연결 확인
- API 서비스 상태 확인
- `--collect` 플래그 확인

## 9. 다음 단계

- [전체 문서](README.md) 읽기
- [프로젝트 계획](plan.md) 확인
- 커스터마이징:
  - `src/checklist/templates.py`에서 질문 수정
  - `config/settings.json`에서 설정 변경

## 10. 실전 예시

### 사업계획서 작성용
```bash
python src/main.py generate "AI 음악 추천 서비스" \
  --type "음악" \
  --stage "아이디어" \
  --focus "시장 중심" \
  --collect \
  --format both
```

### 기술 검증용
```bash
python src/main.py generate "블록체인 게임" \
  --type "게임" \
  --stage "PoC" \
  --focus "기술 중심" \
  --collect
```

### 해외 진출 준비용
```bash
python src/main.py generate "K-드라마 스트리밍" \
  --type "드라마" \
  --stage "해외진출" \
  --focus "정책 중심" \
  --collect
```

---

**도움이 필요하신가요?**
- 전체 명령어 보기: `python src/main.py --help`
- 특정 명령어 도움말: `python src/main.py generate --help`
