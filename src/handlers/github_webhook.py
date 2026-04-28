"""
GitHub 웹훅 핸들러

GitHub 웹훅 이벤트를 처리합니다.
"""

import logging
import hmac
import hashlib
import json
from typing import Optional, Dict, Any

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class GithubWebhookHandler:
    """GitHub 웹훅 핸들러"""
    
    def __init__(self, secret: str = ""):
        """
        초기화
        
        Args:
            secret: 웹훅 서명 시크릿
        """
        self.secret = secret.encode() if secret else None
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """
        GitHub 웹훅 서명 검증
        
        Args:
            payload: 요청 본문
            signature: GitHub에서 보낸 서명 (X-Hub-Signature-256)
        
        Returns:
            검증 결과
        """
        if not self.secret:
            logger.warning("웹훅 시크릿이 설정되지 않았습니다")
            return False
        
        expected_signature = "sha256=" + hmac.new(
            self.secret,
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def parse_payload(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        웹훅 페이로드 파싱
        
        Args:
            payload: GitHub 웹훅 페이로드
        
        Returns:
            파싱된 이벤트 정보
        """
        event_action = payload.get('action')
        
        # 푸시 이벤트
        if 'push' in str(payload):
            return self._parse_push_event(payload)
        
        # Pull Request 이벤트
        if 'pull_request' in payload:
            return self._parse_pr_event(payload)
        
        # Issues 이벤트
        if 'issue' in payload:
            return self._parse_issues_event(payload)
        
        return None
    
    def _parse_push_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """푸시 이벤트 파싱"""
        repo_name = payload.get('repository', {}).get('full_name', 'Unknown')
        pusher = payload.get('pusher', {}).get('name', 'Unknown')
        commits = payload.get('commits', [])
        
        return {
            'event_type': 'push',
            'repo_name': repo_name,
            'pusher': pusher,
            'commit_count': len(commits),
            'commits': commits[:5],  # 최대 5개만
            'branch': payload.get('ref', '').split('/')[-1],
        }
    
    def _parse_pr_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Pull Request 이벤트 파싱"""
        pr = payload.get('pull_request', {})
        action = payload.get('action', 'unknown')
        
        return {
            'event_type': 'pull_request',
            'action': action,
            'repo_name': payload.get('repository', {}).get('full_name', 'Unknown'),
            'pr_number': pr.get('number'),
            'title': pr.get('title'),
            'author': pr.get('user', {}).get('login'),
            'url': pr.get('html_url'),
        }
    
    def _parse_issues_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Issues 이벤트 파싱"""
        issue = payload.get('issue', {})
        action = payload.get('action', 'unknown')
        
        return {
            'event_type': 'issues',
            'action': action,
            'repo_name': payload.get('repository', {}).get('full_name', 'Unknown'),
            'issue_number': issue.get('number'),
            'title': issue.get('title'),
            'author': issue.get('user', {}).get('login'),
            'url': issue.get('html_url'),
        }

class GithubEventParser:
    """GitHub 이벤트 파서"""
    
    @staticmethod
    def format_push_event(event_data: Dict[str, Any]) -> str:
        """푸시 이벤트 포매팅"""
        return (
            f"**{event_data['repo_name']}** - Push\n"
            f"작성자: {event_data['pusher']}\n"
            f"브랜치: {event_data['branch']}\n"
            f"커밋: {event_data['commit_count']}개"
        )
    
    @staticmethod
    def format_pr_event(event_data: Dict[str, Any]) -> str:
        """Pull Request 이벤트 포매팅"""
        action_text = {
            'opened': '열림',
            'closed': '닫힘',
            'merged': '병합됨',
            'synchronize': '업데이트됨',
        }.get(event_data['action'], event_data['action'])
        
        return (
            f"**{event_data['repo_name']}** - PR {action_text}\n"
            f"#{event_data['pr_number']}: {event_data['title']}\n"
            f"작성자: {event_data['author']}"
        )
    
    @staticmethod
    def format_issues_event(event_data: Dict[str, Any]) -> str:
        """Issues 이벤트 포매팅"""
        action_text = {
            'opened': '열림',
            'closed': '닫힘',
            'reopened': '다시 열림',
        }.get(event_data['action'], event_data['action'])
        
        return (
            f"**{event_data['repo_name']}** - Issue {action_text}\n"
            f"#{event_data['issue_number']}: {event_data['title']}\n"
            f"작성자: {event_data['author']}"
        )
