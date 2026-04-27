## 설정 및 설치 가이드

Discord-Git Bot을 설정하고 실행하는 방법입니다.

### 필수 요구사항

- Python 3.10 이상
- Git
- Discord 서버 (관리자 권한)
- GitHub 계정

---

## 1. Discord 봇 생성

### 1. Discord Developer Portal 방문
[Discord Developer Portal](https://discord.com/developers/applications/) 접속

### 2. 새 애플리케이션 생성
- "New Application" 클릭
- 봇 이름 입력 후 생성

### 3. Bot 생성
- 왼쪽 메뉴에서 "Bot" 클릭
- "Add Bot" 버튼 클릭

### 4. 토큰 복사
- "Reset Token" 클릭
- **TOKEN 복사 (절대 공유 금지!)**

### 5. Privileged Gateway Intents 활성화
- "Privileged Gateway Intents" 섹션으로 스크롤
- 다음 항목 활성화:
  - ✅ **Message Content Intent**
  - (선택) ✅ **Server Members Intent**
  - (선택) ✅ **Presence Intent**
- "Save Changes" 클릭

### 6. OAuth2 권한 설정
- 왼쪽 메뉴에서 "OAuth2" → "URL Generator" 클릭
- **Scopes 선택:**
  - ✅ bot
- **Permissions 선택:**
  - ✅ Send Messages
  - ✅ Embed Links
  - ✅ Read Messages/View Channels
  - ✅ Read Message History
- 생성된 URL 복사 후 브라우저에서 열어 봇을 서버에 초대

---

## 2. GitHub 설정

### 1. Personal Access Token 생성
- GitHub 우측 상단 프로필 → "Settings"
- 왼쪽 메뉴 → "Developer settings" → "Personal access tokens"
- "Generate new token (classic)" 클릭
- **Scopes 선택:**
  - ✅ repo (모든 레포지토리 접근)
  - ✅ read:user (사용자 정보)
- 토큰 복사 (절대 공유 금지!)

---

## 3. 로컬 설정

### 1. 저장소 클론
```bash
git clone <your-discord-git-bot-repo>
cd discord-git-bot
```

### 2. 가상환경 생성 (선택 - 권장)

**Windows (PowerShell):**
```powershell
.\scripts\setup_venv.ps1
.\scripts\activate.ps1
```

**Windows (cmd):**
```cmd
scripts\setup_venv.bat
scripts\activate.bat
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
```bash
# .env 파일 생성
cp config\.env.example config\.env
```

**config/.env 파일 편집:**
```env
# Discord
DISCORD_TOKEN=your_discord_token_here
COMMAND_PREFIX=!

# GitHub
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=username/repository

# Logging
LOG_LEVEL=INFO
```

---

## 4. 봇 실행

### 방법 1: 직접 실행
```bash
python -m src.main
```

### 방법 2: 테스트 메시지 전송
```bash
# 기본 메시지 전송
python scripts/test_send_message.py <channel_id>

# 커스텀 메시지 전송
python scripts/test_send_message.py <channel_id> "테스트 메시지"
```

**채널 ID 얻는 방법:**
1. Discord 개발자 모드 활성화 (사용자 설정 → 개발자 옵션)
2. 채널 우클릭 → "채널 ID 복사"

---

## Git 저장소 설정

### 로컬 저장소 추가 (선택)

```bash
# 저장소 디렉토리 생성
mkdir repositories
cd repositories

# 저장소 클론
git clone <your-git-repo>
```

**config/.env 수정:**
```env
GIT_REPO_PATH=./repositories/<repository-name>
```

---

## 설정 확인

```bash
# 봇 실행 후 Discord에서
!admin config
```

모든 설정이 올바르게 되었는지 확인합니다.

---

## 문제 해결

### 토큰 오류
```
❌ 오류: 잘못된 Discord 토큰입니다.
```
- Discord Developer Portal에서 토큰 재확인
- 토큰이 정확히 복사되었는지 확인

### Privileged Intents 오류
```
❌ 오류: PrivilegedIntentsRequired
```
- Discord Developer Portal → Bot → Privileged Gateway Intents 활성화

### 저장소를 찾을 수 없음
```
❌ 저장소를 사용할 수 없습니다
```
- `GIT_REPO_PATH`가 올바른지 확인
- 디렉토리가 유효한 Git 저장소인지 확인

---

