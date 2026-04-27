@echo off
REM Discord-Git Bot 가상환경 설정 스크립트
REM 이 스크립트는 Python 가상환경을 생성하고 필요한 패키지를 설치합니다.

echo.
echo ========================================
echo Discord-Git Bot 가상환경 설정
echo ========================================
echo.

REM 가상환경 디렉토리 설정
set VENV_DIR=%~dp0..\venv

REM 이미 가상환경이 존재하는지 확인
if exist "%VENV_DIR%" (
    echo [안내] 가상환경이 이미 존재합니다.
    echo 경로: %VENV_DIR%
    echo.
    echo 기존 가상환경을 삭제하시겠습니까? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        echo 기존 가상환경을 삭제 중...
        rmdir /s /q "%VENV_DIR%"
    ) else (
        echo 기존 가상환경을 유지합니다.
    )
)

REM 새 가상환경 생성
echo.
echo [진행] 새로운 가상환경을 생성 중입니다...
python -m venv "%VENV_DIR%"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [오류] 가상환경 생성에 실패했습니다.
    echo Python이 설치되어 있는지 확인하세요.
    pause
    exit /b 1
)

echo [완료] 가상환경이 생성되었습니다.
echo.

REM 가상환경 활성화
echo [진행] 가상환경을 활성화 중입니다...
call "%VENV_DIR%\Scripts\activate.bat"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [오류] 가상환경 활성화에 실패했습니다.
    pause
    exit /b 1
)

echo [완료] 가상환경이 활성화되었습니다.
echo.

REM requirements.txt가 존재하는 경우 패키지 설치
set REQUIREMENTS_FILE=%~dp0..\requirements.txt

if exist "%REQUIREMENTS_FILE%" (
    echo [진행] requirements.txt에서 패키지를 설치 중입니다...
    echo 경로: %REQUIREMENTS_FILE%
    echo.
    pip install --upgrade pip
    pip install -r "%REQUIREMENTS_FILE%"
    
    if %ERRORLEVEL% neq 0 (
        echo.
        echo [경고] 패키지 설치 중 일부 오류가 발생했습니다.
    ) else (
        echo [완료] 모든 패키지가 설치되었습니다.
    )
) else (
    echo [안내] requirements.txt 파일이 없습니다.
    echo pip install [패키지명] 을 사용하여 패키지를 설치할 수 있습니다.
)

echo.
echo ========================================
echo 가상환경 설정이 완료되었습니다!
echo ========================================
echo.
echo 다음 번에는 activate.bat를 실행하여 가상환경을 활성화하세요.
echo.
pause
