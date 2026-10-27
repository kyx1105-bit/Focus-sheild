"""
Focus Shield (app.py)
---------------------
지정된 시간 동안 특정 웹사이트의 접속을 로컬 PC에서 차단하는 백그라운드 프로그램입니다.
"""

import time
from datetime import datetime
import sys
import ctypes
import os

# ==========================================
# 1. 환경 설정 (Configuration)
# ==========================================
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"

# 차단할 사이트 목록
BLOCK_LIST = [
    "www.youtube.com",
    "youtube.com",
    "www.dcinside.com",
    "dcinside.com"
]

# 차단 작동 시간 (24시간제)
WORK_START = 9
WORK_END = 18


# ==========================================
# 2. 핵심 함수 (Functions)
# ==========================================
def is_admin():
    """현재 스크립트가 관리자 권한으로 실행되었는지 확인합니다."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_sites():
    """hosts 파일에 차단 사이트를 추가합니다."""
    with open(HOSTS_PATH, 'r+') as file:
        content = file.read()
        for website in BLOCK_LIST:
            if website not in content:
                file.write(f"{REDIRECT_IP} {website}\n")

def unblock_sites():
    """hosts 파일에서 차단 사이트를 제거합니다."""
    with open(HOSTS_PATH, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(website in line for website in BLOCK_LIST):
                file.write(line)
        file.truncate()


# ==========================================
# 3. 메인 실행부 (Main Loop)
# ==========================================
def main():
    # 관리자 권한 체크
    if not is_admin():
        print("❌ [권한 오류] 시스템 파일을 수정하려면 '관리자 권한'이 필요합니다.")
        print("터미널(cmd 또는 PowerShell)을 관리자 권한으로 실행한 뒤 다시 시도하세요.")
        time.sleep(5)
        sys.exit(1)

    print("🛡️ 포커스 쉴드(Focus Shield) 작동 시작...")
    print(f"⏰ 설정된 집중 시간: {WORK_START}시 ~ {WORK_END}시\n")

    while True:
        current_hour = datetime.now().hour
        
        try:
            if WORK_START <= current_hour < WORK_END:
                block_sites()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 집중 시간 작동 중 (사이트 차단)")
            else:
                unblock_sites()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ☕ 휴식 시간 (차단 해제됨)")
            
            # 60초 대기 후 재검사
            time.sleep(60)
            
        except Exception as e:
            print(f"❌ 예기치 않은 오류 발생: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
