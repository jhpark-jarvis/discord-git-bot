"""
테스트 커맨드 Cog

테스트 실행 관련 Discord 커맨드를 처리합니다.
"""

import discord
from discord.ext import commands
import logging
import asyncio
from typing import Optional

from ..utils.test_runner import TestRunner, create_test_result_embed
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class TestCommands(commands.Cog):
    """테스트 관련 커맨드"""
    
    def __init__(self, bot: commands.Bot):
        """
        초기화
        
        Args:
            bot: Discord 봇 인스턴스
        """
        self.bot = bot
        self.test_runner = TestRunner()
        self.is_running = False
    
    @commands.group(name="test", invoke_without_command=True)
    async def test_group(self, ctx: commands.Context):
        """테스트 실행 커맨드"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="테스트 명령어",
                description="사용 가능한 테스트 명령어:",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="사용법",
                value="""```
!test all        모든 테스트 실행
!test unit       유닛 테스트만 실행
!test integration 통합 테스트만 실행
!test <test_name> 특정 테스트 실행
```""",
                inline=False
            )
            await ctx.send(embed=embed)
    
    @test_group.command(name="all")
    @commands.is_owner()
    async def test_all(self, ctx: commands.Context):
        """모든 테스트 실행"""
        await self._run_tests(ctx, "all", "모든")
    
    @test_group.command(name="unit")
    @commands.is_owner()
    async def test_unit(self, ctx: commands.Context):
        """유닛 테스트만 실행"""
        await self._run_tests(ctx, "unit", "유닛")
    
    @test_group.command(name="integration")
    @commands.is_owner()
    async def test_integration(self, ctx: commands.Context):
        """통합 테스트만 실행"""
        await self._run_tests(ctx, "integration", "통합")
    
    @test_group.command(name="git_commands")
    @commands.is_owner()
    async def test_git_commands(self, ctx: commands.Context):
        """Git 커맨드 테스트 실행"""
        await self._run_tests(ctx, "git_commands", "Git 커맨드")
    
    @test_group.command(name="git_helper")
    @commands.is_owner()
    async def test_git_helper(self, ctx: commands.Context):
        """Git Helper 테스트 실행"""
        await self._run_tests(ctx, "git_helper", "Git Helper")
    
    @test_group.command(name="git_service")
    @commands.is_owner()
    async def test_git_service(self, ctx: commands.Context):
        """Git Service 테스트 실행"""
        await self._run_tests(ctx, "git_service", "Git Service")
    
    @test_group.command(name="integration_git")
    @commands.is_owner()
    async def test_integration_git(self, ctx: commands.Context):
        """Git 통합 테스트 실행"""
        await self._run_tests(ctx, "integration_git", "Git 통합")
    
    async def _run_tests(self, ctx: commands.Context, test_type: str, description: str):
        """
        테스트 실행
        
        Args:
            ctx: Discord Context
            test_type: 테스트 타입 (all/unit/integration 등)
            description: 설명 텍스트
        """
        # 이미 실행 중인지 확인
        if self.is_running:
            embed = discord.Embed(
                title="테스트 실행 불가",
                description="이미 다른 테스트가 실행 중입니다.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # 시작 메시지
        start_embed = discord.Embed(
            title=f"테스트 시작",
            description=f"{description} 테스트를 실행합니다...",
            color=discord.Color.yellow()
        )
        start_msg = await ctx.send(embed=start_embed)
        
        # 콘솔에 로그
        log_msg = f"테스트 시작: {description} | 사용자: {ctx.author.name}#{ctx.author.id}"
        logger.info(log_msg)
        print(f"\n[TEST] {log_msg}")
        
        self.is_running = True
        
        try:
            # 콜백 함수 생성
            progress_messages = []
            
            def progress_callback(message: str):
                """진행 상황 콜백"""
                print(f"[TEST] {message}")
                progress_messages.append(message)
            
            # 비동기적으로 테스트 실행
            result = await asyncio.to_thread(
                self._run_test_by_type,
                test_type,
                progress_callback
            )
            
            # 진행 상황 메시지 출력
            for msg in progress_messages:
                print(f"[TEST] {msg}")
            
            # 결과 embed 생성
            result_embed = discord.Embed.from_dict(
                create_test_result_embed(result, description)
            )
            
            # 테스트 출력 텍스트가 길면 파일로 저장
            if result.get("output"):
                output = result["output"]
                if len(output) > 1000:
                    # 파일로 저장
                    with open("test_output.txt", "w", encoding="utf-8") as f:
                        f.write(output)
                    
                    # 파일 전송
                    await ctx.send(
                        "테스트 상세 출력:",
                        file=discord.File("test_output.txt")
                    )
                else:
                    # 메시지로 전송
                    output_embed = discord.Embed(
                        title="테스트 상세 출력",
                        description=f"```\n{output[:500]}\n```",
                        color=discord.Color.blurple()
                    )
                    await ctx.send(embed=output_embed)
            
            # 결과 메시지 전송
            await start_msg.edit(embed=result_embed)
            
            # 완료 로그
            status = "완료" if result.get("success") else "실패"
            log_msg = (
                f"테스트 {status}: {result.get('passed', 0)} 통과 / "
                f"{result.get('failed', 0)} 실패 / {result.get('total', 0)} 총계"
            )
            logger.info(log_msg)
            print(f"[TEST] {log_msg}\n")
            
        except Exception as e:
            logger.error(f"테스트 실행 중 오류: {str(e)}", exc_info=True)
            error_embed = discord.Embed(
                title="테스트 오류",
                description=f"테스트 실행 중 오류가 발생했습니다:\n{str(e)[:256]}",
                color=discord.Color.red()
            )
            await start_msg.edit(embed=error_embed)
            print(f"[TEST] 오류: {str(e)}\n")
        
        finally:
            self.is_running = False
    
    def _run_test_by_type(self, test_type: str, callback) -> dict:
        """
        테스트 타입에 따라 실행
        
        Args:
            test_type: 테스트 타입
            callback: 진행 상황 콜백
        
        Returns:
            테스트 결과
        """
        if test_type == "all":
            return self.test_runner.run_all_tests(callback=callback)
        elif test_type == "unit":
            return self.test_runner.run_unit_tests(callback=callback)
        elif test_type == "integration":
            return self.test_runner.run_integration_tests(callback=callback)
        else:
            # 특정 테스트 파일
            return self.test_runner.run_specific_test(
                f"test_{test_type}",
                callback=callback
            )


async def setup(bot: commands.Bot):
    """Cog 로드"""
    await bot.add_cog(TestCommands(bot))
