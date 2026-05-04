"""
Git 서비스 모듈

Git 작업의 비즈니스 로직을 처리합니다.
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path
from git import Repo, GitCommandError
from ..utils.git_helper import GitHelper
from ..utils.logger import setup_logger
from ..config import GITHUB_TOKEN

logger = setup_logger(__name__)

class GitService:
    """Git 서비스 클래스"""
    
    def __init__(self, repo_path: str, github_repo: Optional[str] = None):
        """
        초기화
        
        Args:
            repo_path: Git 저장소 경로
            github_repo: GitHub 저장소명 (owner/repo 형식)
        """
        self.repo_path = Path(repo_path)
        self.github_repo = github_repo
        self.git_helper = None
        self._init_or_clone_repo()
    
    def _init_or_clone_repo(self) -> None:
        """저장소 초기화 또는 clone"""
        try:
            # 저장소가 이미 존재하면 로드
            if self.repo_path.exists() and (self.repo_path / ".git").exists():
                logger.info(f"기존 저장소 로드: {self.repo_path}")
                self.git_helper = GitHelper(str(self.repo_path))
                return
            
            # 저장소가 없으면 clone
            if self.github_repo:
                self._clone_repository()
                self.git_helper = GitHelper(str(self.repo_path))
            else:
                logger.error("저장소를 찾을 수 없고, GitHub 저장소명이 없습니다.")
                raise Exception("저장소를 사용할 수 없습니다")
        except Exception as e:
            logger.error(f"Git 서비스 초기화 실패: {e}")
            self.git_helper = None
    
    def _clone_repository(self) -> None:
        """GitHub에서 저장소 clone"""
        try:
            # 부모 디렉토리 생성
            self.repo_path.parent.mkdir(parents=True, exist_ok=True)
            
            # clone URL 생성
            if GITHUB_TOKEN:
                clone_url = f"https://{GITHUB_TOKEN}@github.com/{self.github_repo}.git"
            else:
                clone_url = f"https://github.com/{self.github_repo}.git"
            
            logger.info(f"저장소 clone 중: {self.github_repo} → {self.repo_path}")
            Repo.clone_from(clone_url, self.repo_path)
            logger.info(f"저장소 clone 완료: {self.repo_path}")
        except GitCommandError as e:
            logger.error(f"Clone 실패: {e}")
            raise
        except Exception as e:
            logger.error(f"Clone 중 오류: {e}")
            raise
    
    def get_status_info(self) -> Dict[str, Any]:
        """저장소 상태 정보 조회"""
        if not self.git_helper:
            return {"error": "저장소를 사용할 수 없습니다"}
        
        return {
            "branch": self.git_helper.get_current_branch(),
            "status": self.git_helper.get_status(),
        }
    
    def get_recent_commits(self, n: int = 5) -> Dict[str, Any]:
        """최근 커밋 조회"""
        if not self.git_helper:
            return {"error": "저장소를 사용할 수 없습니다", "commits": []}
        
        commits = self.git_helper.get_log(n)
        return {"commits": commits}
    
    def get_branches_info(self) -> Dict[str, Any]:
        """브랜치 정보 조회"""
        if not self.git_helper:
            return {"error": "저장소를 사용할 수 없습니다", "branches": []}
        
        branches = self.git_helper.get_branches()
        current = self.git_helper.get_current_branch()
        
        return {
            "branches": branches,
            "current_branch": current,
        }
    
    def sync_repository(self) -> Dict[str, Any]:
        """저장소 동기화"""
        if not self.git_helper:
            return {"error": "저장소를 사용할 수 없습니다"}
        
        result = self.git_helper.pull()
        return {"result": result}
