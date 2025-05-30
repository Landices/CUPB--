#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志配置模块
为应用程序提供统一的日志设置
"""

import os
import logging
from logging.handlers import RotatingFileHandler
import datetime

def setup_logger(log_dir=None, log_level=logging.INFO):
    """
    设置应用程序日志系统
    
    Args:
        log_dir: 日志存储目录，默认为应用根目录下的logs目录
        log_level: 日志级别，默认为INFO
        
    Returns:
        logging.Logger: 根日志记录器
    """
    # 如果没有指定日志目录，使用应用根目录下的logs目录
    if log_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        log_dir = os.path.join(base_dir, 'logs')
    
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 获取根日志记录器
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 清除现有的处理器，避免重复配置
    if logger.handlers:
        logger.handlers.clear()
    
    # 创建一个格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 配置文件处理器（使用当前日期作为文件名）
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f'gpa_calculator_{today}.log')
    
    # 使用RotatingFileHandler控制日志文件大小
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 记录日志系统启动
    logger.info("日志系统已初始化")
    
    return logger 