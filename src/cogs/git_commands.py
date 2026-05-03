"""
Git 커맨드 Cog

!git 로 시작하는 모든 Git 관련 커맨드를 처리합니다.
"""

import discord
from discord.ext import commands
import logging
from typing import Optional

from ..services.git_service import GitService
from ..utils.embedders import create_git_embed
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class GitCommands(commands.Cog):
    """Git 관련 커맨드"""
    
    def __init__(self, bot: commands.Bot):
        """
        초기화
        
        Args:
            bot: Discord 봇 인스턴스
        """
        self.bot = bot
        from .. import config
        try:
            self.git_service = GitService(config.GITHUB_REPO_PATH)
        except Exception as e:
            logger.error(f"Git 서비스 초기화 실패: {e}")
            self.git_service = None
    
    @commands.group(name="git", invoke_without_command=True)
    async def git_group(self, ctx: commands.Context):
        """Git 커맨드 그룹"""
        if ctx.invoked_subcommand is None:
            embed = create_git_embed(
                "🔧 Git 커맨드",
                "사용 가능한 Git 커맨드:\n"
                "`!git status` - 저장소 상태\n"
                "`!git log [n]` - 최근 n개 커밋 (기본: 5)\n"
                "`!git branch` - 브랜치 목록\n"
                "`!git pull` - 저장소 동기화"
            )
            await ctx.send(embed=embed)
    
    @git_group.command(name="status")
    async def git_status(self, ctx: commands.Context):
        """저장소 상태 조회"""
        # 명령어 실행 로그
        log_message = f"👤 {ctx.author.name}#{ctx.author.id} | 📍 #{ctx.channel.name} | ⚙️  명령어: git status"
        logger.info(log_message)
        print(f"\n[GIT COMMAND] {log_message}")
        
        if not self.git_service:
            error_msg = "❌ 저장소를 사용할 수 없습니다"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        info = self.git_service.get_status_info()
        
        if "error" in info:
            error_msg = f"❌ {info['error']}"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        success_msg = f"✅ 저장소 상태 조회 성공 (브랜치: {info['branch']})"
        logger.info(f"   결과: {success_msg}")
        print(f"[RESULT] {success_msg}")
        
        embed = create_git_embed(
            "📊 저장소 상태",
            f"**브랜치**: {info['branch']}"
        )
        embed.add_field(
            name="상태",
            value=f"```\n{info['status'][:1000]}\n```",
            inline=False
        )
        await ctx.send(embed=embed)
    
    @git_group.command(name="log")
    async def git_log(self, ctx: commands.Context, n: int = 5):
        """최근 커밋 조회"""
        # 명령어 실행 로그
        log_message = f"👤 {ctx.author.name}#{ctx.author.id} | 📍 #{ctx.channel.name} | ⚙️  명령어: git log (n={n})"
        logger.info(log_message)
        print(f"\n[GIT COMMAND] {log_message}")
        
        if not self.git_service:
            error_msg = "❌ 저장소를 사용할 수 없습니다"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        if n > 20:
            n = 20
        
        info = self.git_service.get_recent_commits(n)
        
        if "error" in info:
            error_msg = f"❌ {info['error']}"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        if not info['commits']:
            warning_msg = "❌ 커밋이 없습니다"
            logger.warning(f"   결과: {warning_msg}")
            print(f"[RESULT] {warning_msg}")
            await ctx.send(warning_msg)
            return
        
        success_msg = f"✅ {len(info['commits'])}개 커밋 조회 성공"
        logger.info(f"   결과: {success_msg}")
        print(f"[RESULT] {success_msg}")
        
        embed = create_git_embed(
            f"📝 최근 {len(info['commits'])}개 커밋",
            ""
        )
        
        for commit in info['commits']:
            embed.add_field(
                name=f"{commit['hash']} - {commit['author']}",
                value=commit['message'][:200],
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @git_group.command(name="branch")
    async def git_branch(self, ctx: commands.Context):
        """브랜치 목록 조회"""
        # 명령어 실행 로그
        log_message = f"👤 {ctx.author.name}#{ctx.author.id} | 📍 #{ctx.channel.name} | ⚙️  명령어: git branch"
        logger.info(log_message)
        print(f"\n[GIT COMMAND] {log_message}")
        
        if not self.git_service:
            error_msg = "❌ 저장소를 사용할 수 없습니다"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        info = self.git_service.get_branches_info()
        
        if "error" in info:
            error_msg = f"❌ {info['error']}"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        branches = info['branches']
        current = info['current_branch']
        
        success_msg = f"✅ {len(branches)}개 브랜치 조회 성공 (현재: {current})"
        logger.info(f"   결과: {success_msg}")
        print(f"[RESULT] {success_msg}")
        
        branch_list = "\n".join(
            f"{'→ ' if branch == current else '  '}{branch}"
            for branch in branches
        )
        
        embed = create_git_embed(
            "🌿 브랜치 목록",
            f"```\n{branch_list}\n```"
        )
        await ctx.send(embed=embed)
    
    @git_group.command(name="pull")
    async def git_pull(self, ctx: commands.Context):
        """저장소 동기화"""
        # 명령어 실행 로그
        log_message = f"👤 {ctx.author.name}#{ctx.author.id} | 📍 #{ctx.channel.name} | ⚙️  명령어: git pull"
        logger.info(log_message)
        print(f"\n[GIT COMMAND] {log_message}")
        
        if not self.git_service:
            error_msg = "❌ 저장소를 사용할 수 없습니다"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        async with ctx.typing():
            info = self.git_service.sync_repository()
        
        if "error" in info:
            error_msg = f"❌ {info['error']}"
            logger.error(f"   결과: {error_msg}")
            print(f"[RESULT] {error_msg}")
            await ctx.send(error_msg)
            return
        
        success_msg = info['result']
        logger.info(f"   결과: {success_msg}")
        print(f"[RESULT] {success_msg}")
        
        await ctx.send(success_msg)

async def setup(bot: commands.Bot):
    """Cog 설정"""
    await bot.add_cog(GitCommands(bot))
