# Discord-Git Bot 가상환경 활성화 스크립트 (PowerShell용)

# UTF-8 인코딩 설정
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

$VENV_DIR = Join-Path $PSScriptRoot "..\venv"

if (-not (Test-Path $VENV_DIR)) {
    Write-Host ""
    Write-Host "[오류] 가상환경을 찾을 수 없습니다." -ForegroundColor Red
    Write-Host "경로: $VENV_DIR"
    Write-Host ""
    Write-Host "setup_venv.ps1를 먼저 실행하여 가상환경을 생성하세요."
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host ""
Write-Host "========================================"
Write-Host "Discord-Git Bot 가상환경 활성화"
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& "$VENV_DIR\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[오류] 가상환경 활성화에 실패했습니다." -ForegroundColor Red
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host "[완료] 가상환경이 활성화되었습니다." -ForegroundColor Green
Write-Host ""
Write-Host "사용 가능한 명령:"
Write-Host "  - pip install [패키지명]     : 패키지 설치"
Write-Host "  - python src/main.py          : 봇 실행 (구현 후)"
Write-Host "  - deactivate                  : 가상환경 비활성화"
Write-Host ""
