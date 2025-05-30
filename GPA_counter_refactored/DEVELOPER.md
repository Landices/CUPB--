# CUPB绩点计算器 - 开发者指南

## 项目概述

CUPB绩点计算器是一个用于计算中国石油大学（北京）学生GPA的工具。本项目使用Python编写，采用模块化设计，支持命令行和图形用户界面。本应用专为Windows平台设计。

## 技术栈

- **Python 3.6+**: 核心编程语言
- **Pandas**: 用于Excel数据处理
- **PyQt5**: 用于图形用户界面
- **Logging**: 用于日志记录
- **JSON**: 用于数据持久化

## 项目结构

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
├── setup.py              # 打包脚本
├── build.bat             # 打包批处理文件
├── start.bat             # 启动批处理文件
└── install_deps.bat      # 依赖安装批处理文件
```

## 开发环境设置

1. 安装依赖：
   ```
   pip install pandas numpy pyqt5
   # 如果需要打包
   pip install pyinstaller pillow
   ```

## 核心模块说明

### 1. calculator.py

GPA计算器核心逻辑，实现以下功能：
- 平均学分绩计算（原名: Pjxfj）
- 课程绩点计算（原名: Kcjd）
- 平均学分绩点计算（原名: Pjxfjd）

计算公式：
- 平均学分绩 = Σ(课程成绩 * 课程学分) / 总学分
- 课程绩点 = (课程成绩/10) - 5
- 平均学分绩点 = Σ(课程绩点 * 课程学分) / 总学分

### 2. data_loader.py

负责从Excel文件加载课程数据，支持处理：
- 百分制成绩
- 五等级制成绩（优秀、良好、中等、及格、不及格）

### 3. persistence.py

处理历史记录的保存和加载，使用JSON格式存储数据。特别注意，在打包后的环境中，persistence.py会自动检测是否有权限在程序目录创建data文件夹，如果没有权限，会使用临时目录保存历史记录。

### 4. logger.py

配置日志系统，将日志保存到文件中，便于调试和错误追踪。

### 5. config.py

存储配置信息，如成绩映射表、Excel列配置等。

### 6. console_ui.py 和 gui.py

实现命令行界面和图形用户界面，处理用户交互。

## 代码规范

1. **命名约定**：
   - 类名使用驼峰命名法（如 `GpaCalculator`）
   - 函数和变量使用下划线命名法（如 `calculate_average_score`）
   - 私有方法使用下划线前缀（如 `_display_welcome`）
   - 常量使用全大写（如 `VERSION`）

2. **文档字符串**：
   - 所有模块、类和函数都应有文档字符串
   - 函数文档应包含参数、返回值和异常说明

3. **类型注解**：
   - 使用Python类型注解提高代码可读性
   - 例如：`def load_data(self, course_names: List[str]) -> None:`

4. **错误处理**：
   - 使用适当的异常类型
   - 捕获特定异常而非通用异常
   - 记录异常信息到日志

## 测试

目前项目没有自动化测试，但建议添加以下测试：

1. **单元测试**：
   - 测试计算器核心逻辑
   - 测试数据加载功能
   - 测试数据持久化功能

2. **集成测试**：
   - 测试从Excel加载到计算结果的完整流程
   - 测试GUI界面的交互

## 打包

使用PyInstaller创建独立的可执行文件：

```
# 使用批处理文件（推荐）
build.bat

# 或手动运行
python setup.py
```

打包后的文件将位于dist目录中，包括：
- CUPB_GPA_Calculator.exe - 可执行文件
- Excel表格示例.xlsx - 示例数据文件
- README.txt - 使用说明
- data/ - 历史记录存储目录

