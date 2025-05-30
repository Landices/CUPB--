# CUPB绩点计算器

CUPB（中国石油大学北京）GPA计算器是一个用于计算学生GPA的工具，支持从Excel表格导入课程数据，计算平均学分绩、课程绩点和平均学分绩点。本应用专为Windows平台设计。

## 用户指南

### 安装方式

#### 方式一：使用独立可执行文件（推荐普通用户）

1. 从发布页面下载最新版本的`CUPB_GPA_Calculator.exe`
2. 双击运行即可，无需安装Python或任何依赖

#### 方式二：从源代码运行（适合开发者）

1. 确保您的系统安装了Python 3.6或更高版本
2. 安装依赖包：

```
pip install pandas numpy PyQt5
```

3. 从项目根目录运行：

```
python run.py
```

### 使用方法

1. 准备Excel文件，格式参考[Excel表格示例.xlsx](Excel表格示例.xlsx)
2. 启动程序，点击"浏览..."按钮选择Excel文件
3. 检查导入的课程数据，点击"计算绩点"按钮
4. 在"计算结果"选项卡查看结果，可以点击"保存结果"保存到历史记录
5. 在"历史记录"选项卡查看所有历史计算结果

### 命令行参数

```
# 使用命令行界面
python run.py --console

# 使用图形界面
python run.py --gui

# 启用调试模式
python run.py --debug

# 直接指定Excel文件路径
python run.py --file "path/to/excel.xlsx"
```

### Excel文件格式

Excel文件应包含以下列（默认设置）：
- 第2列（索引1）：课程名称
- 第3列（索引2）：课程成绩（支持百分制或五等级制）
- 第4列（索引3）：课程学分

可以在`src/utils/config.py`中修改Excel列配置。

## 开发者文档

### 项目结构

```
GPA_counter_refactored/
├── data/                 # 存储历史记录
├── logs/                 # 存储日志文件
├── src/                  # 源代码目录
│   ├── ui/               # 用户界面模块
│   │   ├── console_ui.py # 命令行界面
│   │   └── gui.py        # 图形用户界面
│   ├── utils/            # 工具模块
│   │   ├── calculator.py # GPA计算器核心
│   │   ├── config.py     # 配置文件
│   │   ├── data_loader.py# 数据加载器
│   │   ├── logger.py     # 日志配置
│   │   └── persistence.py# 数据持久化
│   └── main.py           # 主程序入口
├── run.py                # 启动脚本
├── build.bat             # 打包批处理脚本
├── start.bat             # 启动批处理脚本
├── install_deps.bat      # 依赖安装批处理脚本
└── setup.py              # 打包脚本
```

### 核心模块说明

1. **calculator.py**: 实现GPA计算逻辑，包括平均学分绩、课程绩点和平均学分绩点计算
2. **data_loader.py**: 负责从Excel文件加载课程数据
3. **persistence.py**: 处理历史记录的保存和加载
4. **logger.py**: 配置日志系统
5. **config.py**: 存储配置信息，如成绩映射表、Excel列配置等
6. **console_ui.py**: 命令行界面实现
7. **gui.py**: 图形用户界面实现

### 错误处理

程序包含全面的错误处理机制：

- 文件输入验证：检查文件是否存在、格式是否支持
- 数据验证：检查Excel数据是否有效，处理无效数据
- 计算异常处理：防止除以零等计算错误
- 用户输入验证：验证用户输入的有效性

### 日志系统

程序使用Python标准日志模块记录运行信息：

- 错误日志：记录所有错误和异常信息
- 信息日志：记录操作和计算过程
- 调试日志：记录详细的程序执行流程（在调试模式下）

日志文件保存在`logs`目录下，按日期命名。

### 打包指南

要创建独立的可执行文件，可以使用提供的打包脚本：

```
build.bat
```

或者手动使用PyInstaller：

```
pip install pyinstaller
pyinstaller --onefile --windowed --name="CUPB_GPA_Calculator" run.py
```

生成的可执行文件将位于`dist`目录中。

## 常见问题

1. **问题**: 程序无法启动图形界面
   **解决方案**: 确保已安装PyQt5，运行`pip install PyQt5`

2. **问题**: Excel文件格式不正确
   **解决方案**: 请参考[Excel表格示例.xlsx](Excel表格示例.xlsx)，确保列的位置正确

3. **问题**: 历史记录无法保存
   **解决方案**: 确保程序有权限在其所在目录创建data文件夹，或者尝试以管理员身份运行程序

4. **问题**: 计算结果与预期不符
   **解决方案**: 检查Excel中的成绩和学分数据，确保格式正确

## 系统要求

- 操作系统: Windows 7/8/10/11
- 如果从源码运行: Python 3.6+
