#!/bin/bash
# 재난·안전 체크리스트 대시보드 실행 스크립트 (Linux/macOS)

set -e  # 에러 발생 시 즉시 종료

echo ""
echo "======================================================================"
echo "  재난·안전 체크리스트 대시보드 시작"
echo "======================================================================"
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Python 확인
echo -e "${YELLOW}[1/4]${NC} Python 확인 중..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python3가 설치되어 있지 않습니다."
    echo "Python 3.8 이상을 설치해주세요."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION 감지됨"

# 가상환경 확인 및 생성
echo -e "${YELLOW}[2/4]${NC} 가상환경 확인 중..."
if [ ! -d "venv" ]; then
    echo "가상환경을 생성합니다..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} 가상환경 생성 완료"
fi

# 가상환경 활성화
echo "가상환경을 활성화합니다..."
source venv/bin/activate

# 의존성 설치
echo -e "${YELLOW}[3/4]${NC} 의존성 확인 중..."
if ! pip show fastapi &> /dev/null; then
    echo "의존성을 설치합니다..."
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} 의존성 설치 완료"
else
    echo -e "${GREEN}✓${NC} 의존성이 이미 설치되어 있습니다"
fi

# 데이터베이스 디렉토리 생성
echo -e "${YELLOW}[4/4]${NC} 데이터베이스 디렉토리 확인 중..."
mkdir -p data
echo -e "${GREEN}✓${NC} 데이터베이스 디렉토리 준비 완료"

# 서버 실행
echo ""
echo -e "${GREEN}서버를 시작합니다...${NC}"
echo ""

python3 dashboard/app.py
