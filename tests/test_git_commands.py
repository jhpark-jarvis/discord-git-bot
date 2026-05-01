"""
GitCommands Cog 유닛테스트

Discord 커맨드 핸들러를 테스트합니다.
"""

import pytest
import discord
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands

from src.cogs.git_commands import GitCommands


@pytest.mark.asyncio
class TestGitCommands:
    """GitCommands Cog 테스트"""
    
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    def test_cog_init_success(self, mock_logger, mock_git_service_class):
        """Cog 초기화 성공"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        with patch('src.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        assert cog.bot is not None
        assert cog.git_service is not None
    
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    def test_cog_init_error(self, mock_logger, mock_git_service_class):
        """Cog 초기화 실패"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service_class.side_effect = Exception("Error")
        
        with patch('src.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '/invalid'
            cog = GitCommands(mock_bot)
        
        assert cog.git_service is None
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_status_success(self, mock_logger, mock_git_service_class):
        """!git status 성공"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_git_service.get_status_info.return_value = {
            'branch': 'main',
            'status': 'On branch main\nnothing to commit'
        }
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        # Mock Context 생성
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_status(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        call_args = mock_ctx.send.call_args
        assert isinstance(call_args[1]['embed'], discord.Embed)
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_status_no_service(self, mock_logger, mock_git_service_class):
        """!git status 서비스 없음"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service_class.side_effect = Exception("Error")
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '/invalid'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_status(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        call_args = mock_ctx.send.call_args[0][0]
        assert "저장소를 사용할 수 없습니다" in call_args
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_status_error(self, mock_logger, mock_git_service_class):
        """!git status 에러"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_git_service.get_status_info.return_value = {
            'error': '저장소 접근 불가'
        }
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_status(mock_ctx)
        
        call_args = mock_ctx.send.call_args[0][0]
        assert "저장소 접근 불가" in call_args
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_log_success(self, mock_logger, mock_git_service_class):
        """!git log 성공"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_commits = [
            {
                'hash': 'abc1234',
                'author': 'John Doe',
                'message': 'Fix: bug'
            },
            {
                'hash': 'def5678',
                'author': 'Jane Smith',
                'message': 'Feat: new feature'
            }
        ]
        mock_git_service.get_recent_commits.return_value = {
            'commits': mock_commits
        }
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_log(mock_ctx, n=2)
        
        mock_ctx.send.assert_called_once()
        mock_git_service.get_recent_commits.assert_called_once_with(2)
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_log_max_limit(self, mock_logger, mock_git_service_class):
        """!git log 최대 제한"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_git_service.get_recent_commits.return_value = {'commits': []}
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_log(mock_ctx, n=100)
        
        # n > 20이면 20으로 제한
        mock_git_service.get_recent_commits.assert_called_once_with(20)
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_log_no_commits(self, mock_logger, mock_git_service_class):
        """!git log 커밋 없음"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_git_service.get_recent_commits.return_value = {'commits': []}
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_log(mock_ctx, n=5)
        
        call_args = mock_ctx.send.call_args[0][0]
        assert "커밋이 없습니다" in call_args
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_branch_success(self, mock_logger, mock_git_service_class):
        """!git branch 성공"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_git_service.get_branches_info.return_value = {
            'branches': ['main', 'develop', 'feature/test'],
            'current_branch': 'main'
        }
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_branch(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        call_args = mock_ctx.send.call_args
        assert isinstance(call_args[1]['embed'], discord.Embed)
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_branch_no_service(self, mock_logger, mock_git_service_class):
        """!git branch 서비스 없음"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service_class.side_effect = Exception("Error")
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '/invalid'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        
        await cog.git_branch(mock_ctx)
        
        call_args = mock_ctx.send.call_args[0][0]
        assert "저장소를 사용할 수 없습니다" in call_args
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_pull_success(self, mock_logger, mock_git_service_class):
        """!git pull 성공"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_git_service.sync_repository.return_value = {
            'result': '✅ Pull 완료'
        }
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        mock_ctx.typing = AsyncMock()
        mock_ctx.typing.__aenter__ = AsyncMock()
        mock_ctx.typing.__aexit__ = AsyncMock()
        
        await cog.git_pull(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        call_args = mock_ctx.send.call_args[0][0]
        assert "✅ Pull 완료" in call_args
    
    @pytest.mark.asyncio
    @patch('src.cogs.git_commands.GitService')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_git_pull_error(self, mock_logger, mock_git_service_class):
        """!git pull 에러"""
        mock_bot = MagicMock(spec=commands.Bot)
        mock_git_service = MagicMock()
        mock_git_service_class.return_value = mock_git_service
        
        mock_git_service.sync_repository.return_value = {
            'error': 'Network error'
        }
        
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        mock_ctx = AsyncMock(spec=commands.Context)
        mock_ctx.typing = AsyncMock()
        mock_ctx.typing.__aenter__ = AsyncMock()
        mock_ctx.typing.__aexit__ = AsyncMock()
        
        await cog.git_pull(mock_ctx)
        
        call_args = mock_ctx.send.call_args[0][0]
        assert "Network error" in call_args
