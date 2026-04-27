## 🔗 GitHub 웹훅 설정 가이드

GitHub 저장소의 이벤트를 Discord 채널로 자동 알림받을 수 있습니다.

---

## 📋 웹훅이란?

GitHub 저장소의 특정 이벤트 (Push, PR, Issues 등)가 발생하면 설정된 URL로 HTTP 요청을 보냅니다.

---

## 🚀 웹훅 설정 단계

### 1️⃣ 봇 서버 준비

**현재 상태:** 웹훅 수신 기능은 **개발 중**입니다.

웹훅을 완전히 지원하려면:
- 웹훅 수신 서버 (aiohttp/Flask) 구현 필요
- 공개 IP 또는 터널 (ngrok) 필요
- Docker/클라우드 배포 권장

### 2️⃣ GitHub 웹훅 설정

GitHub 저장소 설정에서 웹훅을 설정할 수 있습니다:

1. GitHub 저장소 → Settings → Webhooks
2. "Add webhook" 클릭
3. 다음 정보 입력:
   - **Payload URL**: `https://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: 강력한 시크릿 문자열 (최소 8자)
4. **Events 선택:**
   - ✅ Push events
   - ✅ Pull requests
   - ✅ Issues
   - ✅ Releases
   - (선택) 기타 이벤트
5. "Add webhook" 클릭

---

## 🔧 환경변수 설정

**config/.env:**
```env
# 웹훅 설정
WEBHOOK_PORT=8080
WEBHOOK_SECRET=your_webhook_secret_string_here
DISCORD_CHANNEL_ID=1234567890  # GitHub 이벤트를 받을 채널 ID
```

---

## 📚 웹훅 이벤트 종류

### Push 이벤트
저장소에 커밋이 푸시될 때:
```
[repository] Push
작성자: username
브랜치: main
커밋: 5개
```

### Pull Request 이벤트
PR이 생성/수정/병합될 때:
```
[repository] PR 열림
#123: New Feature
작성자: username
```

### Issues 이벤트
이슈가 생성/업데이트/해결될 때:
```
[repository] Issue 열림
#456: Bug Report
작성자: username
```

### Release 이벤트
새 릴리스가 배포될 때:
```
[repository] Release 발행
v1.0.0: Initial Release
작성자: username
```

---

## 🌐 배포 옵션

### 옵션 1: ngrok (테스트용)

```bash
# ngrok 다운로드: https://ngrok.com/download

# ngrok 실행
ngrok http 8080

# 표시된 URL을 GitHub 웹훅에 사용
# 예: https://xxxx-xxx-xxxx.ngrok.io/webhook
```

### 옵션 2: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "-m", "src.main"]
```

```bash
docker build -t discord-git-bot .
docker run -e DISCORD_TOKEN=xxx -e GITHUB_TOKEN=yyy -p 8080:8080 discord-git-bot
```

### 옵션 3: 클라우드 배포

- **Heroku** (무료 요금제 종료됨)
- **Railway**: https://railway.app/
- **Fly.io**: https://fly.io/
- **AWS EC2**: https://aws.amazon.com/

---

## 🔐 보안 권장사항

1. **시크릿 보호**
   - GitHub 웹훅 시크릿을 `.env`에만 저장
   - 절대 소스 코드에 커밋하지 말 것

2. **HTTPS 사용**
   - 웹훅은 HTTPS URL 권장
   - HTTP는 보안 위험

3. **시크릿 검증**
   - 봇이 GitHub 시크릿 서명 검증 수행
   - 위조된 요청으로부터 보호

4. **로깅**
   - 모든 웹훅 요청 로깅
   - `logs/bot.log` 확인

---

## 🧪 웹훅 테스트

### GitHub에서 테스트 전송
1. GitHub 저장소 → Settings → Webhooks
2. 웹훅 선택 → "Recent Deliveries" 탭
3. 최근 요청 선택 → "Redeliver" 클릭

### 로그 확인
```bash
tail -f logs/bot.log
```

웹훅 수신 로그를 확인합니다.

---

## 📝 웹훅 페이로드 예시

### Push 이벤트
```json
{
  "ref": "refs/heads/main",
  "before": "abc123...",
  "after": "def456...",
  "repository": {
    "id": 123456,
    "name": "repository",
    "full_name": "owner/repository"
  },
  "pusher": {
    "name": "username",
    "email": "user@example.com"
  },
  "commits": [
    {
      "id": "def456...",
      "message": "Update README",
      "author": {"name": "username", "email": "user@example.com"}
    }
  ]
}
```

---

## 🚀 커밍 soon!

- [ ] 웹훅 수신 서버 완전 구현
- [ ] 웹훅 자동 설정 스크립트
- [ ] 웹훅 관리 커맨드 (enable/disable)
- [ ] 이벤트별 커스텀 메시지 포매팅
- [ ] 다중 채널 라우팅

---

## 📞 문제 해결

### 웹훅이 전달되지 않음
1. GitHub 저장소 → Settings → Webhooks → Recent Deliveries 확인
2. HTTP 상태 코드 확인 (200 OK가 아니면 오류)
3. 봇 로그 확인: `tail logs/bot.log`

### 보안 오류
```
❌ 웹훅 서명 검증 실패
```
- GitHub 웹훅 시크릿 확인
- config/.env WEBHOOK_SECRET 확인

