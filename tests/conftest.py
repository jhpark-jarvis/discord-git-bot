"""
Pytest 설정 및 공통 Fixtures

모든 테스트에서 사용할 수 있는 공통 설정과 Fixtures를 정의합니다.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock

# 프로젝트 루트 경로 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def mock_discord_context():
    """Mock Discord Context"""
    from unittest.mock import AsyncMock
    from discord.ext import commands
    
    ctx = AsyncMock(spec=commands.Context)
    ctx.author = MagicMock()
    ctx.author.name = "TestUser"
    ctx.author.id = 123456789
    ctx.guild = MagicMock()
    ctx.guild.name = "TestServer"
    ctx.channel = MagicMock()
    ctx.channel.name = "test-channel"
    
    # typing context manager 설정
    ctx.typing = AsyncMock()
    ctx.typing.__aenter__ = AsyncMock()
    ctx.typing.__aexit__ = AsyncMock()
    
    return ctx


@pytest.fixture
def mock_git_helper():
    """Mock GitHelper"""
    mock = MagicMock()
    mock.get_current_branch.return_value = 'main'
    mock.get_status.return_value = 'On branch main\nnothing to commit'
    mock.get_log.return_value = [
        {
            'hash': 'abc1234',
            'author': 'Test Author',
            'message': 'Test commit',
            'date': '2024-01-01T10:00:00'
        }
    ]
    mock.get_branches.return_value = ['main', 'develop']
    mock.pull.return_value = '✅ Pull 완료'
    
    return mock


@pytest.fixture
def mock_git_service():
    """Mock GitService"""
    mock = MagicMock()
    mock.get_status_info.return_value = {
        'branch': 'main',
        'status': 'On branch main\nnothing to commit'
    }
    mock.get_recent_commits.return_value = {
        'commits': [
            {
                'hash': 'abc1234',
                'author': 'Test Author',
                'message': 'Test commit',
                'date': '2024-01-01T10:00:00'
            }
        ]
    }
    mock.get_branches_info.return_value = {
        'branches': ['main', 'develop'],
        'current_branch': 'main'
    }
    mock.sync_repository.return_value = {
        'result': '✅ Pull 완료'
    }
    
    return mock


@pytest.fixture
def mock_bot():
    """Mock Discord Bot"""
    from discord.ext import commands
    bot = MagicMock(spec=commands.Bot)
    bot.user = MagicMock()
    bot.user.name = "TestBot"
    bot.user.id = 987654321
    bot.latency = 0.05
    bot.command_prefix = "!"
    
    return bot


@pytest.fixture
def sample_commits():
    """Sample commit data for testing"""
    return [
        {
            'hash': 'abc1234',
            'author': 'John Doe',
            'message': 'Fix: critical bug in parser',
            'date': '2024-01-01T10:00:00'
        },
        {
            'hash': 'def5678',
            'author': 'Jane Smith',
            'message': 'Feature: add new logging system',
            'date': '2024-01-02T11:30:00'
        },
        {
            'hash': 'ghi9012',
            'author': 'Bob Johnson',
            'message': 'Refactor: optimize database queries',
            'date': '2024-01-03T14:15:00'
        }
    ]


@pytest.fixture
def sample_branches():
    """Sample branch data for testing"""
    return {
        'branches': ['main', 'develop', 'feature/new-api', 'bugfix/issue-123'],
        'current_branch': 'develop'
    }


# pytest-asyncio 설정
pytest_plugins = ('pytest_asyncio',)


def pytest_configure(config):
    """Pytest 초기화"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async test"
    )
