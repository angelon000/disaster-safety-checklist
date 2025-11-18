# 🚀 Render.com 무료 배포 가이드

Render.com에서 클릭 몇 번으로 무료 24/7 배포가 가능합니다!

## ✨ Render.com 장점

- ✅ **완전 무료** (Free tier)
- ✅ **24/7 실행** (15분 미사용시 슬립, 첫 요청시 자동 재시작)
- ✅ **GitHub 자동 배포** (푸시하면 자동으로 재배포)
- ✅ **HTTPS 자동** (SSL 인증서 자동 설치)
- ✅ **설정 초간단** (render.yaml 하나면 끝)
- ✅ **재시작 없음** (Codespaces와 달리 항상 켜져있음)

## 📋 배포 단계

### 1단계: Render.com 가입

1. [Render.com](https://render.com) 접속
2. **Get Started** 클릭
3. GitHub 계정으로 로그인

### 2단계: 저장소 연결

1. Render 대시보드에서 **New +** 버튼 클릭
2. **Web Service** 선택
3. **Connect GitHub** → 저장소 `disaster-safety-checklist` 선택
4. 권한 승인

### 3단계: 자동 배포 (render.yaml 사용)

저장소에 이미 `render.yaml` 파일이 있으므로:

1. **You are in control** 섹션에서 **Apply** 클릭
2. Render가 자동으로 설정을 읽어서 배포 시작
3. 5-10분 정도 기다리면 배포 완료!

배포 완료되면 다음과 같은 URL이 생성됩니다:
```
https://disaster-safety-checklist.onrender.com
```

### 4단계: 접속 확인

1. Render 대시보드에서 생성된 URL 클릭
2. 대시보드가 정상적으로 열리는지 확인
3. 체크리스트 생성 테스트

## ⚙️ 수동 설정 (render.yaml 없이)

`render.yaml`을 사용하지 않고 수동으로 설정하려면:

1. **New Web Service** 생성
2. 다음 정보 입력:
   - **Name**: `disaster-safety-checklist`
   - **Region**: `Singapore` (한국과 가장 가까움)
   - **Branch**: `master`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python dashboard/app.py`
3. **Free** 플랜 선택
4. **Create Web Service** 클릭

## 🔄 자동 재배포

GitHub에 푸시하면 **자동으로 재배포**됩니다:

```bash
git add .
git commit -m "업데이트"
git push origin master
```

Render가 자동으로 감지해서 새 버전을 배포합니다!

## 📊 로그 확인

Render 대시보드에서:
1. 서비스 클릭
2. **Logs** 탭에서 실시간 로그 확인
3. 에러가 있으면 여기서 확인 가능

## ⚠️ 주의사항

### 1. SQLite 데이터 손실

Render의 무료 티어는 **임시 파일 시스템**을 사용합니다:
- 재배포할 때마다 SQLite 데이터베이스가 초기화됩니다
- 생성한 프로젝트들이 사라집니다

**해결책:**
- 중요한 데이터는 다운로드해서 백업
- 또는 PostgreSQL로 전환 (Render의 무료 PostgreSQL 제공)

### 2. 콜드 스타트 (Cold Start)

무료 티어는 **15분간 미사용시 슬립 모드**로 들어갑니다:
- 첫 접속시 30초~1분 정도 로딩 시간
- 이후 접속은 즉시 응답

### 3. 무료 티어 제한

- **750시간/월** 실행 시간 (한 달 내내 켜놔도 충분)
- **100GB 대역폭/월**
- **512MB RAM**

이 프로젝트는 제한 내에서 충분히 실행됩니다!

## 🎯 대안: Railway.app

Render보다 더 빠른 콜드 스타트를 원한다면:

### Railway.app 특징
- 더 빠른 시작 속도
- 월 $5 무료 크레딧
- 더 쉬운 설정

### Railway 배포 방법

1. [Railway.app](https://railway.app) 접속
2. **Start a New Project** → **Deploy from GitHub repo**
3. 저장소 선택
4. 자동으로 Python 감지 및 배포
5. **Settings** → **Generate Domain** 클릭

## 🐳 대안: Fly.io

가장 빠른 성능을 원한다면:

### Fly.io 특징
- 전 세계 엣지 배포
- 더 빠른 응답 속도
- 무료 티어: 3개 VM, 3GB 스토리지

### Fly.io 배포 방법

1. [Fly.io CLI 설치](https://fly.io/docs/hands-on/install-flyctl/)
2. 프로젝트 디렉토리에서:
   ```bash
   flyctl launch
   flyctl deploy
   ```

## 🎉 결론

**추천 순서:**
1. **Render.com** - 가장 쉽고 안정적 (설정 자동화)
2. **Railway.app** - 더 빠른 시작 속도
3. **Fly.io** - 최고 성능

모두 무료이고, GitHub 연동 자동 배포를 지원합니다!

## 🔗 유용한 링크

- [Render 공식 문서](https://render.com/docs)
- [Railway 공식 문서](https://docs.railway.app)
- [Fly.io 공식 문서](https://fly.io/docs)

---

**문제가 생기면:**
- Render 대시보드 → Logs 탭 확인
- GitHub Issues에 문의
