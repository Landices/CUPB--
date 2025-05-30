#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CUPB绩点计算器启动脚本
处理命令行参数、检查环境并启动应用程序
"""

import os
import sys
import argparse
import logging
import platform
import traceback
from typing import Optional

# 设置日志目录
if not os.path.exists('logs'):
    os.makedirs('logs')

# 配置基本日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'startup.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("startup")

def check_python_version() -> bool:
    """
    检查Python版本是否满足要求
    
    Returns:
        bool: 版本是否满足要求
    """
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version < required_version:
        logger.error(f"Python版本不满足要求: 需要Python {required_version[0]}.{required_version[1]}或更高版本")
        print(f"错误: 需要Python {required_version[0]}.{required_version[1]}或更高版本")
        print(f"当前版本: Python {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return False
    
    logger.info(f"Python版本检查通过: {sys.version}")
    return True

def check_dependencies() -> bool:
    """
    检查必要的依赖是否已安装
    
    Returns:
        bool: 依赖是否满足要求
    """
    required_packages = ['pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    # 检查是否需要GUI依赖
    if '--console' not in sys.argv:
        try:
            __import__('PyQt5')
        except ImportError:
            missing_packages.append('PyQt5')
    
    if missing_packages:
        logger.error(f"缺少必要的依赖: {', '.join(missing_packages)}")
        print(f"错误: 缺少必要的依赖: {', '.join(missing_packages)}")
        print("请运行以下命令安装依赖:")
        print(f"pip install {' '.join(missing_packages)}")
        
        # 提供安装脚本信息
        if platform.system() == "Windows":
            print("\n或者运行 install_deps.bat 脚本自动安装依赖")
        else:
            print("\n或者运行 ./install_deps.sh 脚本自动安装依赖")
            
        return False
    
    logger.info("依赖检查通过")
    return True

def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='CUPB绩点计算器')
    parser.add_argument('--console', action='store_true', help='使用命令行界面')
    parser.add_argument('--gui', action='store_true', help='使用图形用户界面')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--file', type=str, help='指定Excel文件路径')
    
    return parser.parse_args()

def main():
    """主函数"""
    try:
        # 检查Python版本
        if not check_python_version():
            return 1
        
        # 检查依赖
        if not check_dependencies():
            return 1
        
        # 解析命令行参数
        args = parse_arguments()
        
        # 设置日志级别
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("已启用调试模式")
        
        # 导入主程序
        try:
            from src.main import main as run_main
            
            # 清空命令行参数，避免重复解析
            sys.argv = [sys.argv[0]]
            
            # 设置命令行参数
            if args.console:
                sys.argv.append('--console')
            if args.gui:
                sys.argv.append('--gui')
            if args.debug:
                sys.argv.append('--debug')
            if args.file:
                sys.argv.append('--file')
                sys.argv.append(args.file)
            
            # 运行主程序
            logger.info("启动主程序")
            return run_main()
            
        except ImportError as e:
            logger.error(f"导入主程序失败: {str(e)}")
            print(f"错误: 导入主程序失败: {str(e)}")
            print("请确保您在正确的目录中运行此脚本")
            return 1
            
    except Exception as e:
        logger.error(f"启动过程中发生未知错误: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"错误: 启动过程中发生未知错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 