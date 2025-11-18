"""
KCL 체크리스트 대시보드 실행 스크립트
"""
import sys
import webbrowser
from pathlib import Path
import time
import threading

# dashboard 디렉토리를 Python 경로에 추가
dashboard_dir = Path(__file__).parent / 'dashboard'
sys.path.insert(0, str(dashboard_dir))

def open_browser():
    """3초 후 브라우저 자동 열기"""
    time.sleep(3)
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🚀 재난·안전 체크리스트 대시보드")
    print("="*70)
    print("\n  대시보드를 시작합니다...")
    print("  브라우저가 자동으로 열립니다.\n")

    # 브라우저 자동 열기 (백그라운드)
    threading.Thread(target=open_browser, daemon=True).start()

    # FastAPI 앱 실행
    from app import app
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
