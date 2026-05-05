## 커맨드 문서

이 문서는 Discord-Git Bot의 모든 커맨드를 설명합니다.

### 기본 커맨드

#### !ping
봇이 응답하는지 확인하고 응답 시간을 표시합니다.

```
!ping
```

**응답:**
```
Pong!
응답 시간: 45ms
```

---

### Git 커맨드 (!git)

Git 저장소 관련 작업을 수행합니다.

#### !git status
현재 저장소의 상태를 조회합니다.

```
!git status
```

#### !git log [n]
최근 커밋 로그를 조회합니다.

```
!git log          최근 5개 커밋 (기본값)
!git log 10       최근 10개 커밋
```

#### !git branch
현재 사용 가능한 브랜치 목록을 표시합니다.

```
!git branch
```

**응답:**
```
브랜치 목록
→ main
  develop
  feature/new-feature
```

#### !git pull
저장소를 동기화합니다.

```
!git pull
```

---

### 저장소 커맨드 (!repo)

GitHub 저장소 정보를 조회합니다.

#### !repo info
저장소 기본 정보를 표시합니다.

```
!repo info
```

**응답:**
```
owner/repository

설명: 프로젝트 설명

Stars: 42
Forks: 8
Issues: 3
URL: https://github.com/owner/repository
```

#### !repo issues
현재 오픈된 이슈 목록을 표시합니다.

```
!repo issues
```

#### !repo prs
현재 오픈된 Pull Request 목록을 표시합니다.

```
!repo prs
```

---

### 테스트 커맨드 (!test)

테스트를 실행하고 결과를 확인합니다. (관리자만 사용 가능)

#### !test all
모든 테스트 (유닛 + 통합)를 실행합니다.

```
!test all
```

**응답:**
- 테스트 시작 메시지 (진행 중)
- 테스트 완료 메시지 (결과: 통과/실패 개수)
- 상세 출력 (텍스트 또는 파일)

#### !test unit
유닛 테스트만 실행합니다.

```
!test unit
```

#### !test integration
통합 테스트만 실행합니다.

```
!test integration
```

#### !test git_commands
Git 커맨드 테스트만 실행합니다.

```
!test git_commands
```

#### !test git_helper
Git Helper 테스트만 실행합니다.

```
!test git_helper
```

#### !test git_service
Git Service 테스트만 실행합니다.

```
!test git_service
```

#### !test integration_git
Git 통합 테스트만 실행합니다.

```
!test integration_git
```

**주의사항:**
- 테스트 실행 중에는 다른 테스트를 동시에 실행할 수 없습니다.
- 테스트 실행 시간은 테스트 종류와 개수에 따라 다릅니다 (일반적으로 1-3초).
- 테스트 출력이 길면 파일로 전송됩니다.

---

### 관리자 커맨드 (!admin)

**필수 권한:** 관리자

#### !admin config
봇의 설정 정보를 확인합니다.

```
!admin config
```

#### !admin ping
봇 핑 테스트를 실행합니다.

```
!admin ping
```

---

## 💡 사용 팁

1. **커맨드 도움말**: `!git`, `!repo`, `!admin` 입력 시 해당 그룹의 모든 커맨드를 확인할 수 있습니다.

2. **에러 처리**: 커맨드 실행 중 에러가 발생하면 에러 메시지가 표시됩니다.

3. **권한 확인**: 관리자 커맨드는 관리자 권한이 필요합니다.

---

## 🚀 커밍 soon!

- `!git diff` - 브랜치 비교
- `!git commit` - 커밋 생성
- `!repo stats` - 통계 정보
- `!repo contributors` - 기여자 목록
- GitHub 웹훅 자동 알림

