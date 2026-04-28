"""
Discord-Git Bot
Discord 서버와 Git 저장소를 연동하는 봇

사용법:
    python -m src.main
"""

import discord
from discord.ext import commands
import asyncio
import logging
from pathlib import Path
import sys
import os

# 프로젝트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 설정 및 로거 초기화
from .config import validate_config, COMMAND_PREFIX, DISCORD_TOKEN, LOG_LEVEL
from .utils.logger import setup_logger

logger = setup_logger(__name__, LOG_LEVEL)

# 기본 설정
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# ==================== 이벤트 핸들러 ====================

@bot.event
async def on_ready():
    """봇이 준비되었을 때 호출"""
    logger.info(f"✅ {bot.user}로 로그인했습니다.")
    logger.info(f"Syncing commands...")
    await bot.tree.sync()
    logger.info("✅ 봇이 준비되었습니다!")
    print(f"\n{'=' * 50}")
    print(f"Bot Name: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Command Prefix: {COMMAND_PREFIX}")
    print(f"{'=' * 50}\n")

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """커맨드 에러 처리"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ 알 수 없는 커맨드입니다. `{COMMAND_PREFIX}help`를 입력하세요.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ 이 커맨드를 실행할 권한이 없습니다.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ 필수 인자가 누락되었습니다. `{COMMAND_PREFIX}help {ctx.command}`를 입력하세요.")
    else:
        logger.error(f"Unhandled error: {error}")
        await ctx.send(f"❌ 오류가 발생했습니다: {error}")

@bot.command(name="ping", help="봇이 응답하는지 확인")
async def ping(ctx):
    """봇이 응답하는지 확인"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"응답 시간: {latency}ms",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name="hello", help="인사 명령")
async def hello(ctx):
    """인사 명령"""
    await ctx.send(f"안녕하세요, {ctx.author.name}님! 👋")

# ==================== Cog 로더 ====================

async def load_cogs():
    """Cogs 로드"""
    cogs_path = Path(__file__).parent / "cogs"
    
    for cog_file in cogs_path.glob("*.py"):
        if cog_file.name.startswith("_"):
            continue
        
        cog_name = cog_file.stem
        try:
            await bot.load_extension(f"src.cogs.{cog_name}")
            logger.info(f"✅ Cog 로드: {cog_name}")
        except Exception as e:
            logger.error(f"❌ Cog 로드 실패 ({cog_name}): {e}")

async def main():
    """메인 함수"""
    # 설정 검증
    if not validate_config():
        logger.error("필수 설정이 누락되었습니다.")
        sys.exit(1)
    
    # Cogs 로드
    async with bot:
        await load_cogs()
        
        # 봇 실행
        logger.info("🚀 봇을 시작합니다...")
        try:
            await bot.start(DISCORD_TOKEN)
        except discord.LoginFailure:
            logger.error("❌ 로그인 실패: 잘못된 토큰입니다.")
            sys.exit(1)
        except KeyboardInterrupt:
            logger.info("봇이 중지되었습니다.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"❌ 오류: {type(e).__name__} - {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
