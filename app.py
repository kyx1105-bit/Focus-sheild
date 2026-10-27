import time
from datetime import datetime
import sys

# ==========================================
# 1. 내 입맛대로 설정하기
# ==========================================
# 윈도우 전용 hosts 파일 경로 (수정하지 마세요)
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

# 차단하고 싶은 사이트 목록 (원하는 만큼 추가하세요)
block_list = [
    "www.youtube.com",
    "youtube.com",
    "www.dcinside.com",
    "dcinside.com"
]

# 집중할 시간 설정 (24시간제 기준)
# 예: 9, 18 로 설정하면 아침 9시부터 오후 6시 직전(17:59)까지 차단됩니다.
work_start = 9
work_end = 18

# ==========================================
# 2. 메인 실행 프로그램
# ==========================================
print("🛡️ 포커스 쉴드(Focus Shield)가 시작되었습니다.")
print(f"⏰ 현재 차단 설정 시간: {work_start}시 ~ {work_end}시")

while True:
    try:
        current_hour = datetime.now().hour
        
        # 1. 집중 시간일 때: 차단 모드 작동
        if work_start <= current_hour < work_end:
            with open(hosts_path, 'r+') as file:
                content = file.read()
                for website in block_list:
                    # 파일에 해당 사이트가 없으면 추가해서 접속을 막음
                    if website not in content:
                        file.write(redirect_ip + " " + website + "\n")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 집중 시간! 지정된 사이트가 차단 중입니다.")
        
        # 2. 휴식 시간일 때: 차단 해제 작동
        else:
            with open(hosts_path, 'r+') as file:
                content = file.readlines()
                file.seek(0)
                for line in content:
                    # 차단 리스트에 있는 사이트가 아닌 줄만 다시 기록 (차단 해제)
                    if not any(website in line for website in block_list):
                        file.write(line)
                file.truncate() # 남은 찌꺼기 텍스트 깔끔하게 삭제
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ☕ 휴식 시간! 자유롭게 접속 가능합니다.")
        
        # 1분(60초)마다 현재 시간을 체크하며 무한 반복
        time.sleep(60)

    # 관리자 권한 없이 실행했을 때의 친절한 에러 안내
    except PermissionError:
        print("\n❌ [실행 오류] '관리자 권한'이 필요합니다!")
        print("이 프로그램은 윈도우 시스템 파일을 다룹니다.")
        print("명령 프롬프트(cmd)나 VS Code를 반드시 '관리자 권한으로 실행'한 뒤 작동시켜주세요.")
        time.sleep(15)
        sys.exit()
        
    except Exception as e:
        print(f"\n❌ 알 수 없는 오류 발생: {e}")
        time.sleep(15)
        sys.exit()
