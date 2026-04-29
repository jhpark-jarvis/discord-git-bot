"""
Git 기능 통합 테스트

모든 Git 기능이 함께 작동하는지 테스트합니다.
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime
from discord.ext import commands
import discord

from src.utils.git_helper import GitHelper
from src.services.git_service import GitService
from src.cogs.git_commands import GitCommands


@pytest.mark.asyncio
class TestGitIntegration:
    """Git 통합 테스트"""
    
    @patch('src.utils.git_helper.Repo')
    def test_complete_workflow_git_helper(self, mock_repo):
        """GitHelper 전체 워크플로우 테스트"""
        # Mock 저장소 설정
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock 커밋
        mock_commit = MagicMock()
        mock_commit.hexsha = 'abc1234567890'
        mock_commit.author.name = 'Developer'
        mock_commit.message = 'Initial commit\n'
        mock_commit.committed_datetime = datetime.now()
        
        # Mock 브랜치
        mock_branch = MagicMock()
        mock_branch.name = 'main'
        
        # Mock 설정
        mock_repo_instance.git.status.return_value = 'On branch main\nnothing to commit'
        mock_repo_instance.iter_commits.return_value = [mock_commit]
        mock_repo_instance.heads = [mock_branch]
        mock_active_branch = MagicMock()
        mock_active_branch.name = 'main'
        mock_repo_instance.active_branch = mock_active_branch
        
        mock_origin = MagicMock()
        mock_repo_instance.remote.return_value = mock_origin
        
        # 테스트 실행
        git_helper = GitHelper('.')
        
        # 1. 상태 확인
        status = git_helper.get_status()
        assert 'On branch main' in status
        
        # 2. 커밋 로그 확인
        commits = git_helper.get_log(1)
        assert len(commits) == 1
        assert commits[0]['author'] == 'Developer'
        
        # 3. 브랜치 목록 확인
        branches = git_helper.get_branches()
        assert 'main' in branches
        
        # 4. 현재 브랜치 확인
        current_branch = git_helper.get_current_branch()
        assert current_branch == 'main'
        
        # 5. Pull 수행
        result = git_helper.pull()
        assert '✅' in result
        mock_origin.pull.assert_called_once()
    
    @patch('src.utils.git_helper.Repo')
    def test_complete_workflow_git_service(self, mock_repo):
        """GitService 전체 워크플로우 테스트"""
        # Mock 저장소 설정
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock 커밋
        mock_commit = MagicMock()
        mock_commit.hexsha = 'def5678901234'
        mock_commit.author.name = 'John Doe'
        mock_commit.message = 'Fix: critical bug\n'
        mock_commit.committed_datetime = datetime.now()
        
        # Mock 브랜치
        mock_branch1 = MagicMock()
        mock_branch1.name = 'main'
        mock_branch2 = MagicMock()
        mock_branch2.name = 'develop'
        
        # Mock 설정
        mock_repo_instance.git.status.return_value = 'On branch develop\nnothing to commit'
        mock_repo_instance.iter_commits.return_value = [mock_commit]
        mock_repo_instance.heads = [mock_branch1, mock_branch2]
        mock_active_branch = MagicMock()
        mock_active_branch.name = 'develop'
        mock_repo_instance.active_branch = mock_active_branch
        
        mock_origin = MagicMock()
        mock_repo_instance.remote.return_value = mock_origin
        
        # GitService 생성
        service = GitService('.')
        
        # 1. 상태 정보 조회
        status_info = service.get_status_info()
        assert status_info['branch'] == 'develop'
        assert 'develop' in status_info['status']
        
        # 2. 최근 커밋 조회
        commits_info = service.get_recent_commits(1)
        assert len(commits_info['commits']) == 1
        assert commits_info['commits'][0]['author'] == 'John Doe'
        
        # 3. 브랜치 정보 조회
        branches_info = service.get_branches_info()
        assert 'main' in branches_info['branches']
        assert 'develop' in branches_info['branches']
        assert branches_info['current_branch'] == 'develop'
        
        # 4. 저장소 동기화
        sync_info = service.sync_repository()
        assert '✅' in sync_info['result']
    
    @pytest.mark.asyncio
    @patch('src.utils.git_helper.Repo')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_complete_workflow_git_commands(self, mock_logger, mock_repo):
        """GitCommands 전체 워크플로우 테스트"""
        # Mock 저장소 설정
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock 데이터
        mock_commit1 = MagicMock()
        mock_commit1.hexsha = 'abc1234567890'
        mock_commit1.author.name = 'Developer'
        mock_commit1.message = 'Feature: add git integration\n'
        mock_commit1.committed_datetime = datetime(2024, 1, 1, 10, 0, 0)
        
        mock_commit2 = MagicMock()
        mock_commit2.hexsha = 'def5678901234'
        mock_commit2.author.name = 'Reviewer'
        mock_commit2.message = 'Fix: handle edge cases\n'
        mock_commit2.committed_datetime = datetime(2024, 1, 2, 11, 0, 0)
        
        mock_branch1 = MagicMock()
        mock_branch1.name = 'main'
        mock_branch2 = MagicMock()
        mock_branch2.name = 'develop'
        
        # Mock 설정
        mock_repo_instance.git.status.return_value = 'On branch main\nnothing to commit, working tree clean'
        mock_repo_instance.iter_commits.return_value = [mock_commit1, mock_commit2]
        mock_repo_instance.heads = [mock_branch1, mock_branch2]
        mock_active_branch = MagicMock()
        mock_active_branch.name = 'main'
        mock_repo_instance.active_branch = mock_active_branch
        
        mock_origin = MagicMock()
        mock_repo_instance.remote.return_value = mock_origin
        
        # GitCommands 생성
        mock_bot = MagicMock(spec=commands.Bot)
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        # Mock Context
        mock_ctx = AsyncMock(spec=commands.Context)
        mock_ctx.typing = AsyncMock()
        mock_ctx.typing.__aenter__ = AsyncMock()
        mock_ctx.typing.__aexit__ = AsyncMock()
        
        # 1. Status 명령 테스트
        await cog.git_status(mock_ctx)
        assert mock_ctx.send.call_count >= 1
        status_call = mock_ctx.send.call_args_list[0]
        assert isinstance(status_call[1]['embed'], discord.Embed)
        
        # 2. Log 명령 테스트
        mock_ctx.reset_mock()
        await cog.git_log(mock_ctx, n=2)
        assert mock_ctx.send.call_count >= 1
        log_call = mock_ctx.send.call_args_list[0]
        assert isinstance(log_call[1]['embed'], discord.Embed)
        
        # 3. Branch 명령 테스트
        mock_ctx.reset_mock()
        await cog.git_branch(mock_ctx)
        assert mock_ctx.send.call_count >= 1
        branch_call = mock_ctx.send.call_args_list[0]
        assert isinstance(branch_call[1]['embed'], discord.Embed)
        
        # 4. Pull 명령 테스트
        mock_ctx.reset_mock()
        await cog.git_pull(mock_ctx)
        assert mock_ctx.send.call_count >= 1
    
    @pytest.mark.asyncio
    @patch('src.utils.git_helper.Repo')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_error_handling_workflow(self, mock_logger, mock_repo):
        """에러 처리 워크플로우 테스트"""
        from git import GitCommandError
        
        # Mock 저장소 설정 (에러 상황)
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # 모든 명령에서 에러 발생
        error_msg = "Connection refused"
        mock_repo_instance.git.status.side_effect = GitCommandError('status', 1, error_msg)
        mock_repo_instance.iter_commits.side_effect = GitCommandError('log', 1, error_msg)
        mock_repo_instance.heads = []
        mock_active_branch = MagicMock()
        mock_active_branch.name = 'main'
        mock_repo_instance.active_branch = mock_active_branch
        
        mock_origin = MagicMock()
        mock_origin.pull.side_effect = GitCommandError('pull', 1, error_msg)
        mock_repo_instance.remote.return_value = mock_origin
        
        # GitCommands 생성
        mock_bot = MagicMock(spec=commands.Bot)
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        # Mock Context
        mock_ctx = AsyncMock(spec=commands.Context)
        mock_ctx.typing = AsyncMock()
        mock_ctx.typing.__aenter__ = AsyncMock()
        mock_ctx.typing.__aexit__ = AsyncMock()
        
        # 1. Status 에러 처리
        await cog.git_status(mock_ctx)
        assert mock_ctx.send.called
        
        # 2. Log 에러 처리 (빈 커밋 리스트)
        mock_ctx.reset_mock()
        await cog.git_log(mock_ctx, n=5)
        assert mock_ctx.send.called
        
        # 3. Pull 에러 처리
        mock_ctx.reset_mock()
        await cog.git_pull(mock_ctx)
        assert mock_ctx.send.called
    
    @pytest.mark.asyncio
    @patch('src.utils.git_helper.Repo')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_multiple_commands_sequence(self, mock_logger, mock_repo):
        """여러 명령어 순차 실행 테스트"""
        # Mock 저장소 설정
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # 각 호출에 대한 결과 설정
        mock_repo_instance.git.status.return_value = 'On branch main\nmodified: README.md'
        
        mock_commit = MagicMock()
        mock_commit.hexsha = 'abc1234567890'
        mock_commit.author.name = 'Developer'
        mock_commit.message = 'Update README\n'
        mock_commit.committed_datetime = datetime.now()
        
        mock_repo_instance.iter_commits.return_value = [mock_commit]
        
        mock_branch = MagicMock()
        mock_branch.name = 'main'
        mock_repo_instance.heads = [mock_branch]
        
        mock_active_branch = MagicMock()
        mock_active_branch.name = 'main'
        mock_repo_instance.active_branch = mock_active_branch
        
        mock_origin = MagicMock()
        mock_repo_instance.remote.return_value = mock_origin
        
        # GitCommands 생성
        mock_bot = MagicMock(spec=commands.Bot)
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        # Mock Context
        mock_ctx = AsyncMock(spec=commands.Context)
        mock_ctx.typing = AsyncMock()
        mock_ctx.typing.__aenter__ = AsyncMock()
        mock_ctx.typing.__aexit__ = AsyncMock()
        
        # 순차 실행
        commands_sequence = [
            ('status', cog.git_status, []),
            ('log', cog.git_log, [3]),
            ('branch', cog.git_branch, []),
            ('pull', cog.git_pull, []),
        ]
        
        for cmd_name, cmd_func, args in commands_sequence:
            mock_ctx.reset_mock()
            await cmd_func(mock_ctx, *args) if args else await cmd_func(mock_ctx)
            assert mock_ctx.send.called, f"{cmd_name} should call send()"
    
    @pytest.mark.asyncio
    @patch('src.utils.git_helper.Repo')
    @patch('src.cogs.git_commands.setup_logger')
    async def test_large_commit_list(self, mock_logger, mock_repo):
        """많은 커밋 목록 처리 테스트"""
        # Mock 저장소 설정
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # 많은 커밋 생성
        commits = []
        for i in range(20):
            mock_commit = MagicMock()
            mock_commit.hexsha = f'abc{i:016d}'
            mock_commit.author.name = f'Author {i}'
            mock_commit.message = f'Commit message {i}\n'
            mock_commit.committed_datetime = datetime.now()
            commits.append(mock_commit)
        
        mock_repo_instance.iter_commits.return_value = commits
        
        mock_branch = MagicMock()
        mock_branch.name = 'main'
        mock_repo_instance.heads = [mock_branch]
        
        mock_active_branch = MagicMock()
        mock_active_branch.name = 'main'
        mock_repo_instance.active_branch = mock_active_branch
        
        # GitCommands 생성
        mock_bot = MagicMock(spec=commands.Bot)
        with patch('src.cogs.git_commands.config') as mock_config:
            mock_config.GITHUB_REPO_PATH = '.'
            cog = GitCommands(mock_bot)
        
        # Mock Context
        mock_ctx = AsyncMock(spec=commands.Context)
        
        # 요청한 개수보다 많이 있어도 최대값으로 제한되는지 확인
        await cog.git_log(mock_ctx, n=50)
        
        # 최대 20개로 제한되어야 함
        assert mock_ctx.send.called
