#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPA计算器核心模块，实现各种绩点计算功能
"""

import logging
from typing import List, Union, Optional, Any
from .config import GRADE_MAPPING, FAIL_GRADE_HANDLING

# 配置日志
logger = logging.getLogger(__name__)

class GpaCalculator:
    """
    GPA计算器类，实现平均学分绩、课程绩点和平均学分绩点的计算
    """
    
    def __init__(self):
        """初始化GPA计算器"""
        self.course_names = []
        self.course_grades = []
        self.course_credits = []
        self.course_count = 0
        self.total_credits = 0
    
    def load_data(self, 
                  course_names: List[str], 
                  course_grades: List[Union[str, float, int]], 
                  course_credits: List[Union[str, float, int]]) -> None:
        """
        加载课程数据
        
        Args:
            course_names (List[str]): 课程名称列表
            course_grades (List[Union[str, float, int]]): 课程成绩列表
            course_credits (List[Union[str, float, int]]): 课程学分列表
            
        Raises:
            ValueError: 如果输入数据无效
        """
        # 检查参数是否为列表
        if not all(isinstance(param, list) for param in [course_names, course_grades, course_credits]):
            raise TypeError("课程名称、成绩和学分参数必须是列表类型")
        
        # 检查列表长度是否一致
        if not (len(course_names) == len(course_grades) == len(course_credits)):
            raise ValueError("课程名称、成绩和学分列表长度必须一致")
        
        # 检查列表是否为空
        if len(course_names) == 0:
            raise ValueError("课程数据不能为空")
        
        self.course_names = course_names
        self.course_count = len(course_names)
        
        # 转换学分为浮点数
        self.course_credits = []
        for i, credit in enumerate(course_credits):
            try:
                credit_value = float(credit)
                if credit_value < 0:
                    logger.warning(f"课程 '{course_names[i]}' 的学分为负数 ({credit}), 已调整为0")
                    credit_value = 0.0
                self.course_credits.append(credit_value)
            except (ValueError, TypeError) as e:
                logger.warning(f"无法将课程 '{course_names[i]}' 的学分 '{credit}' 转换为数值，已设为0: {str(e)}")
                self.course_credits.append(0.0)
        
        # 计算总学分
        self.total_credits = sum(self.course_credits)
        
        # 检查总学分是否为0
        if self.total_credits == 0:
            logger.warning("总学分为0，这可能导致除以零错误")
        
        # 转换成绩为数值
        self.course_grades = []
        for i, grade in enumerate(course_grades):
            try:
                if isinstance(grade, str) and grade in GRADE_MAPPING:
                    # 五等级制转换为百分制
                    self.course_grades.append(GRADE_MAPPING[grade])
                else:
                    # 尝试转换为数值
                    grade_value = float(grade)
                    # 百分制成绩范围检查
                    if grade_value < 0:
                        logger.warning(f"课程 '{course_names[i]}' 的成绩为负数 ({grade}), 已调整为0")
                        grade_value = 0.0
                    elif grade_value > 100:
                        logger.warning(f"课程 '{course_names[i]}' 的成绩超过100 ({grade}), 已调整为100")
                        grade_value = 100.0
                    self.course_grades.append(grade_value)
            except (ValueError, TypeError) as e:
                logger.warning(f"无法将课程 '{course_names[i]}' 的成绩 '{grade}' 转换为数值，已设为0: {str(e)}")
                self.course_grades.append(0.0)
    
    def calculate_average_score(self) -> float:
        """
        计算平均学分绩
        
        原名: Pjxfj (拼音缩写: 平均学分绩)
        
        计算公式: 平均学分绩 = Σ(课程成绩 * 课程学分) / 总学分
        注意: 不及格课程按照40分计算
        
        Returns:
            float: 平均学分绩
            
        Raises:
            ValueError: 如果总学分为0
        """
        if self.course_count == 0:
            raise ValueError("没有课程数据，无法计算平均学分绩")
        
        if self.total_credits == 0:
            raise ValueError("总学分为0，无法计算平均学分绩")
        
        # 处理不及格成绩，按照40分计算
        adjusted_grades = []
        for grade in self.course_grades:
            if grade < 60:
                adjusted_grades.append(FAIL_GRADE_HANDLING["avg_score_value"])
            else:
                adjusted_grades.append(grade)
        
        # 计算总成绩*学分
        total_weighted_grade = sum(grade * credit for grade, credit 
                                   in zip(adjusted_grades, self.course_credits))
        
        # 计算平均学分绩
        return total_weighted_grade / self.total_credits
    
    def calculate_course_gpa(self) -> List[float]:
        """
        计算每门课程的绩点
        
        原名: Kcjd (拼音缩写: 课程绩点)
        
        计算公式: 课程绩点 = (课程成绩/10) - 5
        注意: 不及格课程绩点为0
        
        Returns:
            list: 课程绩点列表
            
        Raises:
            ValueError: 如果没有课程数据
        """
        if self.course_count == 0:
            raise ValueError("没有课程数据，无法计算课程绩点")
        
        course_gpa_list = []
        
        for i, grade in enumerate(self.course_grades):
            try:
                if grade < 60:
                    # 不及格课程绩点为0
                    course_gpa_list.append(0.0)
                else:
                    # 计算绩点: (成绩/10) - 5
                    m = int(grade) // 10
                    n = grade / 10 - m
                    course_gpa = m + n - 5
                    
                    # 绩点范围检查 (通常在0-5.0之间)
                    if course_gpa < 0:
                        logger.warning(f"课程 '{self.course_names[i]}' 的绩点计算结果为负数，已调整为0")
                        course_gpa = 0.0
                    elif course_gpa > 5.0:
                        logger.warning(f"课程 '{self.course_names[i]}' 的绩点计算结果超过5.0 ({course_gpa})，可能有误")
                    
                    course_gpa_list.append(round(course_gpa, 1))
            except Exception as e:
                logger.error(f"计算课程 '{self.course_names[i]}' 的绩点时出错: {str(e)}")
                course_gpa_list.append(0.0)
        
        return course_gpa_list
    
    def calculate_overall_gpa(self) -> float:
        """
        计算平均学分绩点(GPA)
        
        原名: Pjxfjd (拼音缩写: 平均学分绩点)
        
        计算公式: 平均学分绩点 = Σ(课程绩点 * 课程学分) / 总学分
        
        Returns:
            float: 平均学分绩点
            
        Raises:
            ValueError: 如果总学分为0
        """
        if self.course_count == 0:
            raise ValueError("没有课程数据，无法计算平均学分绩点")
        
        if self.total_credits == 0:
            raise ValueError("总学分为0，无法计算平均学分绩点")
        
        try:
            # 获取课程绩点
            course_gpa_list = self.calculate_course_gpa()
            
            # 计算总绩点*学分
            total_weighted_gpa = sum(gpa * credit for gpa, credit 
                                    in zip(course_gpa_list, self.course_credits))
            
            # 计算平均学分绩点
            overall_gpa = total_weighted_gpa / self.total_credits
            
            # 绩点范围检查
            if overall_gpa < 0:
                logger.warning(f"计算的总GPA为负数 ({overall_gpa})，已调整为0")
                overall_gpa = 0.0
            elif overall_gpa > 5.0:
                logger.warning(f"计算的总GPA超过5.0 ({overall_gpa})，可能有误")
            
            return round(overall_gpa, 1)
        except Exception as e:
            logger.error(f"计算平均学分绩点时出错: {str(e)}")
            raise 