"""
Git 헬퍼 모듈

GitPython을 래핑하여 Git 명령을 처리합니다.
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from git import Repo, InvalidGitRepositoryError, GitCommandError

logger = logging.getLogger(__name__)

class GitHelper:
    """Git 작업 헬퍼 클래스"""
    
    def __init__(self, repo_path: str):
        """
        초기화
        
        Args:
            repo_path: Git 저장소 경로
        """
        self.repo_path = Path(repo_path)
        self.repo: Optional[Repo] = None
        self._init_repo()
    
    def _init_repo(self) -> None:
        """저장소 초기화"""
        try:
            self.repo = Repo(self.repo_path)
            logger.info(f"저장소 로드: {self.repo_path}")
        except InvalidGitRepositoryError:
            logger.error(f"유효한 Git 저장소가 아닙니다: {self.repo_path}")
            raise
    
    def get_status(self) -> str:
        """현재 상태 조회"""
        if not self.repo:
            return "저장소 없음"
        
        try:
            status = self.repo.git.status()
            return status
        except GitCommandError as e:
            logger.error(f"상태 조회 실패: {e}")
            return f"오류: {e}"
    
    def get_log(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        커밋 로그 조회
        
        Args:
            n: 조회할 커밋 수
        
        Returns:
            커밋 정보 리스트
        """
        if not self.repo:
            return []
        
        try:
            commits = []
            for commit in self.repo.iter_commits(max_count=n):
                commits.append({
                    'hash': commit.hexsha[:7],
                    'author': commit.author.name,
                    'message': commit.message.strip(),
                    'date': commit.committed_datetime.isoformat(),
                })
            return commits
        except GitCommandError as e:
            logger.error(f"로그 조회 실패: {e}")
            return []
    
    def get_branches(self) -> List[str]:
        """브랜치 목록 조회"""
        if not self.repo:
            return []
        
        try:
            branches = [head.name for head in self.repo.heads]
            return branches
        except GitCommandError as e:
            logger.error(f"브랜치 조회 실패: {e}")
            return []
    
    def get_current_branch(self) -> str:
        """현재 브랜치명 조회"""
        if not self.repo:
            return "unknown"
        
        try:
            return self.repo.active_branch.name
        except Exception as e:
            logger.error(f"현재 브랜치 조회 실패: {e}")
            return "unknown"
    
    def pull(self) -> str:
        """저장소 동기화"""
        if not self.repo:
            return "저장소 없음"
        
        try:
            origin = self.repo.remote(name='origin')
            origin.pull()
            return "✅ Pull 완료"
        except GitCommandError as e:
            logger.error(f"Pull 실패: {e}")
            return f"❌ Pull 실패: {e}"
