# Discord-Git Bot

Discord 서버에서 Git/GitHub 저장소를 관리하는 통합 봇입니다.

## 주요 기능

- **Git 커맨드**: Discord에서 Git 작업 수행
  - 저장소 상태, 커밋 로그, 브랜치 관리, 저장소 동기화
  
- **GitHub 저장소 자동 관리**: GITHUB_REPO 기반 자동 clone
  - GitHub 저장소에서 자동으로 clone하여 관리
  - 로컬 저장소 자동 생성 및 유지
  
- **GitHub 정보 조회**: 저장소 정보 및 이슈 확인
  - 저장소 상세 정보, 오픈 이슈, PR 목록
  
- **웹훅 알림**: 저장소 이벤트 자동 알림 (준비 중)
  - Push, PR, Issues, Releases 알림
  
- **관리자 기능**: 봇 설정 및 관리
  - 설정 확인, 핑 테스트

## 빠른 시작

### 사전 요구사항

- Python 3.10 이상
- Git
- Discord 서버 (관리자 권한)
- GitHub 계정

### 1단계: 설정

```bash
# .env 파일 생성
cp config\.env.example config\.env

# 편집: DISCORD_TOKEN과 GITHUB_TOKEN 입력
```

자세한 설정 방법: [SETUP.md](docs/SETUP.md)

### 2단계: 설치

```bash
# 의존성 설치
pip install -r requirements.txt
```

### 3단계: 실행

```bash
python -m src.main
```

## 커맨드

### Git 커맨드 (`!git`)

```
!git status          저장소 상태 확인
!git log [n]         최근 n개 커밋 조회 (기본: 5)
!git branch          브랜치 목록 표시
!git pull            저장소 동기화
```

### 저장소 커맨드 (`!repo`)

```
!repo info           저장소 정보 조회
!repo issues         오픈 이슈 목록
!repo prs            오픈 PR 목록
```

### 기본 커맨드

```
!ping                봇 응답 확인
```

더 많은 커맨드: [COMMANDS.md](docs/COMMANDS.md)

## 프로젝트 구조

```
discord-git-bot/
├── src/
│   ├── main.py               봇 진입점
│   ├── config.py             설정 관리
│   ├── cogs/
│   │   ├── git_commands.py   Git 관련 커맨드
│   │   ├── repo_commands.py  저장소 관련 커맨드
│   │   └── admin_commands.py 관리자 커맨드
│   ├── handlers/             이벤트 핸들러
│   ├── utils/                유틸리티
│   │   ├── git_helper.py     Git 래퍼
│   │   ├── github_api.py     GitHub API 클라이언트
│   │   ├── logger.py         로깅
│   │   ├── validators.py     검증
│   │   └── embedders.py      Embed 생성
│   └── services/             비즈니스 로직
│       ├── git_service.py    Git 서비스
│       └── github_service.py GitHub 서비스
├── config/
│   ├── .env                  환경변수
│   └── .env.example          환경변수 예제
├── repositories/             자동 clone된 저장소 (GITHUB_REPO 기반)
├── scripts/
│   ├── send_test_results.py  테스트 결과 전송
│   ├── test_send_message.py  메시지 테스트
│   └── activate.*            가상환경 활성화
├── tests/                    테스트 코드
│   ├── test_git_commands.py
│   ├── test_git_helper.py
│   ├── test_git_service.py
│   ├── test_integration_git.py
│   ├── conftest.py
│   └── fixtures/
├── docs/
│   ├── SETUP.md              설치 가이드
│   ├── COMMANDS.md           커맨드 문서
│   └── WEBHOOK_SETUP.md      웹훅 설정
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── PLAN.md
└── STATUS.md
```

## 🔧 설치 가이드

### Windows (PowerShell)

```powershell
# 1. 가상환경 생성
.\scripts\setup_venv.ps1

# 2. 가상환경 활성화
.\scripts\activate.ps1

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 설정
cp config\.env.example config\.env
# config/.env 파일 편집

# 5. 실행
python -m src.main
```

### Windows (Command Prompt)

```cmd
# 1. 가상환경 생성
scripts\setup_venv.bat

# 2. 가상환경 활성화
scripts\activate.bat

# 3. 이후는 위와 동일
```

### 상세 설정 가이드

더 자세한 설정 방법은 [docs/SETUP.md](docs/SETUP.md) 참고

## 🔐 환경변수 설정

**config/.env** (필수):

```env
# Discord 토큰 (필수)
DISCORD_TOKEN=your_token_here

# GitHub 토큰 (필수)
GITHUB_TOKEN=your_token_here

# GitHub 저장소 (필수, owner/repo 형식)
GITHUB_REPO=username/repository

# 커맨드 프리픽스 (선택, 기본값: !)
COMMAND_PREFIX=!

# 로그 레벨 (선택, 기본값: INFO)
LOG_LEVEL=INFO
```

토큰 발급 방법:
- **Discord 토큰**: [Discord Developer Portal](https://discord.com/developers/applications/)
- **GitHub 토큰**: [GitHub Settings - Tokens](https://github.com/settings/tokens)

## 📚 문서

| 문서 | 설명 |
|------|------|
| [SETUP.md](docs/SETUP.md) | Discord/GitHub 설정 및 설치 가이드 |
| [COMMANDS.md](docs/COMMANDS.md) | 모든 커맨드 상세 설명 |
| [WEBHOOK_SETUP.md](docs/WEBHOOK_SETUP.md) | GitHub 웹훅 설정 (개발 중) |
| [PLAN.md](PLAN.md) | 프로젝트 비전 및 로드맵 |
| [CHANGELOG.md](CHANGELOG.md) | 버전별 변경 사항 |

## 🔄 개발 로드맵

### Phase 1: 기초 인프라 ✅
- [x] 프로젝트 구조 설계
- [x] Cogs 시스템 구현
- [x] Git 커맨드 구현
- [x] 저장소 커맨드 구현

### Phase 2: 웹훅 연동 (진행 중)
- [ ] 웹훅 수신 서버
- [ ] GitHub 이벤트 알림
- [ ] 웹훅 자동 설정

### Phase 3: 고급 기능
- [ ] 통계 및 리포팅
- [ ] 데이터베이스 통합
- [ ] Docker 지원

## 🛠️ 기술 스택

- **Python 3.10+**
- **discord.py**: Discord 봇 API
- **GitPython**: Git 명령 실행
- **aiohttp**: 비동기 HTTP 클라이언트
- **PyGithub**: GitHub API
- **python-dotenv**: 환경변수 관리

## 🆘 문제 해결

### 토큰 오류
```
❌ 오류: 잘못된 Discord 토큰입니다.
```
→ Discord Developer Portal에서 토큰 재확인

### Privileged Intents 오류
```
❌ PrivilegedIntentsRequired
```
→ Discord Developer Portal → Bot → Privileged Gateway Intents 활성화

### 저장소를 찾을 수 없음
```
❌ 저장소를 사용할 수 없습니다
```
→ GIT_REPO_PATH가 올바른지, 유효한 Git 저장소인지 확인

더 많은 도움: [docs/SETUP.md - 문제 해결](docs/SETUP.md#-문제-해결)

## 📝 테스트

```bash
# 메시지 테스트 스크립트
python scripts/test_send_message.py <channel_id> "테스트 메시지"
```

## 📞 지원

문제가 발생하면:

1. [문제 해결 가이드](docs/SETUP.md#-문제-해결) 확인
2. 로그 파일 확인: `logs/bot.log`
3. GitHub Issues 등록

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

## 👨‍💻 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

---

**현재 상태**: 개발 중 (v1.0.0)

최종 업데이트: 2026-04-27
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

## Plan

- Git 연동 기능 구현
- Discord 이벤트 핸들러 추가
- 커스텀 명령어 개발
- 데이터베이스 통합 (필요 시)
