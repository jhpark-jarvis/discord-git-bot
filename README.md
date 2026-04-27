# Discord-Git Bot

Discord 서버와 Git 저장소를 연동하는 Discord 봇 프로젝트입니다.

## 프로젝트 구조

```
discord-git-bot/
├── scripts/
│   ├── setup_venv.bat          # 가상환경 생성 (cmd용)
│   ├── setup_venv.ps1          # 가상환경 생성 (PowerShell용)
│   ├── activate.bat            # 가상환경 활성화 (cmd용)
│   └── activate.ps1            # 가상환경 활성화 (PowerShell용)
├── src/
│   └── main.py                 # 봇 메인 코드
├── config/
│   └── .env.example            # 환경설정 예제
├── requirements.txt            # Python 의존성
├── .gitignore                  # Git 무시 파일
└── README.md                   # 프로젝트 설명
```

## 빠른 시작

### 방법 1: Command Prompt (cmd) 사용

#### 1단계: 가상환경 설정 (첫 실행)
```cmd
scripts\setup_venv.bat
```

#### 2단계: 가상환경 활성화 (이후 실행)
```cmd
scripts\activate.bat
```

### 방법 2: PowerShell 사용

#### 1단계: 가상환경 설정 (첫 실행)
```powershell
.\scripts\setup_venv.ps1
```

**주의**: PowerShell에서 실행 정책 오류 발생 시:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
그 후 다시 실행하세요.

#### 2단계: 가상환경 활성화 (이후 실행)
```powershell
.\scripts\activate.ps1
```

### 공통 단계: 환경설정

#### 3단계: `.env` 파일 생성

**cmd 사용:**
```cmd
copy config\.env.example config\.env
```

**PowerShell 사용:**
```powershell
Copy-Item config\.env.example config\.env
```

#### 4단계: 설정 수정

`config/.env` 파일을 편집하여 다음 정보 입력:
```env
# Discord 봇 토큰 (https://discord.com/developers/applications에서 발급)
DISCORD_TOKEN=your_bot_token_here

# Git 저장소 설정
GIT_REPO_URL=https://github.com/username/repository.git
GIT_REPO_PATH=./repositories/

# 로깅 설정
LOG_LEVEL=INFO
```

#### 5단계: 봇 실행

가상환경이 활성화된 상태에서:
```bash
python src/main.py
```

## 의존성

- **discord.py** (>=2.0.0) - Discord 봇 라이브러리
- **GitPython** (>=3.1.0) - Git 작업 관리
- **python-dotenv** (>=0.19.0) - 환경변수 관리
- **aiohttp** (>=3.8.0) - 비동기 HTTP 요청

모든 의존성은 `setup_venv.bat` 또는 `setup_venv.ps1` 실행 시 자동 설치됩니다.

## 스크립트 설명

### setup_venv.bat (cmd용)
- 새로운 Python 가상환경 생성 (`venv/` 디렉토리)
- 기존 가상환경 있을 시 삭제 여부 확인
- `requirements.txt`의 패키지 자동 설치
- 한글 완벽 지원
- **첫 실행 시에만 필요** (한 번만 실행하면 됨)

### setup_venv.ps1 (PowerShell용)
- cmd 버전과 동일한 기능
- PowerShell에서 한글이 깨지는 현상 자동 해결
- 색상 있는 출력으로 더 이쁜 UI 제공
- 한글 완벽 지원
- **첫 실행 시에만 필요** (한 번만 실행하면 됨)

### activate.bat (cmd용)
- 기존 가상환경 활성화
- 가상환경이 없으면 오류 메시지 표시
- 한글 완벽 지원
- **매번 새로운 터미널에서 봇을 실행할 때마다 실행**

### activate.ps1 (PowerShell용)
- cmd 버전과 동일한 기능
- PowerShell에서 한글이 깨지는 현상 자동 해결
- 색상 있는 출력으로 더 이쁜 UI 제공
- 한글 완벽 지원
- **매번 새로운 터미널에서 봇을 실행할 때마다 실행**

## Discord 봇 토큰 발급

1. [Discord Developers](https://discord.com/developers/applications)에 접속
2. "New Application" 클릭하여 새 애플리케이션 생성
3. "Bot" 탭에서 "Add Bot" 클릭
4. "TOKEN" 섹션의 "Copy" 버튼으로 토큰 복사
5. `.env` 파일의 `DISCORD_TOKEN`에 붙여넣기

## 기본 명령어

- `!ping` - 봇 응답 확인 (응답 시간 표시)
- `!hello` - 인사 메시지

## 개발 환경

- **Python 버전**: 3.8+
- **OS**: Windows (배치 파일 기반)
- **필수 설치**: Python 3.8 이상

## 자주 묻는 질문

### Q: PowerShell 실행 정책 오류가 나요?
```
스크립트 실행이 이 시스템에서 비활성화되어 있어서 ...
```

**A:** 다음 명령어 실행 후 다시 시도하세요:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: pip 업데이트 오류가 나요? (WinError 5, 액세스 거부)

**A:** 
- cmd 또는 PowerShell을 **관리자 권한**으로 실행해보세요
- 또는 스크립트가 자동으로 무시하고 패키지 설치를 진행합니다

### Q: PowerShell에서 한글이 깨져요?

**A:** 
- `setup_venv.ps1` 또는 `activate.ps1`를 사용하세요 (한글 자동 지원)
- 또는 cmd를 사용하세요

### Q: 어떤 방법을 사용해야 하나요?

**A:** 
- **PowerShell 권장** (색상, 한글 완벽 지원)
- cmd도 완벽하게 작동함

## 다음 단계

- Git 연동 기능 구현
- Discord 이벤트 핸들러 추가
- 커스텀 명령어 개발
- 데이터베이스 통합 (필요 시)

## 라이선스

MIT License

## 기여

프로젝트에 기여하고 싶으신 경우 Pull Request를 보내주세요.
