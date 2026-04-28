"""
Discord Embed 생성 모듈

Discord 메시지용 Embed를 생성합니다.
"""

from typing import Optional, List
import discord

def create_git_embed(title: str, description: str, **kwargs) -> discord.Embed:
    """
    Git 관련 Embed 생성
    
    Args:
        title: 제목
        description: 설명
        **kwargs: 추가 옵션
    
    Returns:
        Embed 객체
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue(),
        **kwargs
    )
    return embed

def create_webhook_embed(
    event_type: str,
    repo_name: str,
    details: dict,
    **kwargs
) -> discord.Embed:
    """
    GitHub 웹훅 이벤트 Embed 생성
    
    Args:
        event_type: 이벤트 타입 (push, pull_request, issues, etc)
        repo_name: 저장소명
        details: 이벤트 상세 정보
        **kwargs: 추가 옵션
    
    Returns:
        Embed 객체
    """
    embed = discord.Embed(
        title=f"[{repo_name}] {event_type.upper()}",
        description=details.get('description', ''),
        color=discord.Color.green(),
        **kwargs
    )
    
    # 필드 추가
    for key, value in details.items():
        if key != 'description' and value:
            embed.add_field(
                name=key,
                value=str(value)[:1024],
                inline=False
            )
    
    return embed
