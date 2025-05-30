#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
打包脚本
使用PyInstaller创建独立的可执行文件
"""

import os
import sys
import shutil
import platform
from PyInstaller.__main__ import run

# 确保在项目根目录下运行
if not os.path.exists('run.py'):
    print("错误: 请在项目根目录下运行此脚本")
    sys.exit(1)

# 清理旧的打包文件
def clean_old_files():
    print("清理旧的打包文件...")
    if os.path.exists('dist'):
        try:
            for item in os.listdir('dist'):
                item_path = os.path.join('dist', item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    print(f"已删除: {item_path}")
        except Exception as e:
            print(f"清理文件时出错: {str(e)}")
    
    # 确保dist目录存在
    if not os.path.exists('dist'):
        os.makedirs('dist')

# 创建图标目录
if not os.path.exists('resources'):
    os.makedirs('resources')

# 创建简单的图标文件（如果没有）
icon_path = os.path.join('resources', 'icon.ico')
if not os.path.exists(icon_path):
    try:
        # 跳过图标创建，使用文本提示
        print("注意: 未找到图标文件，将使用默认图标")
        icon_path = None
    except Exception as e:
        print(f"创建图标时出错: {str(e)}")
        icon_path = None

# 创建data目录（如果不存在）
if not os.path.exists('data'):
    os.makedirs('data')

# 创建logs目录（如果不存在）
if not os.path.exists('logs'):
    os.makedirs('logs')

# 复制Excel示例文件到dist目录
def copy_example_file():
    print("复制示例文件...")
    
    # 查找示例文件
    example_files = ['Excel表格示例.xlsx', '成绩单示例.xlsx']
    found_files = []
    
    # 检查当前目录
    for file in example_files:
        if os.path.exists(file):
            found_files.append((file, file))
    
    # 检查上级目录
    for file in example_files:
        parent_path = os.path.join('..', file)
        if os.path.exists(parent_path):
            found_files.append((parent_path, file))
    
    # 复制找到的文件
    if found_files:
        for source, dest in found_files:
            try:
                shutil.copy(source, os.path.join('dist', dest))
                print(f"已复制: {source} -> dist/{dest}")
            except Exception as e:
                print(f"复制文件 {source} 时出错: {str(e)}")
    else:
        print("警告: 未找到示例Excel文件")

# 创建README.txt文件
def create_readme():
    print("创建README.txt文件...")
    readme_content = """CUPB绩点计算器使用说明
========================

1. 准备Excel文件，格式参考Excel表格示例.xlsx
2. 运行CUPB_GPA_Calculator.exe
3. 点击"浏览..."按钮选择Excel文件
4. 检查导入的课程数据，点击"计算绩点"按钮
5. 在"计算结果"选项卡查看结果
6. 可以点击"保存结果"保存到历史记录
7. 在"历史记录"选项卡查看所有历史计算结果

注意事项：
- 如果历史记录无法保存，请确保程序有权限在其所在目录创建data文件夹
- 如果权限不足，历史记录将保存在用户临时目录下的CUPB_GPA_Calculator/data文件夹中
- 程序会自动处理权限问题，无需手动干预

如有问题，请联系开发者
"""
    
    try:
        with open(os.path.join('dist', 'README.txt'), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("已创建README.txt文件")
    except Exception as e:
        print(f"创建README.txt文件时出错: {str(e)}")

# 创建dist/data目录
def create_dist_data_dir():
    print("创建dist/data目录...")
    data_dir = os.path.join('dist', 'data')
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print("已创建dist/data目录")
        except Exception as e:
            print(f"创建dist/data目录时出错: {str(e)}")

# 清理旧文件
clean_old_files()

# 构建命令行参数
pyinstaller_args = [
    '--onefile',
    '--windowed',
    '--clean',
    '--name=CUPB_GPA_Calculator',
]

# 添加图标（如果存在）
if icon_path and os.path.exists(icon_path):
    pyinstaller_args.append(f'--icon={icon_path}')

# 添加主脚本
pyinstaller_args.append('run.py')

print("开始构建可执行文件...")
print(f"使用参数: {' '.join(pyinstaller_args)}")

try:
    # 运行PyInstaller
    run(pyinstaller_args)
    
    # 创建必要的目录和文件
    create_dist_data_dir()
    copy_example_file()
    create_readme()
    
    print("\n构建完成！可执行文件位于dist目录")
    print("文件名: CUPB_GPA_Calculator.exe")
    
except Exception as e:
    print(f"打包过程中出现错误: {str(e)}")
    sys.exit(1) 