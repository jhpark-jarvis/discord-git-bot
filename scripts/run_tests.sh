#!/bin/bash

# 모든 테스트 실행 스크립트 (Linux/macOS)
# 사용법: ./run_tests.sh [all|unit|integration]

# 테스트 타입 결정
TEST_TYPE=${1:-all}

# 프로젝트 루트
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}====================================${NC}"
echo -e "${GREEN}테스트 실행: $TEST_TYPE${NC}"
echo -e "${CYAN}====================================${NC}"
echo ""

# 테스트 타입별 실행
case $TEST_TYPE in
    all)
        echo -e "${YELLOW}모든 테스트를 실행합니다...${NC}"
        python -m pytest tests/ -v --tb=short
        ;;
    unit)
        echo -e "${YELLOW}유닛 테스트를 실행합니다...${NC}"
        python -m pytest tests/ -v -m "not integration" --tb=short
        ;;
    integration)
        echo -e "${YELLOW}통합 테스트를 실행합니다...${NC}"
        python -m pytest tests/ -v -m "integration" --tb=short
        ;;
    *)
        echo -e "${YELLOW}특정 테스트를 실행합니다: test_$TEST_TYPE${NC}"
        python -m pytest "tests/test_$TEST_TYPE.py" -v --tb=short
        ;;
esac

TEST_RESULT=$?

echo ""
echo -e "${CYAN}====================================${NC}"
echo -e "${GREEN}테스트 완료${NC}"
echo -e "${CYAN}====================================${NC}"

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}모든 테스트가 통과했습니다!${NC}"
else
    echo -e "${RED}일부 테스트가 실패했습니다.${NC}"
fi

echo ""
exit $TEST_RESULT
