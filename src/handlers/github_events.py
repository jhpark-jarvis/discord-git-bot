"""
GitHub 이벤트 파서

GitHub 웹훅 이벤트를 파싱하고 처리합니다.
"""

import logging
from typing import Dict, Any, Optional

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class GithubEventParser:
    """GitHub 이벤트 파서"""
    
    @staticmethod
    def parse(event_type: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        GitHub 이벤트 파싱
        
        Args:
            event_type: 이벤트 타입 (X-GitHub-Event 헤더 값)
            payload: GitHub 웹훅 페이로드
        
        Returns:
            파싱된 이벤트 정보
        """
        parsers = {
            'push': GithubEventParser._parse_push,
            'pull_request': GithubEventParser._parse_pull_request,
            'issues': GithubEventParser._parse_issues,
            'release': GithubEventParser._parse_release,
        }
        
        parser = parsers.get(event_type)
        if parser:
            return parser(payload)
        
        return None
    
    @staticmethod
    def _parse_push(payload: Dict[str, Any]) -> Dict[str, Any]:
        """푸시 이벤트 파싱"""
        return {
            'event_type': 'push',
            'repo': payload.get('repository', {}).get('full_name', 'Unknown'),
            'pusher': payload.get('pusher', {}).get('name', 'Unknown'),
            'branch': payload.get('ref', '').split('/')[-1],
            'commits': [
                {
                    'id': c.get('id', '')[:7],
                    'message': c.get('message', '').split('\n')[0],
                    'author': c.get('author', {}).get('name', 'Unknown'),
                }
                for c in payload.get('commits', [])[:5]
            ],
            'distinct_commits': payload.get('distinct_size', 0),
        }
    
    @staticmethod
    def _parse_pull_request(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Pull Request 이벤트 파싱"""
        pr = payload.get('pull_request', {})
        return {
            'event_type': 'pull_request',
            'repo': payload.get('repository', {}).get('full_name', 'Unknown'),
            'action': payload.get('action', 'unknown'),
            'number': pr.get('number'),
            'title': pr.get('title', 'Untitled'),
            'author': pr.get('user', {}).get('login', 'Unknown'),
            'url': pr.get('html_url', ''),
            'base_branch': pr.get('base', {}).get('ref', 'unknown'),
            'head_branch': pr.get('head', {}).get('ref', 'unknown'),
        }
    
    @staticmethod
    def _parse_issues(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Issues 이벤트 파싱"""
        issue = payload.get('issue', {})
        return {
            'event_type': 'issues',
            'repo': payload.get('repository', {}).get('full_name', 'Unknown'),
            'action': payload.get('action', 'unknown'),
            'number': issue.get('number'),
            'title': issue.get('title', 'Untitled'),
            'author': issue.get('user', {}).get('login', 'Unknown'),
            'url': issue.get('html_url', ''),
            'state': issue.get('state', 'unknown'),
        }
    
    @staticmethod
    def _parse_release(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Release 이벤트 파싱"""
        release = payload.get('release', {})
        return {
            'event_type': 'release',
            'repo': payload.get('repository', {}).get('full_name', 'Unknown'),
            'action': payload.get('action', 'unknown'),
            'tag_name': release.get('tag_name', 'Unknown'),
            'name': release.get('name', 'Untitled'),
            'author': release.get('author', {}).get('login', 'Unknown'),
            'url': release.get('html_url', ''),
            'prerelease': release.get('prerelease', False),
        }
