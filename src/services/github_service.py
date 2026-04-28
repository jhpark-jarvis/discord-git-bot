"""
GitHub 서비스 모듈

GitHub API의 비즈니스 로직을 처리합니다.
"""

import logging
from typing import Optional, Dict, Any, List
from ..utils.github_api import GithubAPI
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class GithubService:
    """GitHub 서비스 클래스"""
    
    def __init__(self, token: str):
        """
        초기화
        
        Args:
            token: GitHub Personal Access Token
        """
        self.github_api = GithubAPI(token)
    
    async def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """저장소 정보 조회"""
        info = await self.github_api.get_repo_info(owner, repo)
        
        if not info:
            return {"error": "저장소 정보를 조회할 수 없습니다"}
        
        return {
            "name": info.get("full_name"),
            "description": info.get("description"),
            "stars": info.get("stargazers_count"),
            "forks": info.get("forks_count"),
            "open_issues": info.get("open_issues_count"),
            "url": info.get("html_url"),
        }
    
    async def get_issues_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """오픈 이슈 정보 조회"""
        issues = await self.github_api.get_open_issues(owner, repo)
        
        return {
            "count": len(issues),
            "issues": [
                {
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "author": issue.get("user", {}).get("login"),
                    "url": issue.get("html_url"),
                }
                for issue in issues[:5]  # 최대 5개만
            ]
        }
    
    async def get_prs_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """오픈 PR 정보 조회"""
        prs = await self.github_api.get_open_prs(owner, repo)
        
        return {
            "count": len(prs),
            "prs": [
                {
                    "number": pr.get("number"),
                    "title": pr.get("title"),
                    "author": pr.get("user", {}).get("login"),
                    "url": pr.get("html_url"),
                }
                for pr in prs[:5]  # 최대 5개만
            ]
        }
    
    async def get_user_repositories(self, username: str) -> Dict[str, Any]:
        """사용자의 모든 저장소 조회"""
        repos = await self.github_api.get_user_repos(username)
        
        if not repos:
            return {"error": "저장소를 조회할 수 없습니다", "repositories": []}
        
        return {
            "count": len(repos),
            "repositories": [
                {
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "description": repo.get("description") or "설명 없음",
                    "stars": repo.get("stargazers_count"),
                    "language": repo.get("language") or "N/A",
                    "url": repo.get("html_url"),
                }
                for repo in repos[:20]  # 최대 20개만
            ]
        }
    
    async def search_user_repositories(self, username: str, keyword: str) -> Dict[str, Any]:
        """사용자의 저장소에서 검색"""
        results = await self.github_api.search_repos(username, keyword)
        
        if not results:
            return {"error": "검색 결과가 없습니다", "results": []}
        
        return {
            "count": len(results),
            "results": [
                {
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "description": repo.get("description") or "설명 없음",
                    "stars": repo.get("stargazers_count"),
                    "language": repo.get("language") or "N/A",
                    "url": repo.get("html_url"),
                }
                for repo in results[:15]  # 최대 15개만
            ]
        }
