@echo off
REM 모든 테스트 실행 스크립트 (Windows)
REM 사용법: run_tests.bat [all|unit|integration]

setlocal enabledelayedexpansion

REM 프로젝트 루트 디렉토리
set PROJECT_ROOT=%~dp0

REM 테스트 타입 결정
if "%1"=="" (
    set TEST_TYPE=all
) else (
    set TEST_TYPE=%1
)

REM 테스트 타입별 실행
if "%TEST_TYPE%"=="all" (
    echo.
    echo ====================================
    echo 모든 테스트 실행 중...
    echo ====================================
    echo.
    python -m pytest tests/ -v --tb=short
    goto end
)

if "%TEST_TYPE%"=="unit" (
    echo.
    echo ====================================
    echo 유닛 테스트 실행 중...
    echo ====================================
    echo.
    python -m pytest tests/ -v -m "not integration" --tb=short
    goto end
)

if "%TEST_TYPE%"=="integration" (
    echo.
    echo ====================================
    echo 통합 테스트 실행 중...
    echo ====================================
    echo.
    python -m pytest tests/ -v -m "integration" --tb=short
    goto end
)

REM 특정 테스트 파일 실행
echo.
echo ====================================
echo test_%TEST_TYPE% 테스트 실행 중...
echo ====================================
echo.
python -m pytest tests/test_%TEST_TYPE%.py -v --tb=short

:end
echo.
echo ====================================
echo 테스트 완료
echo ====================================
pause
