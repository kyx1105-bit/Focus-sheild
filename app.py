import streamlit as st
import base64

# ==========================================
# 1. 웹 페이지 기본 설정
# ==========================================
st.set_page_config(page_title="포커스 쉴드 생성기", page_icon="🛡️")

st.title("🛡️ 포커스 쉴드(Focus Shield) 생성기")
st.write("검은색 실행 창(cmd) 깜빡임조차 완전히 없앤 **무소음 완벽 숨김 버전(.vbs)**입니다.")
st.divider()

# ==========================================
# 2. 사용자 설정 UI
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

site_list = [site.strip() for site in user_sites.split(",") if site.strip()]
ps_array = ", ".join([f'"{site}"' for site in site_list])

# ==========================================
# 3. Base64 파워쉘 스크립트 생성
# ==========================================
ps_script = f"""
$hostsPath = "$env:windir\\System32\\drivers\\etc\\hosts"
$blockList = @({ps_array})
$workStart = {work_start}$workEnd = {work_end}

while ($true) {{$currentHour = (Get-Date).Hour
    if ($currentHour -ge$workStart -and $currentHour -lt$workEnd) {{
        $content = Get-Content$hostsPath -Raw
        if ($content -eq $null) {{$content = "" }}
        foreach ($site in$blockList) {{
            if ($content -notmatch [regex]::Escape($site)) {{
                Add-Content -Path $hostsPath -Value "127.0.0.1 $site"
            }}
        }}
    }} else {{
        $lines = Get-Content$hostsPath
        if ($lines -ne $null) {{$newLines = @()
            foreach ($line in$lines) {{
                $match =$false
                foreach ($site in$blockList) {{
                    if ($line -match [regex]::Escape($site)) {{ $match =$true; break }}
                }}
                if (-not $match) {{ $newLines +=$line }}
            }}
            [IO.File]::WriteAllLines($hostsPath,$newLines)
        }}
    }}
    Start-Sleep -Seconds 60
}}
"""

encoded_bytes = ps_script.encode('utf-16le')
encoded_command = base64.b64encode(encoded_bytes).decode('utf-8')

# ==========================================
# 4. 윈도우용 VBScript 템플릿 세팅 (깜빡임 완벽 제거)
# ==========================================
vbs_template = f"""Set objShell = CreateObject("Shell.Application")
psCommand = "-WindowStyle Hidden -ExecutionPolicy Bypass -EncodedCommand {encoded_command}"
' 0은 창을 완전히 숨김(Hide) 처리한다는 의미이며, runas는 관리자 권한을 요청합니다.
objShell.ShellExecute "powershell.exe", psCommand, "", "runas", 0
"""

st.divider()

# ==========================================
# 5. 코드 다운로드 버튼
# ==========================================
st.subheader("3. 맞춤형 스크립트 다운로드")
st.write("버튼을 눌러 `focus_shield.vbs` 파일을 다운로드하고, 컴퓨터에서 **더블클릭**만 하세요.")

st.download_button(
    label="📥 Focus Shield 다운로드 (.vbs)",
    data=vbs_template,
    file_name="focus_shield.vbs",
    mime="text/vbscript"
