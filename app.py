import time
from datetime import datetime

# 윈도우 기준 hosts 파일 경로 (맥은 '/private/etc/hosts')
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

# 늪에 빠지게 만드는 사이트 목록
block_list = ["www.youtube.com", "youtube.com", "www.dcinside.com"]

# 잠금 시간 설정 (예: 아침 9시 ~ 오후 6시)
work_start = 9
work_end = 18

while True:
    current_hour = datetime.now().hour
    
    # 1. 잠금 시간일 때: 차단 모드
    if work_start <= current_hour < work_end:
        with open(hosts_path, 'r+') as file:
            content = file.read()
            for website in block_list:
                # 파일에 해당 사이트가 없으면 127.0.0.1과 함께 추가
                if website not in content:
                    file.write(redirect_ip + " " + website + "\n")
        print("집중 시간입니다. 사이트가 차단되었습니다.")
    
    # 2. 휴식 시간일 때: 차단 해제 모드
    else:
        with open(hosts_path, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                # 차단 리스트에 있는 사이트가 아닌 줄만 다시 기록 (차단 해제)
                if not any(website in line for website in block_list):
                    file.write(line)
            file.truncate() # 남은 찌꺼기 텍스트 삭제
        print("휴식 시간입니다. 접속 차단이 풀렸습니다.")
    
    # 1분(60초)마다 현재 시간을 체크하며 무한 반복
    time.sleep(60)
