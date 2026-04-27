# Discord-Git Bot 가상환경 설정 스크립트 (PowerShell용)
# 이 스크립트는 Python 가상환경을 생성하고 필요한 패키지를 설치합니다.

# UTF-8 인코딩 설정
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

Write-Host ""
Write-Host "========================================"
Write-Host "Discord-Git Bot 가상환경 설정"
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 가상환경 디렉토리 설정
$VENV_DIR = Join-Path $PSScriptRoot "..\venv"

# 이미 가상환경이 존재하는지 확인
if (Test-Path $VENV_DIR) {
    Write-Host "[안내] 가상환경이 이미 존재합니다." -ForegroundColor Yellow
    Write-Host "경로: $VENV_DIR"
    Write-Host ""
    $choice = Read-Host "기존 가상환경을 삭제하시겠습니까? (Y/N)"
    
    if ($choice -eq 'Y' -or $choice -eq 'y') {
        Write-Host "기존 가상환경을 삭제 중..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $VENV_DIR
    } else {
        Write-Host "기존 가상환경을 유지합니다."
    }
}

# 새 가상환경 생성
Write-Host ""
Write-Host "[진행] 새로운 가상환경을 생성 중입니다..." -ForegroundColor Cyan
python -m venv $VENV_DIR

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[오류] 가상환경 생성에 실패했습니다." -ForegroundColor Red
    Write-Host "Python이 설치되어 있는지 확인하세요."
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host "[완료] 가상환경이 생성되었습니다." -ForegroundColor Green
Write-Host ""

# 가상환경 활성화
Write-Host "[진행] 가상환경을 활성화 중입니다..." -ForegroundColor Cyan
& "$VENV_DIR\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[오류] 가상환경 활성화에 실패했습니다." -ForegroundColor Red
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host "[완료] 가상환경이 활성화되었습니다." -ForegroundColor Green
Write-Host ""

# requirements.txt가 존재하는 경우 패키지 설치
$REQUIREMENTS_FILE = Join-Path $PSScriptRoot "..\requirements.txt"

if (Test-Path $REQUIREMENTS_FILE) {
    Write-Host "[진행] requirements.txt에서 패키지를 설치 중입니다..." -ForegroundColor Cyan
    Write-Host "경로: $REQUIREMENTS_FILE"
    Write-Host ""
    
    # pip 업그레이드 (선택사항 - 오류 무시)
    Write-Host "[정보] pip을 업그레이드 중입니다..." -ForegroundColor Yellow
    python -m pip install --upgrade pip --quiet 2>$null
    
    # 패키지 설치
    pip install -r $REQUIREMENTS_FILE
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[경고] 패키지 설치 중 일부 오류가 발생했습니다." -ForegroundColor Yellow
        Write-Host "다시 실행하거나 수동으로 설치해주세요."
    } else {
        Write-Host "[완료] 모든 패키지가 설치되었습니다." -ForegroundColor Green
    }
} else {
    Write-Host "[안내] requirements.txt 파일이 없습니다." -ForegroundColor Yellow
    Write-Host "pip install [패키지명] 을 사용하여 패키지를 설치할 수 있습니다."
}

Write-Host ""
Write-Host "========================================"
Write-Host "가상환경 설정이 완료되었습니다!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "다음 번에는 activate.ps1를 실행하여 가상환경을 활성화하세요."
Write-Host ""
