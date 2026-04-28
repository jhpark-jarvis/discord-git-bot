"""
GitHub API 모듈

GitHub REST API를 통해 저장소 정보를 조회합니다.
"""

import logging
from typing import Optional, List, Dict, Any
import aiohttp

logger = logging.getLogger(__name__)

class GithubAPI:
    """GitHub API 클라이언트"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str):
        """
        초기화
        
        Args:
            token: GitHub Personal Access Token
        """
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def get_repo_info(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """저장소 정보 조회"""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API 오류: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"요청 실패: {e}")
                return None
    
    async def get_open_issues(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """오픈 이슈 목록 조회"""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
        params = {"state": "open"}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API 오류: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"요청 실패: {e}")
                return []
    
    async def get_open_prs(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """오픈 Pull Request 목록 조회"""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls"
        params = {"state": "open"}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API 오류: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"요청 실패: {e}")
                return []
    
    async def get_user_repos(self, username: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """사용자의 모든 저장소 조회"""
        url = f"{self.BASE_URL}/users/{username}/repos"
        params = {"per_page": per_page, "sort": "updated"}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API 오류: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"요청 실패: {e}")
                return []
    
    async def search_repos(self, username: str, keyword: str) -> List[Dict[str, Any]]:
        """사용자의 저장소에서 검색"""
        url = f"{self.BASE_URL}/search/repositories"
        params = {
            "q": f"user:{username} {keyword}",
            "sort": "updated",
            "per_page": 30
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("items", [])
                    else:
                        logger.error(f"API 오류: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"요청 실패: {e}")
                return []
