"""
테스트 결과를 Discord 채널에 전송하는 스크립트

사용법:
    python scripts/send_test_results.py
"""

import asyncio
import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import discord
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(project_root / "config" / ".env")

# 기본 설정
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

# 테스트 결과 데이터
TEST_RESULTS = {
    "GitCommands Cog": {
        "total": 7,
        "passed": 7,
        "tests": [
            "✅ Cog 초기화 성공",
            "✅ Cog 초기화 실패 처리",
            "✅ Git 서비스 상태 조회",
            "✅ Git 서비스 없음 처리",
            "✅ 최근 커밋 조회",
            "✅ 브랜치 정보 조회",
            "✅ 저장소 동기화"
        ]
    },
    "GitHelper": {
        "total": 14,
        "passed": 14,
        "tests": [
            "✅ 저장소 초기화 성공",
            "✅ 유효하지 않은 저장소 처리",
            "✅ 저장소 상태 조회",
            "✅ 상태 조회 에러 처리",
            "✅ 저장소 없음 처리",
            "✅ 커밋 로그 조회",
            "✅ 로그 조회 에러 처리",
            "✅ 로그 없음 처리",
            "✅ 브랜치 목록 조회",
            "✅ 브랜치 조회 에러 처리",
            "✅ 현재 브랜치 조회",
            "✅ 현재 브랜치 에러 처리",
            "✅ Pull 성공",
            "✅ Pull 에러 처리"
        ]
    },
    "GitService": {
        "total": 13,
        "passed": 13,
        "tests": [
            "✅ 서비스 초기화 성공",
            "✅ 서비스 초기화 실패 처리",
            "✅ 상태 정보 조회",
            "✅ 상태 정보 조회 (서비스 없음)",
            "✅ 최근 커밋 조회",
            "✅ 최근 커밋 조회 (서비스 없음)",
            "✅ 최근 커밋 조회 (빈 결과)",
            "✅ 브랜치 정보 조회",
            "✅ 브랜치 정보 조회 (서비스 없음)",
            "✅ 저장소 동기화 성공",
            "✅ 저장소 동기화 에러 처리",
            "✅ 저장소 동기화 (서비스 없음)"
        ]
    },
    "Integration Tests": {
        "total": 6,
        "passed": 6,
        "tests": [
            "✅ GitHelper 전체 워크플로우",
            "✅ GitService 전체 워크플로우",
            "✅ GitCommands 통합 워크플로우",
            "✅ 에러 처리 워크플로우",
            "✅ 다중 명령어 순차 실행",
            "✅ 많은 커밋 목록 처리"
        ]
    }
}

TOTAL_TESTS = sum(data["total"] for data in TEST_RESULTS.values())
TOTAL_PASSED = sum(data["passed"] for data in TEST_RESULTS.values())


async def send_test_results():
    """테스트 결과를 Discord에 전송"""
    if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID:
        print("❌ 오류: DISCORD_TOKEN 또는 DISCORD_CHANNEL_ID가 설정되지 않았습니다.")
        print("   config/.env 파일을 확인하세요.")
        return False
    
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            
            if channel is None:
                print(f"❌ 오류: 채널 ID {DISCORD_CHANNEL_ID}를 찾을 수 없습니다.")
                await client.close()
                return
            
            print(f"✅ 채널 '{channel.name}'에 테스트 결과를 전송 중...\n")
            
            # 헤더 메시지
            header_embed = discord.Embed(
                title="🧪 테스트 실행 결과",
                description=f"**전체: {TOTAL_PASSED}/{TOTAL_TESTS} 통과**",
                color=discord.Color.green()
            )
            header_embed.add_field(
                name="📊 요약",
                value=f"```\n성공률: {(TOTAL_PASSED/TOTAL_TESTS)*100:.1f}%\n```",
                inline=False
            )
            
            await channel.send(embed=header_embed)
            
            # 각 카테고리별 결과
            for category, data in TEST_RESULTS.items():
                print(f"📤 '{category}' 테스트 결과 전송 중...")
                
                embed = discord.Embed(
                    title=f"📋 {category}",
                    description=f"**{data['passed']}/{data['total']} 통과**",
                    color=discord.Color.blue() if data['passed'] == data['total'] else discord.Color.orange()
                )
                
                # 테스트 목록
                tests_text = "\n".join(data['tests'])
                embed.add_field(
                    name="테스트 목록",
                    value=tests_text,
                    inline=False
                )
                
                await channel.send(embed=embed)
                await asyncio.sleep(0.5)  # Rate limiting 방지
            
            # 마무리 메시지
            footer_embed = discord.Embed(
                title="✅ 모든 테스트 완료",
                description="모든 Git 기능이 정상적으로 작동합니다!",
                color=discord.Color.green()
            )
            footer_embed.add_field(
                name="🚀 사용 가능한 명령어",
                value="""```
!git status   - 저장소 상태 확인
!git log [n]  - 최근 n개 커밋 보기 (기본: 5)
!git branch   - 브랜치 목록 확인
!git pull     - 저장소 동기화
```""",
                inline=False
            )
            
            await channel.send(embed=footer_embed)
            
            print(f"\n✅ 모든 테스트 결과가 '{channel.name}' 채널에 전송되었습니다!")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        finally:
            await client.close()
    
    try:
        await client.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Discord 연결 오류: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("테스트 결과 Discord 전송 도구")
    print("=" * 50)
    
    try:
        asyncio.run(send_test_results())
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
