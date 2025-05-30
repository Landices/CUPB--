@echo off
chcp 65001 > nul
echo 正在启动CUPB绩点计算器...

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请安装Python 3.6或更高版本
    echo 您可以运行install_deps.bat安装必要的依赖
    pause
    exit /b 1
)

REM 启动程序
python run.py %*

if %errorlevel% neq 0 (
    echo 程序运行时出现错误，请查看上面的错误信息
    echo 如果是缺少依赖，请运行install_deps.bat安装必要的依赖
    pause
) 