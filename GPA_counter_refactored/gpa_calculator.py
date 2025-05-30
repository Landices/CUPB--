#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPA计算器启动脚本
"""

import sys
import os
import argparse

# 将src目录添加到模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入必要的模块
from src.utils.calculator import GpaCalculator
from src.utils.data_loader import DataLoader
from src.utils.persistence import DataPersistence
from src.ui.console_ui import ConsoleUI
from src.ui.gui import run_gui

def main():
    """程序入口函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='CUPB绩点计算器')
    parser.add_argument('--console', action='store_true', help='使用命令行界面')
    args = parser.parse_args()
    
    try:
        if args.console:
            # 使用命令行界面
            calculator = GpaCalculator()
            data_loader = DataLoader()
            ui = ConsoleUI(calculator, data_loader)
            ui.run()
        else:
            # 使用图形界面（默认）
            run_gui()
    except Exception as e:
        print(f"程序发生错误: {str(e)}")
        input("\n按回车键退出程序...")

if __name__ == "__main__":
    main() 