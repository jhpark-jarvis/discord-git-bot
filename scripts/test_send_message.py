"""
Discord 봇 테스트 메시지 전송 스크립트

사용법:
    python scripts/test_send_message.py <channel_id> [메시지]
    
예시:
    python scripts/test_send_message.py 123456789 "안녕하세요!"
    python scripts/test_send_message.py 123456789  # 기본 메시지 사용
"""

import asyncio
import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(project_root / "config" / ".env")

# 기본 설정
# 주의: message_content Intent를 사용하려면 Discord 개발자 포털에서 활성화해야 합니다
# 테스트 메시지 전송만 할 경우 아래 주석 처리 가능
intents = discord.Intents.default()
intents.message_content = True  # 필요시 주석 해제하고 개발자 포털에서 활성화

client = discord.Client(intents=intents)

async def send_test_message(channel_id: int, message: str):
    """지정된 채널에 테스트 메시지 전송"""
    try:
        channel = client.get_channel(channel_id)
        if channel is None:
            print(f"❌ 오류: 채널 ID {channel_id}를 찾을 수 없습니다.")
            print("   - 채널 ID가 올바른지 확인하세요.")
            print("   - 봇이 해당 채널에 접근 권한이 있는지 확인하세요.")
            return False
        
        await channel.send(message)
        print(f"✅ 메시지 전송 성공!")
        print(f"   채널: {channel.name} ({channel_id})")
        print(f"   메시지: {message}")
        return True
    except discord.Forbidden:
        print(f"❌ 오류: 채널 {channel_id}에 메시지를 보낼 권한이 없습니다.")
        return False
    except discord.HTTPException as e:
        print(f"❌ 오류: HTTP 요청 실패 - {e}")
        return False
    except Exception as e:
        print(f"❌ 오류: {type(e).__name__} - {e}")
        return False

@client.event
async def on_ready():
    """봇이 준비되었을 때 호출"""
    print(f"✅ {client.user}로 연결되었습니다.")
    
    # 테스트 메시지 전송
    if hasattr(client, '_test_channel_id') and hasattr(client, '_test_message'):
        success = await send_test_message(client._test_channel_id, client._test_message)
        
        # 봇 종료
        await client.close()

async def main():
    """메인 함수"""
    # 토큰 확인
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ 오류: DISCORD_TOKEN이 설정되어 있지 않습니다.")
        print("   config/.env 파일을 생성하고 DISCORD_TOKEN을 설정하세요.")
        print("   예: cp config/.env.example config/.env")
        sys.exit(1)
    
    # 명령줄 인자 확인
    if len(sys.argv) < 2:
        print("❌ 사용법: python test_send_message.py <channel_id> [메시지]")
        print()
        print("예시:")
        print("  python scripts/test_send_message.py 123456789 '안녕하세요!'")
        print("  python scripts/test_send_message.py 987654321")
        sys.exit(1)
    
    # 채널 ID 파싱
    try:
        channel_id = int(sys.argv[1])
    except ValueError:
        print(f"❌ 오류: 채널 ID는 숫자여야 합니다. 입력값: {sys.argv[1]}")
        sys.exit(1)
    
    # 메시지 설정
    message = sys.argv[2] if len(sys.argv) > 2 else "🤖 Discord 봇 테스트 메시지입니다!"
    
    # 클라이언트에 정보 저장
    client._test_channel_id = channel_id
    client._test_message = message
    
    # 봇 연결
    try:
        print("🔗 Discord에 연결 중...")
        await client.start(token)
    except discord.LoginFailure:
        print("❌ 오류: 잘못된 Discord 토큰입니다.")
        print("   DISCORD_TOKEN을 확인하세요.")
        sys.exit(1)
    except discord.PrivilegedIntentsRequired:
        print("❌ 오류: Privileged Intents가 활성화되지 않았습니다.")
        print()
        print("해결 방법:")
        print("1. https://discord.com/developers/applications/ 방문")
        print("2. 봇 애플리케이션 선택")
        print("3. 'Bot' 메뉴 → 'Privileged Gateway Intents' 섹션")
        print("4. 'Message Content Intent' 활성화 후 저장")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 오류: {type(e).__name__} - {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
