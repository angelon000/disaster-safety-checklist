# 재난·안전 체크리스트 시스템 배포 가이드

이 문서는 재난·안전 체크리스트 시스템을 외부에서 접속 가능하도록 배포하는 방법을 설명합니다.

## 목차
1. [로컬 네트워크 배포](#1-로컬-네트워크-배포)
2. [인터넷 배포 (ngrok)](#2-인터넷-배포-ngrok)
3. [클라우드 배포](#3-클라우드-배포)
4. [프로덕션 배포](#4-프로덕션-배포)

---

## 1. 로컬 네트워크 배포

같은 네트워크(Wi-Fi, 회사 내부망)에 있는 다른 기기에서 접속할 수 있도록 설정합니다.

### 1.1 실행

```bash
# 대시보드 실행
python dashboard/app.py
```

실행하면 다음과 같이 표시됩니다:
```
======================================================================
  재난·안전 체크리스트 대시보드
======================================================================

  🌐 로컬 접속: http://localhost:8000
  🌍 네트워크 접속: http://192.168.1.100:8000
  📚 API 문서: http://localhost:8000/docs

  💡 외부 접속을 위해 방화벽 8000번 포트를 열어주세요.
  🛑 종료하려면 Ctrl+C를 누르세요.
```

### 1.2 방화벽 설정

#### Windows
```powershell
# PowerShell 관리자 권한으로 실행
New-NetFirewallRule -DisplayName "재난안전 대시보드" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

또는 GUI로:
1. `Windows Defender 방화벽` → `고급 설정`
2. `인바운드 규칙` → `새 규칙`
3. `포트` → `TCP` → `특정 로컬 포트: 8000`
4. `연결 허용` → 이름: "재난안전 대시보드 8000"

#### Linux/Ubuntu
```bash
# UFW 사용 시
sudo ufw allow 8000/tcp
sudo ufw reload

# firewalld 사용 시
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

#### macOS
```bash
# macOS는 기본적으로 방화벽이 꺼져있음
# 켜져있다면 시스템 환경설정 → 보안 및 개인 정보 보호 → 방화벽 옵션에서 설정
```

### 1.3 접속 테스트

같은 네트워크의 다른 기기에서:
```
http://[서버IP주소]:8000
예: http://192.168.1.100:8000
```

---

## 2. 인터넷 배포 (ngrok)

인터넷을 통해 전 세계 어디서나 접속 가능하도록 터널링 서비스를 사용합니다.

### 2.1 ngrok 설치

#### Windows
```powershell
# Chocolatey 사용
choco install ngrok

# 또는 수동 다운로드
# https://ngrok.com/download 에서 다운로드
```

#### Linux/macOS
```bash
# 공식 설치 스크립트
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

### 2.2 ngrok 설정

1. https://ngrok.com 에서 무료 계정 생성
2. 인증 토큰 설정:
```bash
ngrok config add-authtoken [YOUR_AUTH_TOKEN]
```

### 2.3 실행

터미널 2개를 엽니다:

**터미널 1 - 대시보드 실행**
```bash
python dashboard/app.py
```

**터미널 2 - ngrok 터널 생성**
```bash
ngrok http 8000
```

ngrok이 생성한 URL로 접속:
```
Forwarding: https://abcd-1234-5678.ngrok-free.app -> http://localhost:8000
```

**장점:**
- 간단하고 빠름
- HTTPS 자동 지원
- 별도 서버 불필요

**단점:**
- 무료 버전은 URL이 매번 변경됨
- 세션 제한 (무료: 2시간)

---

## 3. 클라우드 배포

### 3.1 Docker 이미지 생성

#### Dockerfile 작성

`Dockerfile` 생성:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 실행
CMD ["python", "dashboard/app.py"]
```

#### 빌드 및 실행
```bash
# 이미지 빌드
docker build -t disaster-safety-checklist .

# 컨테이너 실행
docker run -d -p 8000:8000 --name checklist-dashboard disaster-safety-checklist
```

### 3.2 AWS EC2 배포

1. **EC2 인스턴스 생성**
   - Ubuntu Server 22.04 LTS
   - t2.micro (프리티어)
   - 보안 그룹: TCP 8000 포트 개방

2. **서버 설정**
```bash
# SSH 접속
ssh -i your-key.pem ubuntu@[EC2-PUBLIC-IP]

# 프로젝트 복사
git clone [YOUR-REPO-URL]
cd kcl

# 의존성 설치
pip install -r requirements.txt

# 백그라운드 실행
nohup python dashboard/app.py > dashboard.log 2>&1 &
```

3. **접속**
```
http://[EC2-PUBLIC-IP]:8000
```

### 3.3 Heroku 배포

1. **Procfile 생성**
```
web: python dashboard/app.py
```

2. **runtime.txt 생성**
```
python-3.10.12
```

3. **배포**
```bash
heroku login
heroku create disaster-safety-checklist
git push heroku main
heroku open
```

### 3.4 Google Cloud Run 배포

1. **gcloud 설정**
```bash
gcloud init
gcloud auth login
```

2. **배포**
```bash
# 컨테이너 빌드 및 배포
gcloud run deploy disaster-safety-checklist \
  --source . \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated
```

---

## 4. 프로덕션 배포

실제 운영 환경을 위한 설정입니다.

### 4.1 환경 변수 설정

`.env` 파일 생성:
```bash
# 환경
ENVIRONMENT=production

# 데이터베이스
DATABASE_PATH=./data/checklist.db

# 보안
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 포트
PORT=8000
```

### 4.2 Nginx 리버스 프록시

**nginx.conf**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.3 SSL/HTTPS 설정 (Let's Encrypt)

```bash
# Certbot 설치
sudo apt-get install certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 자동 갱신 설정
sudo certbot renew --dry-run
```

### 4.4 systemd 서비스 등록

`/etc/systemd/system/disaster-checklist.service`:
```ini
[Unit]
Description=Disaster Safety Checklist Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/kcl
Environment="PATH=/home/ubuntu/.local/bin:/usr/bin"
ExecStart=/usr/bin/python3 dashboard/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

서비스 시작:
```bash
sudo systemctl daemon-reload
sudo systemctl enable disaster-checklist
sudo systemctl start disaster-checklist
sudo systemctl status disaster-checklist
```

### 4.5 모니터링

**로그 확인**
```bash
# systemd 로그
sudo journalctl -u disaster-checklist -f

# 애플리케이션 로그
tail -f dashboard.log
```

**헬스 체크**
```bash
curl http://localhost:8000/health
```

---

## 보안 권장사항

### 1. 환경 변수 관리
- `.env` 파일을 git에 커밋하지 마세요
- 민감한 정보는 환경 변수로 관리

### 2. HTTPS 사용
- 프로덕션에서는 반드시 HTTPS 사용
- Let's Encrypt 무료 인증서 활용

### 3. 방화벽 설정
- 필요한 포트만 개방
- SSH는 키 인증만 허용

### 4. 정기 업데이트
```bash
# 의존성 업데이트
pip install --upgrade -r requirements.txt

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y
```

### 5. 백업
```bash
# 데이터베이스 백업
cp data/checklist.db data/checklist.db.backup.$(date +%Y%m%d)

# 정기 백업 (cron)
0 2 * * * cp /home/ubuntu/kcl/data/checklist.db /home/ubuntu/backups/checklist.db.$(date +\%Y\%m\%d)
```

---

## 트러블슈팅

### 포트가 이미 사용 중
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID번호] /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### 방화벽 규칙 확인
```bash
# Windows
netsh advfirewall firewall show rule name=all | findstr 8000

# Linux (UFW)
sudo ufw status

# Linux (firewalld)
sudo firewall-cmd --list-all
```

### 연결 테스트
```bash
# 로컬 테스트
curl http://localhost:8000/health

# 원격 테스트
curl http://[서버IP]:8000/health
```

---

## 참고 자료

- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn 설정](https://www.uvicorn.org/settings/)
- [ngrok 문서](https://ngrok.com/docs)
- [Docker 문서](https://docs.docker.com/)
- [Let's Encrypt](https://letsencrypt.org/)

---

## 문의

배포 관련 문제가 있으시면 이슈를 등록해주세요.
