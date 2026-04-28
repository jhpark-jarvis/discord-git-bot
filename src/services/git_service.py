"""
Git 서비스 모듈

Git 작업의 비즈니스 로직을 처리합니다.
"""

import logging
from typing import Optional, Dict, Any
from ..utils.git_helper import GitHelper
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class GitService:
    """Git 서비스 클래스"""
    
    def __init__(self, repo_path: str):
        """
        초기화
        
        Args:
            repo_path: Git 저장소 경로
        """
        try:
            self.git_helper = GitHelper(repo_path)
        except Exception as e:
            logger.error(f"Git 서비스 초기화 실패: {e}")
            self.git_helper = None
    
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
