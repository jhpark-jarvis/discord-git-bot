# 모든 테스트 실행 스크립트 (PowerShell)
# 사용법: .\run_tests.ps1 [-TestType all|unit|integration]

param(
    [Parameter(Position = 0)]
    [ValidateSet('all', 'unit', 'integration', 'git_commands', 'git_helper', 'git_service', 'integration_git')]
    [string]$TestType = 'all'
)

# 프로젝트 루트
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "테스트 실행: $TestType" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 테스트 타입별 실행
switch ($TestType) {
    'all' {
        Write-Host "모든 테스트를 실행합니다..." -ForegroundColor Yellow
        & python -m pytest tests/ -v --tb=short
        break
    }
    'unit' {
        Write-Host "유닛 테스트를 실행합니다..." -ForegroundColor Yellow
        & python -m pytest tests/ -v -m "not integration" --tb=short
        break
    }
    'integration' {
        Write-Host "통합 테스트를 실행합니다..." -ForegroundColor Yellow
        & python -m pytest tests/ -v -m "integration" --tb=short
        break
    }
    default {
        Write-Host "특정 테스트를 실행합니다: test_$TestType" -ForegroundColor Yellow
        & python -m pytest "tests/test_$TestType.py" -v --tb=short
    }
}

$TestResult = $LASTEXITCODE

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "테스트 완료" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan

if ($TestResult -eq 0) {
    Write-Host "모든 테스트가 통과했습니다!" -ForegroundColor Green
} else {
    Write-Host "일부 테스트가 실패했습니다." -ForegroundColor Red
}

Write-Host ""
exit $TestResult
