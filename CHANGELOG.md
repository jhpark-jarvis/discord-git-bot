## 변경 사항 기록

모든 버전의 변경 사항을 기록합니다.

---

## [Unreleased]

### 개발 중 기능
- 웹훅 수신 서버 완전 구현
- 웹훅 자동 설정 스크립트
- 웹훅 관리 커맨드
- 추가 Git 커맨드 (diff, commit)
- GitHub 통계 기능
- 데이터베이스 통합
- Docker 지원

---

## [1.1.0] - 2026-05-04

### 추가됨
- GITHUB_REPO 기반 자동 저장소 관리
  - GitHub 저장소에서 자동 clone
  - 로컬 경로 자동 생성 (repositories/{owner}/{repo})
  - 저장소 없을 시 첫 실행 시 자동 clone

- 포괄적인 테스트 시스템
  - 41개 단위 및 통합 테스트
  - pytest 및 pytest-asyncio 기반
  - 모든 테스트 통과

- 명령어 실행 로깅
  - Console에 모든 명령어 기록
  - 사용자, 채널, 명령어, 결과 기록
  - [GIT COMMAND], [RESULT] 태그 사용

- 봇 활성화 알림
  - Discord 채널에 봇 시작 메시지
  - 저장소 정보 및 사용 가능한 명령어 표시
  - Embed 형식으로 전송

- 테스트 결과 전송 스크립트
  - send_test_results.py 추가
  - Discord 채널에 테스트 결과 메시지 전송
  - 카테고리별 테스트 결과 표시

### 개선됨
- GitService 초기화 방식
  - github_repo 매개변수 추가
  - 저장소 자동 clone 기능
  - 오류 처리 강화

- config.py
  - GITHUB_REPO에서 경로 자동 생성
  - owner/repo 파싱 로직 추가

---

## [1.0.0] - 2026-04-27

### 추가됨
- 모듈화된 프로젝트 구조
  - Cogs 시스템으로 기능 분리
  - utils, services, handlers 계층 분리

- Git 커맨드 그룹
  - !git status - 저장소 상태 조회
  - !git log [n] - 커밋 로그 조회
  - !git branch - 브랜치 목록
  - !git pull - 저장소 동기화

- 저장소 커맨드 그룹
  - !repo info - 저장소 정보
  - !repo issues - 오픈 이슈 목록
  - !repo prs - 오픈 PR 목록

- 관리자 커맨드 그룹
  - !admin config - 설정 확인
  - !admin ping - 핑 테스트

- 유틸리티 기능
  - GitPython 래퍼 (GitHelper)
  - GitHub REST API 클라이언트 (GithubAPI)
  - 로깅 시스템
  - 입력값 검증
  - Discord Embed 자동 생성

- 문서
  - SETUP.md - 설정 가이드
  - COMMANDS.md - 커맨드 문서
  - WEBHOOK_SETUP.md - 웹훅 설정 가이드
  - CHANGELOG.md - 변경 사항

- 개발 도구
  - test_send_message.py - 메시지 테스트 스크립트
  - 테스트 디렉토리 구조

### 개선됨
- 프로젝트 구조 전체 리팩토링
- 환경변수 관리 개선
- 에러 핸들링 강화
- 로깅 시스템 추가

### 고정됨
- .env 파일 경로 문제 해결
- Privileged Intents 오류 처리

---

## [0.1.0] - 초기 버전

### 추가됨
- 기본 Discord 봇 구조
- `!ping` 커맨드
- `!hello` 커맨드
- 기본 에러 핸들링

---

## 📌 버전 번호 규칙

MAJOR.MINOR.PATCH

- **MAJOR**: 주요 기능 추가 또는 호환성 깨지는 변경
- **MINOR**: 새 기능 추가 (호환성 유지)
- **PATCH**: 버그 수정

---

## 🔮 미래 계획

### v1.1.0
- [ ] 웹훅 기본 기능 구현
- [ ] 추가 Git 커맨드
- [ ] 성능 최적화

### v1.2.0
- [ ] 데이터베이스 통합
- [ ] 통계 기능
- [ ] 사용자 설정 저장

### v2.0.0
- [ ] Slash 커맨드 지원
- [ ] 버튼 인터랙션
- [ ] 고급 웹훅 필터링

