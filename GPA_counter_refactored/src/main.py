#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绩点计算器主程序
支持命令行界面和图形界面
"""

import os
import sys
import logging
import argparse
import traceback
from typing import Optional, Union

# 导入自定义模块
from .utils.logger import setup_logger
from .utils.calculator import GpaCalculator
from .utils.data_loader import DataLoader
from .utils.persistence import DataPersistence
from .ui.console_ui import ConsoleUI

# 可选的GUI界面导入
try:
    from .ui.gui import GUIApplication
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='绩点计算器')
    parser.add_argument('--console', action='store_true', help='使用命令行界面')
    parser.add_argument('--gui', action='store_true', help='使用图形用户界面')
    parser.add_argument('--debug', action='store_true', help='启用调试日志')
    parser.add_argument('--file', type=str, help='直接指定Excel文件路径')
    
    return parser.parse_args()

def main():
    """
    程序入口点
    """
    try:
        # 解析命令行参数
        args = parse_arguments()
        
        # 设置日志级别
        log_level = logging.DEBUG if args.debug else logging.INFO
        
        # 初始化日志系统
        logger = setup_logger(log_level=log_level)
        logger.info("绩点计算器启动")
        
        # 创建计算器和数据加载器实例
        calculator = GpaCalculator()
        data_loader = DataLoader()
        
        # 创建数据持久化实例
        try:
            data_persistence = DataPersistence()
        except PermissionError as e:
            logger.error(f"无法初始化数据持久化: {str(e)}")
            print(f"错误: 无法创建数据存储目录。请检查权限或使用其他目录。")
            return 1
        
        # 根据参数选择界面
        if args.console:
            # 使用命令行界面
            logger.info("使用命令行界面")
            ui = ConsoleUI(calculator, data_loader)
            ui.run()
        elif args.gui and GUI_AVAILABLE:
            # 使用图形界面
            logger.info("使用图形用户界面")
            app = GUIApplication(calculator, data_loader, data_persistence)
            
            # 如果指定了文件，直接加载
            if args.file:
                if os.path.exists(args.file):
                    logger.info(f"使用命令行指定的文件: {args.file}")
                    app.set_initial_file(args.file)
                else:
                    logger.warning(f"指定的文件不存在: {args.file}")
            
            app.run()
        elif args.gui and not GUI_AVAILABLE:
            logger.error("GUI模块不可用，请安装必要的依赖")
            print("错误: 图形界面不可用。请安装PyQt5后重试。")
            print("可以使用命令: pip install PyQt5")
            return 1
        else:
            # 默认选择图形界面（如果可用），否则使用命令行界面
            if GUI_AVAILABLE:
                logger.info("默认使用图形用户界面")
                app = GUIApplication(calculator, data_loader, data_persistence)
                
                # 如果指定了文件，直接加载
                if args.file:
                    if os.path.exists(args.file):
                        logger.info(f"使用命令行指定的文件: {args.file}")
                        app.set_initial_file(args.file)
                    else:
                        logger.warning(f"指定的文件不存在: {args.file}")
                
                app.run()
            else:
                logger.info("GUI不可用，默认使用命令行界面")
                ui = ConsoleUI(calculator, data_loader)
                ui.run()
        
        logger.info("绩点计算器正常退出")
        return 0
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        print("\n程序已中断")
        return 130  # 标准Unix的SIGINT退出码
    except Exception as e:
        # 记录详细的异常信息
        logger.critical(f"发生未处理的异常: {str(e)}", exc_info=True)
        print(f"\n程序发生错误: {str(e)}")
        print("详细信息已记录到日志文件中")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 