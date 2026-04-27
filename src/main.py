"""
Discord-Git Bot
Discord 서버와 Git 저장소를 연동하는 봇
"""

import discord
from discord.ext import commands

# 기본 설정
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """봇이 준비되었을 때 호출"""
    print(f"{bot.user}로 로그인했습니다.")
    print("봇이 준비되었습니다!")

@bot.command(name="ping")
async def ping(ctx):
    """봇이 응답하는지 확인"""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name="hello")
async def hello(ctx):
    """인사 명령"""
    await ctx.send(f"안녕하세요, {ctx.author.name}님!")

if __name__ == "__main__":
    # .env 파일에서 DISCORD_TOKEN을 읽어 봇을 실행
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("오류: .env 파일에 DISCORD_TOKEN이 설정되어 있지 않습니다.")
        exit(1)
    
    bot.run(token)
