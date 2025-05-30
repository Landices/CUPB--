@echo off
chcp 65001 > nul
echo CUPB绩点计算器打包工具
echo =====================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请安装Python 3.6或更高版本
    pause
    exit /b 1
)

REM 检查并安装必要的依赖
echo 正在检查并安装必要的依赖...
pip install -q pyinstaller pandas numpy pyqt5 pillow

REM 检查PyInstaller是否安装成功
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: PyInstaller安装失败，请手动安装：pip install pyinstaller
    pause
    exit /b 1
)

REM 运行打包脚本
echo 正在打包应用程序...
python setup.py

if %errorlevel% neq 0 (
    echo 打包过程中出现错误，请查看上面的错误信息
) else (
    echo 打包完成！可执行文件位于dist目录中
    echo 文件名: CUPB_GPA_Calculator.exe
    
    REM 尝试打开dist目录
    start "" "dist"
)

pause 