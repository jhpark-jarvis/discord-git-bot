"""
GitService 클래스 유닛테스트

Git 서비스의 각 메서드를 모의 객체로 테스트합니다.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch

from src.services.git_service import GitService


class TestGitService:
    """GitService 클래스 테스트"""
    
    @patch('src.services.git_service.GitHelper')
    def test_init_success(self, mock_git_helper_class):
        """서비스 초기화 성공"""
        mock_git_helper = MagicMock()
        mock_git_helper_class.return_value = mock_git_helper
        
        service = GitService('.')
        
        assert service.git_helper is not None
        mock_git_helper_class.assert_called_once_with('.')
    
    @patch('src.services.git_service.GitHelper')
    def test_init_error(self, mock_git_helper_class):
        """서비스 초기화 실패"""
        mock_git_helper_class.side_effect = Exception("Invalid path")
        
        service = GitService('/invalid/path')
        
        assert service.git_helper is None
    
    @patch('src.services.git_service.GitHelper')
    def test_get_status_info_success(self, mock_git_helper_class):
        """저장소 상태 정보 조회 성공"""
        mock_git_helper = MagicMock()
        mock_git_helper_class.return_value = mock_git_helper
        
        mock_git_helper.get_current_branch.return_value = 'main'
        mock_git_helper.get_status.return_value = 'On branch main\nnothing to commit'
        
        service = GitService('.')
        info = service.get_status_info()
        
        assert info['branch'] == 'main'
        assert 'nothing to commit' in info['status']
        mock_git_helper.get_current_branch.assert_called_once()
        mock_git_helper.get_status.assert_called_once()
    
    @patch('src.services.git_service.GitHelper')
    def test_get_status_info_no_helper(self, mock_git_helper_class):
        """Git 헬퍼 없음"""
        mock_git_helper_class.side_effect = Exception("Error")
        
        service = GitService('.')
        info = service.get_status_info()
        
        assert "error" in info
        assert info['error'] == "저장소를 사용할 수 없습니다"
    
    @patch('src.services.git_service.GitHelper')
    def test_get_recent_commits_success(self, mock_git_helper_class):
        """최근 커밋 조회 성공"""
        mock_git_helper = MagicMock()
        mock_git_helper_class.return_value = mock_git_helper
        
        mock_commits = [
            {
                'hash': 'abc1234',
                'author': 'John Doe',
                'message': 'Fix: bug',
                'date': '2024-01-01T10:00:00'
            },
            {
                'hash': 'def5678',
                'author': 'Jane Smith',
                'message': 'Feat: new feature',
                'date': '2024-01-02T11:00:00'
            }
        ]
        mock_git_helper.get_log.return_value = mock_commits
        
        service = GitService('.')
        info = service.get_recent_commits(2)
        
        assert len(info['commits']) == 2
        assert info['commits'][0]['author'] == 'John Doe'
        assert info['commits'][1]['author'] == 'Jane Smith'
        mock_git_helper.get_log.assert_called_once_with(2)
    
    @patch('src.services.git_service.GitHelper')
    def test_get_recent_commits_no_helper(self, mock_git_helper_class):
        """Git 헬퍼 없음"""
        mock_git_helper_class.side_effect = Exception("Error")
        
        service = GitService('.')
        info = service.get_recent_commits(5)
        
        assert "error" in info
        assert info['commits'] == []
    
    @patch('src.services.git_service.GitHelper')
    def test_get_recent_commits_empty(self, mock_git_helper_class):
        """커밋 없음"""
        mock_git_helper = MagicMock()
        mock_git_helper_class.return_value = mock_git_helper
        
        mock_git_helper.get_log.return_value = []
        
        service = GitService('.')
        info = service.get_recent_commits(5)
        
        assert info['commits'] == []
    
    @patch('src.services.git_service.GitHelper')
    def test_get_branches_info_success(self, mock_git_helper_class):
        """브랜치 정보 조회 성공"""
        mock_git_helper = MagicMock()
        mock_git_helper_class.return_value = mock_git_helper
        
        mock_git_helper.get_branches.return_value = ['main', 'develop', 'feature/test']
        mock_git_helper.get_current_branch.return_value = 'main'
        
        service = GitService('.')
        info = service.get_branches_info()
        
        assert len(info['branches']) == 3
        assert info['current_branch'] == 'main'
        assert 'develop' in info['branches']
    
    @patch('src.services.git_service.GitHelper')
    def test_get_branches_info_no_helper(self, mock_git_helper_class):
        """Git 헬퍼 없음"""
        mock_git_helper_class.side_effect = Exception("Error")
        
        service = GitService('.')
        info = service.get_branches_info()
        
        assert "error" in info
        assert info['branches'] == []
    
    @patch('src.services.git_service.GitHelper')
    def test_sync_repository_success(self, mock_git_helper_class):
        """저장소 동기화 성공"""
        mock_git_helper = MagicMock()
        mock_git_helper_class.return_value = mock_git_helper
        
        mock_git_helper.pull.return_value = "✅ Pull 완료"
        
        service = GitService('.')
        info = service.sync_repository()
        
        assert info['result'] == "✅ Pull 완료"
        mock_git_helper.pull.assert_called_once()
    
    @patch('src.services.git_service.GitHelper')
    def test_sync_repository_error(self, mock_git_helper_class):
        """저장소 동기화 실패"""
        mock_git_helper = MagicMock()
        mock_git_helper_class.return_value = mock_git_helper
        
        mock_git_helper.pull.return_value = "❌ Pull 실패: Network error"
        
        service = GitService('.')
        info = service.sync_repository()
        
        assert "❌ Pull 실패" in info['result']
    
    @patch('src.services.git_service.GitHelper')
    def test_sync_repository_no_helper(self, mock_git_helper_class):
        """Git 헬퍼 없음"""
        mock_git_helper_class.side_effect = Exception("Error")
        
        service = GitService('.')
        info = service.sync_repository()
        
        assert "error" in info
