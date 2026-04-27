@echo off
REM Discord-Git Bot 가상환경 활성화 스크립트

set VENV_DIR=%~dp0..\venv

if not exist "%VENV_DIR%" (
    echo [오류] 가상환경을 찾을 수 없습니다.
    echo 경로: %VENV_DIR%
    echo.
    echo setup_venv.bat를 먼저 실행하여 가상환경을 생성하세요.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Discord-Git Bot 가상환경 활성화
echo ========================================
echo.

call "%VENV_DIR%\Scripts\activate.bat"

if %ERRORLEVEL% neq 0 (
    echo [오류] 가상환경 활성화에 실패했습니다.
    pause
    exit /b 1
)

echo [완료] 가상환경이 활성화되었습니다.
echo.
echo 사용 가능한 명령:
echo  - pip install [패키지명]     : 패키지 설치
echo  - python src/main.py          : 봇 실행 (구현 후)
echo  - deactivate                  : 가상환경 비활성화
echo.
