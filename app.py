import streamlit as st

# ==========================================
# 1. 웹 페이지 기본 설정
# ==========================================
st.set_page_config(page_title="포커스 쉴드 생성기", page_icon="🛡️")

st.title("🛡️ 포커스 쉴드(Focus Shield) 생성기")
st.write("""
클라우드 웹 서버에서는 방문자의 PC 접속을 직접 차단할 수 없습니다. 
대신, 아래에서 원하는 조건을 설정한 뒤 **내 PC용 맞춤형 차단 스크립트**를 다운로드하세요.
""")
st.divider()

# ==========================================
# 2. 사용자 설정 UI (웹 화면)
# ==========================================
st.subheader("1. 딴짓 방지 시간 설정")
time_range = st.slider(
    "집중할 시간대(24시간제)를 선택하세요", 
    min_value=0, max_value=24, value=(9, 18)
)
work_start, work_end = time_range

st.subheader("2. 차단할 웹사이트 입력")
default_sites = "www.youtube.com, youtube.com, www.dcinside.com, dcinside.com"
user_sites = st.text_area("쉼표(,)로 구분해서 적어주세요.", default_sites)

# 텍스트를 리스트 형태로 변환
site_list = [site.strip() for site in user_sites.split(",") if site.strip()]

# ==========================================
# 3. 다운로드될 로컬 PC용 파이썬 코드 템플릿
# ==========================================
# 사용자가 설정한 값(시간, 사이트)이 반영된 코드를 텍스트로 생성합니다.
script_template = f"""import time
from datetime import datetime
import sys
import ctypes

HOSTS_PATH = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
REDIRECT_IP = "127.0.0.1"

BLOCK_LIST = {site_list}

WORK_START = {work_start}
WORK_END = {work_end}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not is_admin():
        print("❌ [권한 오류] '관리자 권한'이 필요합니다.")
        time.sleep(5)
        sys.exit(1)

    print(f"🛡️ 포커스 쉴드 작동 중... (차단 시간: {{WORK_START}}시 ~ {{WORK_END}}시)")

    while True:
        try:
            current_hour = datetime.now().hour
            
            if WORK_START <= current_hour < WORK_END:
                with open(HOSTS_PATH, 'r+') as file:
                    content = file.read()
                    for website in BLOCK_LIST:
                        if website not in content:
                            file.write(f"{{REDIRECT_IP}} {{website}}\\n")
            else:
                with open(HOSTS_PATH, 'r+') as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if not any(website in line for website in BLOCK_LIST):
                            file.write(line)
                    file.truncate()
            
            time.sleep(60)
            
        except Exception as e:
            time.sleep(60)

if __name__ == "__main__":
    main()
"""

st.divider()

# ==========================================
# 4. 코드 다운로드 버튼
# ==========================================
st.subheader("3. 맞춤형 스크립트 다운로드")
st.write("버튼을 눌러 `focus_shield.pyw` 파일을 다운로드하고, 윈도우에서 '관리자 권한'으로 실행하세요.")

st.download_button(
    label="📥 Focus Shield 다운로드 (.pyw)",
    data=script_template,
    file_name="focus_shield.pyw",
    mime="text/x-python"
)
