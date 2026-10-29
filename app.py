import streamlit as st

# ==========================================
# 1. 웹 페이지 기본 설정
# ==========================================
st.set_page_config(page_title="포커스 쉴드 생성기", page_icon="🛡️")

st.title("🛡️ 포커스 쉴드(Focus Shield) 생성기")
st.write("파이썬 설치? **필요 없습니다.** 내 PC 설정에 맞춘 윈도우용 실행 파일(.bat)을 만들어 드립니다.")
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

# 텍스트를 파워쉘 배열 형태로 변환 (예: "youtube.com", "dcinside.com")
site_list = [site.strip() for site in user_sites.split(",") if site.strip()]
ps_array = ", ".join([f'"{site}"' for site in site_list])

# ==========================================
# 3. 파이썬 불필요: 윈도우 기본 PowerShell & BAT 템플릿
# ==========================================
# 파이썬 없이 윈도우에서 바로 도는 배치(BAT) 스크립트입니다.
# 관리자 권한을 스스로 묻고, 실행 즉시 까만 창을 백그라운드로 숨깁니다.
bat_template = f"""<# :
@echo off
:: 1. 관리자 권한 체크 및 숨김 실행 요청
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)

:: 2. 권한이 있다면 본 파일 코드를 읽어들여 백그라운드에서 조용히 실행
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "iex ((Get-Content '%~f0') -join [Environment]::NewLine); Invoke-FocusShield"
exit /b
#>

function Invoke-FocusShield {{
    $hostsPath = "$env:windir\\System32\\drivers\\etc\\hosts"
    $redirectIp = "127.0.0.1"
    $blockList = @({ps_array})
    $workStart = {work_start}
    $workEnd = {work_end}

    while ($true) {{
        $currentHour = (Get-Date).Hour
        if ($currentHour -ge $workStart -and $currentHour -lt $workEnd) {{
            # 집중 시간: 차단 모드
            $content = Get-Content $hostsPath -Raw
            foreach ($site in $blockList) {{
                if ($content -notmatch [regex]::Escape($site)) {{
                    Add-Content -Path $hostsPath -Value "$redirectIp $site"
                }}
            }}
        }} else {{
            # 휴식 시간: 차단 해제 모드
            $lines = Get-Content $hostsPath
            $newLines = $lines | Where-Object {{
                $line = $_
                $match = $false
                foreach ($site in $blockList) {{
                    if ($line -match [regex]::Escape($site)) {{ $match = $true; break }}
                }}
                -not $match
            }}
            [IO.File]::WriteAllLines($hostsPath, $newLines)
        }}
        Start-Sleep -Seconds 60
    }}
}}
"""

st.divider()

# ==========================================
# 4. 코드 다운로드 버튼
# ==========================================
st.subheader("3. 맞춤형 스크립트 다운로드")
st.write("버튼을 눌러 `focus_shield.bat` 파일을 다운로드하고, 컴퓨터에서 **더블클릭**만 하세요.")

st.download_button(
    label="📥 Focus Shield 다운로드 (.bat)",
    data=bat_template,
    file_name="focus_shield.bat",
    mime="application/x-msdos-program"
)
