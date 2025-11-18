@echo off
REM 재난·안전 체크리스트 대시보드 실행 스크립트 (Windows)

echo.
echo ======================================================================
echo   재난·안전 체크리스트 대시보드 시작
echo ======================================================================
echo.

REM Python이 설치되어 있는지 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되어 있지 않습니다.
    echo Python 3.8 이상을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 의존성 확인
echo [1/3] 의존성 확인 중...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [INFO] 의존성을 설치합니다...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] 의존성 설치에 실패했습니다.
        pause
        exit /b 1
    )
)

REM 데이터베이스 디렉토리 생성
echo [2/3] 데이터베이스 디렉토리 확인 중...
if not exist "data" mkdir data

REM 서버 실행
echo [3/3] 서버를 시작합니다...
echo.
python dashboard/app.py

pause
