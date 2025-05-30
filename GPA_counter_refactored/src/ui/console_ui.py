#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行界面模块
处理用户交互和结果展示
"""

import logging
import os
import sys
import traceback
from typing import Tuple, List, Any, Optional

from ..utils.config import VERSION

# 获取日志记录器
logger = logging.getLogger(__name__)

class ConsoleUI:
    """
    命令行界面类
    负责处理用户输入和输出结果展示
    """
    
    def __init__(self, calculator, data_loader):
        """
        初始化命令行界面
        
        Args:
            calculator: GPA计算器实例
            data_loader: 数据加载器实例
        """
        logger.info("初始化命令行界面")
        self.calculator = calculator
        self.data_loader = data_loader
    
    def run(self):
        """运行界面，处理用户交互流程"""
        logger.info("启动命令行界面")
        self._display_welcome()
        
        while True:
            try:
                # 获取Excel文件路径
                file_path = self._get_file_path()
                logger.info(f"用户提供的文件路径: {file_path}")
                
                # 验证文件路径
                if not os.path.exists(file_path):
                    logger.error(f"文件不存在: {file_path}")
                    print(f"\n错误: 文件不存在: {file_path}")
                    continue
                
                # 检查文件扩展名
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext not in ['.xlsx', '.xls']:
                    logger.error(f"不支持的文件格式: {file_ext}")
                    print(f"\n错误: 不支持的文件格式: {file_ext}，仅支持.xlsx和.xls格式")
                    continue
                
                # 加载数据
                try:
                    logger.info("开始从Excel加载数据")
                    course_count, course_names, course_grades, course_credits = self.data_loader.load_from_excel(file_path)
                    logger.info(f"成功加载{course_count}门课程的数据")
                
                    # 显示课程信息
                    self._display_courses(course_count, course_names, course_grades, course_credits)
                    
                    # 确认信息
                    if not self._confirm_data():
                        logger.info("用户选择修改数据")
                        print("请修改Excel文件后重新运行\n")
                        continue
                    
                    # 加载数据到计算器
                    logger.info("将数据加载到计算器中")
                    try:
                        self.calculator.load_data(course_names, course_grades, course_credits)
                    except (TypeError, ValueError) as e:
                        logger.error(f"加载数据到计算器失败: {str(e)}")
                        print(f"\n错误: 数据格式有误 - {str(e)}")
                        continue
                    
                    # 计算并显示结果
                    logger.info("开始计算结果")
                    self._calculate_and_display_results()
                    
                    # 计算完成，退出循环
                    logger.info("计算完成")
                    break
                    
                except ValueError as e:
                    logger.error(f"数据加载失败: {str(e)}")
                    print(f"\n错误: {str(e)}")
                    print("请检查文件格式是否正确\n")
                except Exception as e:
                    logger.error(f"数据加载异常: {str(e)}", exc_info=True)
                    print(f"\n未知错误: {str(e)}")
                    print("请检查文件格式或路径是否正确\n")
                
            except KeyboardInterrupt:
                logger.info("用户中断了操作")
                print("\n操作已取消")
                return
            
            except Exception as e:
                logger.error(f"未捕获的异常: {str(e)}", exc_info=True)
                print(f"\n错误: {str(e)}")
                print("请检查文件格式或路径是否正确\n")
        
        # 防止程序运行完成立即关闭窗口
        self._wait_for_exit()
    
    def _display_welcome(self):
        """显示欢迎信息"""
        welcome_msg = f"欢迎使用绩点计算 [{VERSION}]"
        print(welcome_msg)
        logger.info(welcome_msg)
    
    def _get_file_path(self) -> str:
        """
        获取Excel文件路径
        
        Returns:
            str: 文件路径
        """
        path = input("请拖入成绩文件，并回车确定: ").strip()
        # 处理Windows下拖拽文件带引号的情况
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        # 处理空输入
        if not path:
            logger.warning("用户提供了空的文件路径")
            print("错误: 文件路径不能为空")
            return self._get_file_path()  # 递归调用直到获取有效输入
        return path
    
    def _display_courses(self, course_count: int, course_names: List[str], 
                         course_grades: List[Any], course_credits: List[Any]):
        """
        显示课程信息
        
        Args:
            course_count (int): 课程数量
            course_names (list): 课程名称列表
            course_grades (list): 课程成绩列表
            course_credits (list): 课程学分列表
        """
        logger.info("显示课程信息")
        print("\n课程信息如下：")
        
        # 显示表头
        header = f"{'课程名称':<30} | {'成绩':^10} | {'学分':^10}"
        print(header)
        print("-" * len(header))
        
        # 显示课程数据
        for i in range(course_count):
            try:
                # 格式化课程名称（截断过长的名称）
                name = course_names[i]
                if len(name) > 28:  # 预留2个字符的空间
                    name = name[:25] + "..."
                
                # 格式化成绩和学分
                grade = str(course_grades[i])
                credit = str(course_credits[i])
                
                print(f"{name:<30} | {grade:^10} | {credit:^10}")
            except Exception as e:
                logger.error(f"显示课程信息时出错: {str(e)}")
                print(f"[显示错误] {course_names[i] if i < len(course_names) else '未知课程'}")
    
    def _confirm_data(self) -> bool:
        """
        确认数据是否正确
        
        Returns:
            bool: 数据正确返回True，否则返回False
        """
        while True:
            confirm = input('\n请确认课程(有误请输入"1"，无误直接回车): ')
            if confirm == "1":
                logger.info("用户表示数据有误")
                return False
            elif confirm == "":
                logger.info("用户确认数据无误")
                return True
            else:
                logger.warning(f"用户输入了未知选项: {confirm}")
                print('请输入"1"表示数据有误，或直接回车表示数据无误')
    
    def _calculate_and_display_results(self):
        """计算并显示所有结果"""
        try:
            # 计算并显示平均学分绩
            logger.info("计算平均学分绩")
            try:
                avg_score = self.calculator.calculate_average_score()
                print(f"\n平均学分绩为: {avg_score:.2f}")
                logger.info(f"平均学分绩: {avg_score:.2f}")
            except ValueError as e:
                logger.error(f"计算平均学分绩失败: {str(e)}")
                print(f"\n无法计算平均学分绩: {str(e)}")
            
            # 计算并显示课程绩点
            logger.info("计算课程绩点")
            try:
                course_gpas = self.calculator.calculate_course_gpa()
                print("\n各课程绩点:")
                for name, gpa in zip(self.calculator.course_names, course_gpas):
                    print(f"{name}: {gpa}")
                logger.info(f"成功计算{len(course_gpas)}门课程的绩点")
            except ValueError as e:
                logger.error(f"计算课程绩点失败: {str(e)}")
                print(f"\n无法计算课程绩点: {str(e)}")
            
            # 计算并显示平均学分绩点
            logger.info("计算平均学分绩点")
            try:
                overall_gpa = self.calculator.calculate_overall_gpa()
                print(f"\n同学，你的平均学分绩点（GPA）为: {overall_gpa}")
                logger.info(f"平均学分绩点: {overall_gpa}")
            except ValueError as e:
                logger.error(f"计算平均学分绩点失败: {str(e)}")
                print(f"\n无法计算平均学分绩点: {str(e)}")
                
        except Exception as e:
            logger.error(f"计算结果时发生未知错误: {str(e)}", exc_info=True)
            print(f"\n计算过程中发生错误: {str(e)}")
    
    def _wait_for_exit(self):
        """等待用户按键退出"""
        logger.info("等待用户退出")
        input("\n按回车键退出程序...") 