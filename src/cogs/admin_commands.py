"""
관리자 커맨드 Cog

!admin 로 시작하는 관리자 전용 커맨드를 처리합니다.
"""

import discord
from discord.ext import commands
import logging
from typing import Optional

from ..utils.embedders import create_git_embed
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AdminCommands(commands.Cog):
    """관리자 관련 커맨드"""
    
    def __init__(self, bot: commands.Bot):
        """
        초기화
        
        Args:
            bot: Discord 봇 인스턴스
        """
        self.bot = bot
    
    def is_admin(self, ctx: commands.Context) -> bool:
        """관리자 권한 확인"""
        return ctx.author.guild_permissions.administrator
    
    @commands.group(name="admin", invoke_without_command=True)
    @commands.check(lambda ctx: ctx.author.guild_permissions.administrator)
    async def admin_group(self, ctx: commands.Context):
        """관리자 커맨드 그룹"""
        if ctx.invoked_subcommand is None:
            embed = create_git_embed(
                "⚙️ 관리자 커맨드",
                "사용 가능한 관리자 커맨드:\n"
                "`!admin config` - 설정 확인\n"
                "`!admin ping` - 봇 핑 테스트"
            )
            await ctx.send(embed=embed)
    
    @admin_group.command(name="config")
    async def admin_config(self, ctx: commands.Context):
        """설정 확인"""
        from .. import config
        
        embed = create_git_embed(
            "⚙️ 봇 설정",
            ""
        )
        embed.add_field(
            name="Discord",
            value=f"Token: {'●' * 10} (설정됨)" if config.DISCORD_TOKEN else "Token: 미설정",
            inline=False
        )
        embed.add_field(
            name="GitHub",
            value=f"Token: {'●' * 10}\nRepo: {config.GITHUB_REPO}",
            inline=False
        )
        embed.add_field(
            name="웹훅",
            value=f"Port: {config.WEBHOOK_PORT}\nSecret: {'●' * 10}" if config.WEBHOOK_SECRET else "Secret: 미설정",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @admin_group.command(name="ping")
    async def admin_ping(self, ctx: commands.Context):
        """봇 핑 테스트"""
        latency = self.bot.latency * 1000
        embed = create_git_embed(
            "🏓 Pong!",
            f"응답 시간: {latency:.0f}ms"
        )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    """Cog 설정"""
    await bot.add_cog(AdminCommands(bot))
