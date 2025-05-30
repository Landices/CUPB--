#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置文件，包含成绩等级映射等常量
"""

# 五等级制成绩映射到百分制
GRADE_MAPPING = {
    "优秀": 95,
    "良好": 85,
    "中等": 75,
    "及格": 65,
    "不及格": 0
}

# Excel表格相关配置
EXCEL_CONFIG = {
    "start_row": 1,  # 数据从第2行开始（索引为1），标题行通常是第1行（索引为0）
    "course_name_col": 1,  # 课程名称列索引
    "course_grade_col": 2,  # 课程成绩列索引
    "course_credit_col": 3  # 课程学分列索引
}

# 不及格成绩的处理方式
FAIL_GRADE_HANDLING = {
    "avg_score_value": 40,  # 计算平均学分绩(平均学分绩=pjxfj)时不及格成绩按40分计算
    "gpa_value": 0          # 计算GPA(平均学分绩点=pjxfjd)时不及格成绩按0计算
}

# 版本信息
VERSION = "3.0" 