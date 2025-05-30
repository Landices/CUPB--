#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据加载模块，用于从Excel读取课程数据
"""

import os
import logging
import pandas as pd
from typing import Tuple, List, Union, Any
from .config import EXCEL_CONFIG

# 配置日志
logger = logging.getLogger(__name__)

class DataLoader:
    """
    数据加载类，负责从Excel文件中读取课程数据
    """
    
    @staticmethod
    def load_from_excel(file_path: str) -> Tuple[int, List[str], List[Any], List[Any]]:
        """
        从Excel文件加载课程数据
        
        Args:
            file_path (str): Excel文件路径
            
        Returns:
            tuple: (课程数量, 课程名称列表, 课程成绩列表, 课程学分列表)
            
        Raises:
            ValueError: 如果文件读取失败或格式不正确
            FileNotFoundError: 如果文件不存在
            TypeError: 如果file_path不是字符串类型
        """
        # 检查参数类型
        if not isinstance(file_path, str):
            raise TypeError("文件路径必须是字符串类型")
            
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        # 检查文件扩展名
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in ['.xlsx', '.xls']:
            raise ValueError(f"不支持的文件格式: {file_ext}，仅支持.xlsx和.xls格式")
        
        try:
            # 打开Excel文件
            df = pd.read_excel(file_path)
            
            # 检查文件是否为空
            if df.empty:
                raise ValueError("Excel文件为空")
                
            # 获取配置
            start_row = EXCEL_CONFIG["start_row"]
            name_col = EXCEL_CONFIG["course_name_col"]
            grade_col = EXCEL_CONFIG["course_grade_col"]
            credit_col = EXCEL_CONFIG["course_credit_col"]
            
            # 检查列数是否足够
            required_cols = max(name_col, grade_col, credit_col) + 1
            if df.shape[1] < required_cols:
                raise ValueError(f"Excel文件列数不足，至少需要{required_cols}列")
            
            # 检查数据有效性
            if df.shape[0] <= start_row:
                raise ValueError(f"Excel文件中没有足够的数据行，至少需要{start_row+1}行")
            
            # 尝试识别有效数据范围
            # 查找所有非空的课程名称单元格
            valid_rows = []
            for i in range(start_row, df.shape[0]):
                if pd.notna(df.iloc[i, name_col]) and str(df.iloc[i, name_col]).strip():
                    # 检查该行其他必要列是否有数据
                    if pd.isna(df.iloc[i, grade_col]):
                        logger.warning(f"第{i+1}行课程'{df.iloc[i, name_col]}'没有成绩数据")
                    if pd.isna(df.iloc[i, credit_col]):
                        logger.warning(f"第{i+1}行课程'{df.iloc[i, name_col]}'没有学分数据")
                    valid_rows.append(i)
            
            if not valid_rows:
                raise ValueError("未找到有效的课程数据")
            
            logger.info(f"找到{len(valid_rows)}行有效课程数据")
            
            # 提取数据
            course_names = []
            course_grades = []
            course_credits = []
            
            for i in valid_rows:
                # 课程名称处理
                name = str(df.iloc[i, name_col]).strip()
                course_names.append(name)
                
                # 成绩处理
                grade = df.iloc[i, grade_col]
                course_grades.append(grade)
                
                # 学分处理
                credit = df.iloc[i, credit_col]
                course_credits.append(credit)
            
            # 记录提取的数据概况
            logger.info(f"成功从Excel文件中提取{len(course_names)}门课程的数据")
            
            # 返回课程数量和数据
            return len(course_names), course_names, course_grades, course_credits
            
        except pd.errors.EmptyDataError:
            logger.error("Excel文件为空或格式错误")
            raise ValueError("Excel文件为空或格式错误")
        except pd.errors.ParserError as e:
            logger.error(f"解析Excel文件时出错: {str(e)}")
            raise ValueError(f"解析Excel文件时出错: {str(e)}")
        except Exception as e:
            logger.error(f"加载Excel文件失败: {str(e)}")
            raise ValueError(f"加载Excel文件失败: {str(e)}") 