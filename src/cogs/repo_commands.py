"""
저장소 커맨드 Cog

!repo 로 시작하는 저장소 관련 커맨드를 처리합니다.
"""

import discord
from discord.ext import commands
import logging

from ..services.github_service import GithubService
from ..utils.embedders import create_git_embed
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class RepoCommands(commands.Cog):
    """저장소 관련 커맨드"""
    
    def __init__(self, bot: commands.Bot):
        """
        초기화
        
        Args:
            bot: Discord 봇 인스턴스
        """
        self.bot = bot
        from .. import config
        try:
            self.github_service = GithubService(config.GITHUB_TOKEN)
        except Exception as e:
            logger.error(f"GitHub 서비스 초기화 실패: {e}")
            self.github_service = None
    
    @commands.group(name="repo", invoke_without_command=True)
    async def repo_group(self, ctx: commands.Context):
        """저장소 커맨드 그룹"""
        if ctx.invoked_subcommand is None:
            embed = create_git_embed(
                "📦 저장소 커맨드",
                "사용 가능한 저장소 커맨드:\n"
                "`!repo info` - 현재 설정된 저장소 정보\n"
                "`!repo issues` - 현재 저장소 오픈 이슈\n"
                "`!repo prs` - 현재 저장소 오픈 PR\n"
                "`!repo list` - 내 GitHub 계정의 모든 저장소\n"
                "`!repo search <키워드>` - 저장소 검색"
            )
            await ctx.send(embed=embed)
    
    @repo_group.command(name="info")
    async def repo_info(self, ctx: commands.Context):
        """저장소 정보 조회"""
        if not self.github_service:
            await ctx.send("❌ GitHub 서비스를 사용할 수 없습니다")
            return
        
        from .. import config
        owner, repo = config.GITHUB_REPO.split('/')
        
        async with ctx.typing():
            info = await self.github_service.get_repository_info(owner, repo)
        
        if "error" in info:
            await ctx.send(f"❌ {info['error']}")
            return
        
        embed = create_git_embed(
            f"📦 {info['name']}",
            info.get('description', '설명 없음')
        )
        embed.add_field(name="⭐ Stars", value=str(info['stars']), inline=True)
        embed.add_field(name="🍴 Forks", value=str(info['forks']), inline=True)
        embed.add_field(name="📋 Issues", value=str(info['open_issues']), inline=True)
        embed.add_field(name="🔗 URL", value=f"[GitHub]({info['url']})", inline=False)
        
        await ctx.send(embed=embed)
    
    @repo_group.command(name="issues")
    async def repo_issues(self, ctx: commands.Context):
        """오픈 이슈 목록"""
        if not self.github_service:
            await ctx.send("❌ GitHub 서비스를 사용할 수 없습니다")
            return
        
        from .. import config
        owner, repo = config.GITHUB_REPO.split('/')
        
        async with ctx.typing():
            info = await self.github_service.get_issues_info(owner, repo)
        
        if info['count'] == 0:
            await ctx.send("✅ 오픈 이슈가 없습니다")
            return
        
        embed = create_git_embed(
            f"📋 오픈 이슈 ({info['count']}개)",
            ""
        )
        
        for issue in info['issues']:
            embed.add_field(
                name=f"#{issue['number']} - {issue['title']}",
                value=f"작성자: {issue['author']}\n[링크]({issue['url']})",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @repo_group.command(name="prs")
    async def repo_prs(self, ctx: commands.Context):
        """오픈 PR 목록"""
        if not self.github_service:
            await ctx.send("❌ GitHub 서비스를 사용할 수 없습니다")
            return
        
        from .. import config
        owner, repo = config.GITHUB_REPO.split('/')
        
        async with ctx.typing():
            info = await self.github_service.get_prs_info(owner, repo)
        
        if info['count'] == 0:
            await ctx.send("✅ 오픈 PR이 없습니다")
            return
        
        embed = create_git_embed(
            f"🔀 오픈 PR ({info['count']}개)",
            ""
        )
        
        for pr in info['prs']:
            embed.add_field(
                name=f"#{pr['number']} - {pr['title']}",
                value=f"작성자: {pr['author']}\n[링크]({pr['url']})",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @repo_group.command(name="list")
    async def repo_list(self, ctx: commands.Context):
        """내 GitHub 계정의 모든 저장소 조회"""
        if not self.github_service:
            await ctx.send("❌ GitHub 서비스를 사용할 수 없습니다")
            return
        
        from .. import config
        owner = config.GITHUB_REPO.split('/')[0]
        
        async with ctx.typing():
            info = await self.github_service.get_user_repositories(owner)
        
        if "error" in info:
            await ctx.send(f"❌ {info['error']}")
            return
        
        if info['count'] == 0:
            await ctx.send("❌ 저장소가 없습니다")
            return
        
        embed = create_git_embed(
            f"📚 {owner}의 저장소 ({info['count']}개)",
            "최근 업데이트된 순서\n*(최대 20개 표시)*"
        )
        embed.color = discord.Color.purple()
        
        for idx, repo in enumerate(info['repositories'], 1):
            value = (
                f"**⭐ {repo['stars']}** | "
                f"**🔤 {repo['language']}**\n"
                f"{repo['description']}\n"
                f"[링크]({repo['url']})"
            )
            embed.add_field(
                name=f"{idx}. {repo['name']}",
                value=value,
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @repo_group.command(name="search")
    async def repo_search(self, ctx: commands.Context, *, keyword: str):
        """저장소 검색
        
        사용법: !repo search <키워드>
        예: !repo search discord
        """
        if not self.github_service:
            await ctx.send("❌ GitHub 서비스를 사용할 수 없습니다")
            return
        
        if not keyword or len(keyword) < 2:
            await ctx.send("❌ 검색 키워드는 최소 2자 이상이어야 합니다")
            return
        
        from .. import config
        owner = config.GITHUB_REPO.split('/')[0]
        
        async with ctx.typing():
            info = await self.github_service.search_user_repositories(owner, keyword)
        
        if "error" in info or info['count'] == 0:
            await ctx.send(f"❌ '{keyword}' 검색 결과가 없습니다")
            return
        
        embed = create_git_embed(
            f"🔍 '{keyword}' 검색 결과",
            f"{owner}의 저장소 중 검색된 항목: {info['count']}개\n*(최대 15개 표시)*"
        )
        embed.color = discord.Color.orange()
        
        for idx, repo in enumerate(info['results'], 1):
            value = (
                f"**⭐ {repo['stars']}** | "
                f"**🔤 {repo['language']}**\n"
                f"{repo['description']}\n"
                f"[링크]({repo['url']})"
            )
            embed.add_field(
                name=f"{idx}. {repo['name']}",
                value=value,
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    """Cog 설정"""
    await bot.add_cog(RepoCommands(bot))
