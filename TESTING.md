# Discord Git Bot - 테스트 가이드

## 테스트 구조

이 프로젝트는 유닛테스트와 통합테스트로 구성되어 있습니다.

### 테스트 파일 설명

- **test_git_helper.py**: GitHelper 클래스의 유닛테스트
  - Git 저장소 초기화
  - 상태 조회 (get_status)
  - 커밋 로그 조회 (get_log)
  - 브랜치 목록 조회 (get_branches)
  - 현재 브랜치 조회 (get_current_branch)
  - 저장소 동기화 (pull)

- **test_git_service.py**: GitService 클래스의 유닛테스트
  - 서비스 초기화
  - 저장소 상태 정보 조회
  - 최근 커밋 조회
  - 브랜치 정보 조회
  - 저장소 동기화

- **test_git_commands.py**: GitCommands Cog의 유닛테스트
  - Cog 초기화
  - !git status 명령
  - !git log [n] 명령
  - !git branch 명령
  - !git pull 명령
  - 에러 처리

- **test_integration_git.py**: 통합 테스트
  - GitHelper 전체 워크플로우
  - GitService 전체 워크플로우
  - GitCommands 전체 워크플로우
  - 에러 처리 워크플로우
  - 여러 명령어 순차 실행
  - 많은 커밋 목록 처리

### conftest.py

공통 설정 및 Fixtures:
- `mock_discord_context`: Mock Discord Context
- `mock_git_helper`: Mock GitHelper
- `mock_git_service`: Mock GitService
- `mock_bot`: Mock Discord Bot
- `sample_commits`: 샘플 커밋 데이터
- `sample_branches`: 샘플 브랜치 데이터

## 테스트 실행

### 모든 테스트 실행

```bash
pytest
```

### 특정 파일의 테스트만 실행

```bash
# GitHelper 테스트만
pytest tests/test_git_helper.py -v

# GitService 테스트만
pytest tests/test_git_service.py -v

# GitCommands 테스트만
pytest tests/test_git_commands.py -v

# 통합 테스트만
pytest tests/test_integration_git.py -v
```

### 특정 클래스의 테스트만 실행

```bash
pytest tests/test_git_helper.py::TestGitHelper -v
```

### 특정 테스트만 실행

```bash
pytest tests/test_git_helper.py::TestGitHelper::test_init_repo_success -v
```

### 상세 출력 옵션

```bash
# 매우 상세한 출력
pytest -vv

# 각 테스트의 실행 시간 표시
pytest -v --durations=10

# 커버리지 포함 (coverage 설치 필요)
pytest --cov=src --cov-report=html
```

### 마커를 이용한 실행

```bash
# 모든 async 테스트만 실행
pytest -m asyncio

# integration 마커가 있는 테스트만
pytest -m integration

# unit 테스트만
pytest -m unit
```

## 테스트 커버리지

테스트 커버리지를 확인하려면:

```bash
# coverage 설치
pip install coverage

# 커버리지 실행
pytest --cov=src --cov-report=html

# HTML 리포트 보기
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

## Mock 객체 사용

이 프로젝트의 테스트는 다음을 모킹(mock)합니다:

1. **Git 저장소** (`GitPython.Repo`)
   - 실제 Git 저장소에 접근하지 않음
   - 테스트 데이터로 동작 검증

2. **Discord Bot & Context**
   - 실제 Discord 봇과 연결되지 않음
   - 명령어 처리 로직만 테스트

3. **GitHelper, GitService**
   - 각 계층을 독립적으로 테스트
   - 의존성 주입으로 테스트 격리

## 예시: 새로운 테스트 작성

```python
import pytest
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_my_new_feature(mock_discord_context, mock_git_helper):
    """테스트 설명"""
    # Arrange: 테스트 데이터 설정
    mock_git_helper.get_status.return_value = "Test status"
    
    # Act: 테스트 대상 함수 실행
    result = mock_git_helper.get_status()
    
    # Assert: 결과 검증
    assert result == "Test status"
```

## 주요 테스트 시나리오

### 1. 성공 케이스
- 정상적인 Git 명령 실행
- 예상된 결과 반환
- 적절한 Discord 메시지 전송

### 2. 에러 케이스
- 저장소 없음
- Git 명령 실패
- 네트워크 오류
- 권한 오류

### 3. 경계값 테스트
- 최대 커밋 개수 제한 (20개)
- 빈 브랜치/커밋 목록
- 매우 긴 메시지 처리

### 4. 워크플로우 테스트
- 여러 명령어 순차 실행
- 상태 변화 추적
- 전체 기능 통합 동작

## 도움말

### pytest 치트시트

```bash
pytest          # 모든 테스트 실행
pytest -v       # 상세 출력
pytest -x       # 첫 실패에서 중단
pytest -k name  # 이름 필터
pytest --lf     # 마지막 실패 테스트만
pytest --ff     # 실패한 테스트 우선 실행
```

### 자주 하는 실수

1. **비동기 테스트에 @pytest.mark.asyncio 빠뜨림**
   - async def 테스트는 반드시 @pytest.mark.asyncio 필요

2. **Mock 설정 누락**
   - Mock 객체에서 필요한 메서드를 설정하지 않으면 AttributeError 발생

3. **fixture 이름 오타**
   - fixture 이름을 정확히 입력해야 자동 주입됨

## 문제 해결

### ImportError 발생
```bash
# 프로젝트 루트에서 실행해야 함
cd /path/to/discord-git-bot
pytest
```

### 비동기 테스트 실행 안됨
```bash
# pytest-asyncio 설치 확인
pip install pytest-asyncio
```

### Mock 객체 문제
```python
# from으로 import하는 부분을 patch해야 함
@patch('src.cogs.git_commands.GitService')  # O
# @patch('src.services.git_service.GitService')  # X
```
