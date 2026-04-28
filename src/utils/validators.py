"""
입력값 검증 모듈
"""

import re
import logging

logger = logging.getLogger(__name__)

def validate_channel_id(channel_id: str) -> bool:
    """
    Discord 채널 ID 검증
    
    Args:
        channel_id: 채널 ID 문자열
    
    Returns:
        유효성 여부
    """
    try:
        int_id = int(channel_id)
        return 0 < int_id < 2**63
    except ValueError:
        return False

def validate_repo_name(repo_name: str) -> bool:
    """
    저장소명 검증 (owner/repo 형식)
    
    Args:
        repo_name: 저장소명
    
    Returns:
        유효성 여부
    """
    pattern = r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$'
    return bool(re.match(pattern, repo_name))

def validate_webhook_secret(secret: str) -> bool:
    """
    웹훅 시크릿 검증
    
    Args:
        secret: 웹훅 시크릿
    
    Returns:
        유효성 여부
    """
    return len(secret) >= 8
