"""
테스트 실행 유틸리티 모듈

테스트를 실행하고 결과를 수집합니다.
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Callable
import logging

logger = logging.getLogger(__name__)


class TestRunner:
    """테스트 실행 및 결과 수집 클래스"""
    
    def __init__(self, project_root: str = None):
        """
        초기화
        
        Args:
            project_root: 프로젝트 루트 디렉토리
        """
        if project_root is None:
            project_root = str(Path(__file__).parent.parent.parent)
        self.project_root = Path(project_root)
        self.tests_dir = self.project_root / "tests"
    
    def run_all_tests(self, callback: Callable = None) -> Dict[str, Any]:
        """
        모든 테스트 실행
        
        Args:
            callback: 진행사항 콜백 함수 (메시지 전달용)
        
        Returns:
            테스트 결과 딕셔너리
        """
        return self._run_pytest(
            "-v",
            callback=callback,
            description="모든 테스트 실행 중..."
        )
    
    def run_unit_tests(self, callback: Callable = None) -> Dict[str, Any]:
        """
        유닛 테스트만 실행
        
        Args:
            callback: 진행사항 콜백 함수
        
        Returns:
            테스트 결과 딕셔너리
        """
        return self._run_pytest(
            "-v",
            "-m", "not integration",
            callback=callback,
            description="유닛 테스트 실행 중..."
        )
    
    def run_integration_tests(self, callback: Callable = None) -> Dict[str, Any]:
        """
        통합 테스트만 실행
        
        Args:
            callback: 진행사항 콜백 함수
        
        Returns:
            테스트 결과 딕셔너리
        """
        return self._run_pytest(
            "-v",
            "-m", "integration",
            callback=callback,
            description="통합 테스트 실행 중..."
        )
    
    def run_specific_test(self, test_name: str, callback: Callable = None) -> Dict[str, Any]:
        """
        특정 테스트 파일 실행
        
        Args:
            test_name: 테스트 파일 이름 (확장자 제외)
            callback: 진행사항 콜백 함수
        
        Returns:
            테스트 결과 딕셔너리
        """
        test_file = self.tests_dir / f"{test_name}.py"
        if not test_file.exists():
            return {
                "success": False,
                "error": f"테스트 파일을 찾을 수 없습니다: {test_name}",
                "passed": 0,
                "failed": 0,
                "total": 0
            }
        
        return self._run_pytest(
            str(test_file),
            "-v",
            callback=callback,
            description=f"{test_name} 테스트 실행 중..."
        )
    
    def _run_pytest(self, *args, callback: Callable = None, description: str = "") -> Dict[str, Any]:
        """
        pytest 실행
        
        Args:
            *args: pytest 인자
            callback: 진행사항 콜백 함수
            description: 설명 메시지
        
        Returns:
            테스트 결과 딕셔너리
        """
        if callback:
            callback(f"시작: {description}")
        
        try:
            # pytest 명령 구성
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                str(self.tests_dir),
                "--tb=short",
                "--no-header",
                "-q"
            ]
            cmd.extend(args)
            
            logger.info(f"테스트 명령 실행: {' '.join(cmd)}")
            
            # pytest 실행
            result = subprocess.run(
                cmd,
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # 결과 파싱
            output = result.stdout + result.stderr
            
            # 간단한 통계 추출
            summary = self._parse_pytest_output(output)
            summary["success"] = result.returncode == 0
            summary["returncode"] = result.returncode
            summary["output"] = output
            
            if callback:
                status = "완료" if summary["success"] else "실패"
                callback(
                    f"{status}: {summary['passed']} 통과 / "
                    f"{summary['failed']} 실패 / {summary['total']} 총계"
                )
            
            return summary
            
        except subprocess.TimeoutExpired:
            error_msg = "테스트 실행 시간 초과 (120초)"
            logger.error(error_msg)
            if callback:
                callback(f"오류: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "passed": 0,
                "failed": 0,
                "total": 0,
                "output": ""
            }
        except Exception as e:
            error_msg = f"테스트 실행 중 오류: {str(e)}"
            logger.error(error_msg)
            if callback:
                callback(f"오류: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "passed": 0,
                "failed": 0,
                "total": 0,
                "output": ""
            }
    
    def _parse_pytest_output(self, output: str) -> Dict[str, Any]:
        """
        pytest 출력 파싱
        
        Args:
            output: pytest 출력
        
        Returns:
            파싱된 결과 딕셔너리
        """
        result = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "total": 0,
            "tests": []
        }
        
        lines = output.split("\n")
        
        # 마지막 몇 줄에서 요약 정보 추출
        for line in lines[-10:]:
            if "passed" in line:
                try:
                    # "41 passed in 2.07s" 형식 파싱
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            result["passed"] = int(parts[i-1])
                        elif part == "failed":
                            result["failed"] = int(parts[i-1])
                        elif part == "error":
                            result["errors"] = int(parts[i-1])
                        elif part == "skipped":
                            result["skipped"] = int(parts[i-1])
                except:
                    pass
        
        result["total"] = result["passed"] + result["failed"] + result["errors"]
        
        # 개별 테스트 결과 추출
        for line in lines:
            if "PASSED" in line or "FAILED" in line or "ERROR" in line:
                test_info = self._parse_test_line(line)
                if test_info:
                    result["tests"].append(test_info)
        
        return result
    
    def _parse_test_line(self, line: str) -> Dict[str, str]:
        """
        개별 테스트 라인 파싱
        
        Args:
            line: pytest 테스트 결과 라인
        
        Returns:
            파싱된 테스트 정보
        """
        if "::" not in line:
            return None
        
        try:
            parts = line.split("::")
            if len(parts) >= 2:
                test_name = parts[-1].split()[0]
                
                if "PASSED" in line:
                    status = "PASSED"
                elif "FAILED" in line:
                    status = "FAILED"
                elif "ERROR" in line:
                    status = "ERROR"
                else:
                    status = "UNKNOWN"
                
                return {
                    "name": test_name,
                    "status": status,
                    "file": parts[0]
                }
        except:
            pass
        
        return None


def create_test_result_embed(result: Dict[str, Any], test_type: str = "모든") -> Dict[str, Any]:
    """
    Discord embed용 테스트 결과 생성
    
    Args:
        result: 테스트 결과 딕셔너리
        test_type: 테스트 타입 (모든/유닛/통합)
    
    Returns:
        Discord embed 데이터
    """
    success = result.get("success", False)
    passed = result.get("passed", 0)
    failed = result.get("failed", 0)
    total = result.get("total", 0)
    
    if success:
        color = 0x00ff00  # 녹색
        status = "성공"
    else:
        color = 0xff0000  # 빨강
        status = "실패"
    
    embed = {
        "title": f"{test_type} 테스트 - {status}",
        "description": f"총 {total}개 테스트 중 {passed}개 통과",
        "color": color,
        "fields": [
            {"name": "통과", "value": str(passed), "inline": True},
            {"name": "실패", "value": str(failed), "inline": True},
            {"name": "총계", "value": str(total), "inline": True}
        ]
    }
    
    # 테스트 목록 추가 (최대 25개 필드)
    tests = result.get("tests", [])
    if tests:
        test_list = "\n".join([
            f"{'✓' if t.get('status') == 'PASSED' else '✗'} {t.get('name', 'Unknown')}"
            for t in tests[:10]  # 처음 10개만 표시
        ])
        if len(tests) > 10:
            test_list += f"\n... 외 {len(tests) - 10}개"
        
        embed["fields"].append({
            "name": "테스트 결과",
            "value": test_list if test_list else "없음",
            "inline": False
        })
    
    # 오류 정보 추가
    if "error" in result:
        embed["fields"].append({
            "name": "오류",
            "value": result["error"][:256],
            "inline": False
        })
    
    return embed
