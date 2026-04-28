# Discord-Git Bot 개선 계획

## 📌 프로젝트 비전
**Discord 서버에서 Git/GitHub 저장소를 관리하는 통합 봇**

Git 이벤트를 실시간으로 Discord 채널에 알림하고, Discord 채팅으로 Git 작업을 자동화하는 DevOps 도구

---

## 🎯 핵심 기능 아이디어

### 1️⃣ GitHub 웹훅 연동 (★★★ 우선순위 높음)
**설명**: GitHub 저장소의 이벤트를 Discord 채널로 자동 알림
- **Push 이벤트**: 커밋 메시지, 작성자, 파일 변경 사항 표시
- **Pull Request**: PR 생성/병합/닫힘 알림
- **Issues**: 이슈 생성/업데이트/해결 알림
- **Release**: 새 릴리스 배포 알림

### 2️⃣ Discord 커맨드로 Git 작업 (★★ 우선순위 중간)
**설명**: Discord 채팅에서 직접 Git 명령 실행
- `!git status` → 현재 저장소 상태 표시
- `!git log` → 최근 커밋 로그 조회
- `!git branch` → 브랜치 목록 표시
- `!git pull` → 저장소 동기화
- `!repo info` → 저장소 정보 조회

### 3️⃣ 자동 모니터링 및 알림 (★★ 우선순위 중간)
**설명**: 저장소 상태를 주기적으로 확인
- 테스트 실패 알림
- CI/CD 파이프라인 상태
- 빌드 실패/성공 알림
- 코드 리뷰 요청 알림

### 4️⃣ 협업 기능 (★ 우선순위 낮음)
**설명**: 팀 협업 효율화
- 커밋 기여도 통계
- 주간/월간 활동 리포트
- 팀 멤버별 작업 현황

---

## 🏗️ 프로젝트 구조

```
discord-git-bot/
│
├── src/                               # 메인 소스코드
│   ├── main.py                       # 봇 진입점
│   ├── config.py                     # 봇 설정 (토큰, 설정값)
│   │
│   ├── cogs/                         # 기능 모듈 (Commands)
│   │   ├── __init__.py
│   │   ├── git_commands.py          # Git 커맨드 (!git ...)
│   │   ├── repo_commands.py         # 저장소 커맨드 (!repo ...)
│   │   └── admin_commands.py        # 관리자 커맨드 (!admin ...)
│   │
│   ├── handlers/                     # 이벤트 핸들러
│   │   ├── __init__.py
│   │   ├── github_webhook.py        # GitHub 웹훅 처리
│   │   └── github_events.py         # GitHub 이벤트 파서
│   │
│   ├── utils/                        # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── git_helper.py            # Git 명령 래퍼
│   │   ├── github_api.py            # GitHub REST API
│   │   ├── logger.py                # 로깅 설정
│   │   ├── validators.py            # 입력값 검증
│   │   └── embedders.py             # Discord Embed 생성
│   │
│   └── services/                     # 비즈니스 로직
│       ├── __init__.py
│       ├── git_service.py           # Git 작업 로직
│       └── github_service.py        # GitHub API 호출 로직
│
├── config/
│   ├── .env.example                 # 환경변수 예제
│   ├── .env                         # 실제 환경변수 (git 무시)
│   └── webhooks/                    # 웹훅 설정
│       └── github_webhook.json      # GitHub 웹훅 설정 예제
│
├── scripts/                          # 유틸리티 스크립트
│   ├── test_send_message.py         # 메시지 테스트 (기존)
│   ├── setup_webhook.py             # GitHub 웹훅 자동 설정
│   └── setup_venv.*                 # 가상환경 (기존)
│
├── tests/                            # 테스트 코드
│   ├── __init__.py
│   ├── test_git_commands.py         # Git 커맨드 테스트
│   ├── test_webhook.py              # 웹훅 처리 테스트
│   └── fixtures/                    # 테스트 데이터
│       └── github_webhook_payload.json
│
├── docs/                             # 문서
│   ├── SETUP.md                     # 설치 가이드
│   ├── COMMANDS.md                  # 커맨드 문서
│   ├── WEBHOOK_SETUP.md             # 웹훅 설정 가이드
│   └── API.md                       # API 문서
│
├── requirements.txt                 # Python 의존성
├── .gitignore                       # Git 무시 파일
├── .env                             # 환경변수 (git 무시)
├── README.md                        # 프로젝트 소개 (기존)
├── PLAN.md                          # 이 파일
└── CHANGELOG.md                     # 변경 사항 기록
```

---

## 📋 개발 로드맵

### Phase 1: 기초 인프라 구축 (1-2주)
- [ ] 프로젝트 구조 리팩토링
- [ ] Cogs 시스템 구현
- [ ] 설정 관리 (config.py)
- [ ] 로깅 설정
- [ ] 기본 에러 핸들링

### Phase 2: GitHub 웹훅 연동 (2-3주)
- [ ] 웹훅 엔드포인트 구현 (Flask/aiohttp)
- [ ] GitHub 이벤트 파서
- [ ] Discord Embed 포매팅
- [ ] 웹훅 자동 설정 스크립트
- [ ] 테스트 코드 작성

### Phase 3: Discord 커맨드 구현 (2-3주)
- [ ] Git 커맨드 Cog
- [ ] 저장소 정보 조회 Cog
- [ ] 권한 관리 (admin only)
- [ ] 커맨드 헬프 시스템
- [ ] 테스트 코드 작성

### Phase 4: 모니터링 및 고급 기능 (2-3주)
- [ ] 주기적 상태 체크
- [ ] 성능 최적화
- [ ] 데이터베이스 통합 (선택)
- [ ] 통계 기능

### Phase 5: 배포 및 최적화 (1-2주)
- [ ] Docker 지원
- [ ] CI/CD 파이프라인
- [ ] 문서 작성
- [ ] 배포 가이드

---

## 🔧 기술 스택

| 영역 | 도구 | 버전 |
|------|------|------|
| **Discord** | discord.py | >=2.0.0 |
| **Git** | GitPython | >=3.1.0 |
| **GitHub API** | PyGithub 또는 aiohttp | 최신 |
| **웹훅** | aiohttp 또는 Flask | >=3.8.0 |
| **환경변수** | python-dotenv | >=0.19.0 |
| **로깅** | logging (표준) | - |
| **테스트** | pytest | >=7.0.0 |

---

## ⚙️ 필수 환경변수 (.env)

```env
# Discord
DISCORD_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=1234567890

# GitHub
GITHUB_TOKEN=github_personal_access_token
GITHUB_REPO=username/repository
GITHUB_REPO_PATH=./repositories/

# 웹훅 (선택)
WEBHOOK_PORT=8080
WEBHOOK_SECRET=your_webhook_secret

# 로깅
LOG_LEVEL=INFO
```

---

## 🎨 기능별 커맨드 예시

### Git 커맨드
```
!git status          # 저장소 상태
!git log -5          # 최근 5개 커밋
!git branch          # 브랜치 목록
!git pull            # 저장소 동기화
!git diff main..dev  # 브랜치 비교
```

### 저장소 커맨드
```
!repo info           # 저장소 정보
!repo stats          # 커밋 통계
!repo contributors   # 기여자 목록
!repo issues         # 오픈 이슈
!repo prs            # 오픈 PR
```

### 관리자 커맨드
```
!admin webhook sync  # 웹훅 동기화
!admin config show   # 설정 조회
!admin logs          # 봇 로그 조회
```

---

## 🚀 다음 단계

1. **PLAN.md 검토** ✅
2. **프로젝트 구조 생성** → 다음 작업
3. **Phase 1 시작**: 기초 인프라 구축

---

**최종 목표**: DevOps팀과 개발자들이 Discord에서 효율적으로 Git/GitHub를 관리하는 통합 도구
