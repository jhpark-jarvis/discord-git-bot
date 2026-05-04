"""
봇 설정 모듈

환경변수 및 봇 설정을 관리합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent

# .env 파일 로드
ENV_PATH = PROJECT_ROOT / "config" / ".env"
load_dotenv(ENV_PATH)

# Discord 설정
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# GitHub 설정
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# GitHub 저장소 기반으로 로컬 경로 자동 생성
if GITHUB_REPO:
    owner, repo = GITHUB_REPO.split("/")
    GITHUB_REPO_PATH = str(PROJECT_ROOT / "repositories" / owner / repo)
else:
    GITHUB_REPO_PATH = str(PROJECT_ROOT / "repositories")

# 웹훅 설정 (선택)
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8080"))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

# 로깅 설정
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / "logs" / "bot.log"

# 기본값 설정 생성
LOG_FILE.parent.mkdir(exist_ok=True)

def validate_config():
    """필수 설정값 검증"""
    errors = []
    
    if not DISCORD_TOKEN:
        errors.append("DISCORD_TOKEN이 설정되지 않았습니다.")
    
    if not GITHUB_TOKEN:
        errors.append("GITHUB_TOKEN이 설정되지 않았습니다.")
    
    if not GITHUB_REPO:
        errors.append("GITHUB_REPO가 설정되지 않았습니다.")
    
    if errors:
        print("❌ 설정 오류:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    return True
