"""
로깅 설정 모듈

봇의 로깅을 관리합니다.
"""

import logging
from pathlib import Path
from typing import Optional

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    로거 설정
    
    Args:
        name: 로거 이름 (__name__)
        level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        설정된 로거 객체
    """
    from .. import config
    
    logger = logging.getLogger(name)
    log_level = getattr(logging, level or config.LOG_LEVEL)
    logger.setLevel(log_level)
    
    # 로그 파일 핸들러
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(log_level)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # 로그 포매터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
