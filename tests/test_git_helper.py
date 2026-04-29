"""
GitHelper 클래스 유닛테스트

Git 헬퍼의 각 메서드를 모의 객체로 테스트합니다.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from pathlib import Path

from src.utils.git_helper import GitHelper


class TestGitHelper:
    """GitHelper 클래스 테스트"""
    
    @patch('src.utils.git_helper.Repo')
    def test_init_repo_success(self, mock_repo):
        """저장소 초기화 성공"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        git_helper = GitHelper('.')
        
        assert git_helper.repo is not None
        assert git_helper.repo_path == Path('.')
    
    @patch('src.utils.git_helper.Repo')
    def test_init_repo_invalid_repository(self, mock_repo):
        """유효하지 않은 저장소 에러 처리"""
        from git import InvalidGitRepositoryError
        mock_repo.side_effect = InvalidGitRepositoryError()
        
        with pytest.raises(InvalidGitRepositoryError):
            GitHelper('/invalid/path')
    
    @patch('src.utils.git_helper.Repo')
    def test_get_status_success(self, mock_repo):
        """저장소 상태 조회 성공"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        expected_status = "On branch main\nnothing to commit, working tree clean"
        mock_repo_instance.git.status.return_value = expected_status
        
        git_helper = GitHelper('.')
        status = git_helper.get_status()
        
        assert status == expected_status
        mock_repo_instance.git.status.assert_called_once()
    
    @patch('src.utils.git_helper.Repo')
    def test_get_status_error(self, mock_repo):
        """저장소 상태 조회 에러 처리"""
        from git import GitCommandError
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        error_msg = "fatal: not a git repository"
        mock_repo_instance.git.status.side_effect = GitCommandError('status', 128, error_msg)
        
        git_helper = GitHelper('.')
        status = git_helper.get_status()
        
        assert "오류" in status
    
    @patch('src.utils.git_helper.Repo')
    def test_get_status_no_repo(self, mock_repo):
        """저장소 없음"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        git_helper = GitHelper('.')
        git_helper.repo = None
        status = git_helper.get_status()
        
        assert status == "저장소 없음"
    
    @patch('src.utils.git_helper.Repo')
    def test_get_log_success(self, mock_repo):
        """커밋 로그 조회 성공"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock 커밋 생성
        mock_commit1 = MagicMock()
        mock_commit1.hexsha = 'abc1234567890def'
        mock_commit1.author.name = 'John Doe'
        mock_commit1.message = 'Fix: bug in git helper\n'
        mock_commit1.committed_datetime = datetime(2024, 1, 1, 10, 0, 0)
        
        mock_commit2 = MagicMock()
        mock_commit2.hexsha = 'def9876543210abc'
        mock_commit2.author.name = 'Jane Smith'
        mock_commit2.message = 'Feat: add new feature\n'
        mock_commit2.committed_datetime = datetime(2024, 1, 2, 11, 0, 0)
        
        mock_repo_instance.iter_commits.return_value = [mock_commit1, mock_commit2]
        
        git_helper = GitHelper('.')
        commits = git_helper.get_log(2)
        
        assert len(commits) == 2
        assert commits[0]['hash'] == 'abc1234'
        assert commits[0]['author'] == 'John Doe'
        assert commits[0]['message'] == 'Fix: bug in git helper'
        assert commits[1]['hash'] == 'def98765'
        assert commits[1]['author'] == 'Jane Smith'
    
    @patch('src.utils.git_helper.Repo')
    def test_get_log_error(self, mock_repo):
        """커밋 로그 조회 에러 처리"""
        from git import GitCommandError
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        mock_repo_instance.iter_commits.side_effect = GitCommandError('log', 128)
        
        git_helper = GitHelper('.')
        commits = git_helper.get_log(5)
        
        assert commits == []
    
    @patch('src.utils.git_helper.Repo')
    def test_get_log_no_repo(self, mock_repo):
        """저장소 없음"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        git_helper = GitHelper('.')
        git_helper.repo = None
        commits = git_helper.get_log(5)
        
        assert commits == []
    
    @patch('src.utils.git_helper.Repo')
    def test_get_branches_success(self, mock_repo):
        """브랜치 목록 조회 성공"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock 브랜치 생성
        mock_branch1 = MagicMock()
        mock_branch1.name = 'main'
        mock_branch2 = MagicMock()
        mock_branch2.name = 'develop'
        mock_branch3 = MagicMock()
        mock_branch3.name = 'feature/test'
        
        mock_repo_instance.heads = [mock_branch1, mock_branch2, mock_branch3]
        
        git_helper = GitHelper('.')
        branches = git_helper.get_branches()
        
        assert len(branches) == 3
        assert 'main' in branches
        assert 'develop' in branches
        assert 'feature/test' in branches
    
    @patch('src.utils.git_helper.Repo')
    def test_get_branches_error(self, mock_repo):
        """브랜치 목록 조회 에러 처리"""
        from git import GitCommandError
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        mock_repo_instance.heads = MagicMock()
        type(mock_repo_instance).heads = MagicMock(side_effect=GitCommandError('branch', 128))
        
        git_helper = GitHelper('.')
        branches = git_helper.get_branches()
        
        assert branches == []
    
    @patch('src.utils.git_helper.Repo')
    def test_get_current_branch_success(self, mock_repo):
        """현재 브랜치명 조회 성공"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        mock_active_branch = MagicMock()
        mock_active_branch.name = 'main'
        mock_repo_instance.active_branch = mock_active_branch
        
        git_helper = GitHelper('.')
        branch = git_helper.get_current_branch()
        
        assert branch == 'main'
    
    @patch('src.utils.git_helper.Repo')
    def test_get_current_branch_error(self, mock_repo):
        """현재 브랜치명 조회 에러 처리"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        type(mock_repo_instance).active_branch = MagicMock(side_effect=Exception("Detached HEAD"))
        
        git_helper = GitHelper('.')
        branch = git_helper.get_current_branch()
        
        assert branch == "unknown"
    
    @patch('src.utils.git_helper.Repo')
    def test_get_current_branch_no_repo(self, mock_repo):
        """저장소 없음"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        git_helper = GitHelper('.')
        git_helper.repo = None
        branch = git_helper.get_current_branch()
        
        assert branch == "unknown"
    
    @patch('src.utils.git_helper.Repo')
    def test_pull_success(self, mock_repo):
        """저장소 동기화 성공"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        mock_origin = MagicMock()
        mock_repo_instance.remote.return_value = mock_origin
        
        git_helper = GitHelper('.')
        result = git_helper.pull()
        
        assert result == "✅ Pull 완료"
        mock_origin.pull.assert_called_once()
    
    @patch('src.utils.git_helper.Repo')
    def test_pull_error(self, mock_repo):
        """저장소 동기화 에러 처리"""
        from git import GitCommandError
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        mock_origin = MagicMock()
        mock_origin.pull.side_effect = GitCommandError('pull', 1, "Network error")
        mock_repo_instance.remote.return_value = mock_origin
        
        git_helper = GitHelper('.')
        result = git_helper.pull()
        
        assert "❌ Pull 실패" in result
    
    @patch('src.utils.git_helper.Repo')
    def test_pull_no_repo(self, mock_repo):
        """저장소 없음"""
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        git_helper = GitHelper('.')
        git_helper.repo = None
        result = git_helper.pull()
        
        assert result == "저장소 없음"
