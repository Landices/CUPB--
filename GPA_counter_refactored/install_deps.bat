@echo off
chcp 65001 > nul
echo CUPB绩点计算器 - 依赖安装工具
echo ==============================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请安装Python 3.6或更高版本
    echo 您可以从 https://www.python.org/downloads/ 下载Python
    pause
    exit /b 1
)

REM 安装必要的依赖
echo 正在安装必要的依赖...
python -m pip install --upgrade pip
pip install pandas numpy pyqt5

if %errorlevel% neq 0 (
    echo 安装依赖时出现错误，请检查网络连接或手动安装依赖：
    echo pip install pandas numpy pyqt5
) else (
    echo 依赖安装成功！
    echo 现在您可以运行程序：python run.py
)

pause 