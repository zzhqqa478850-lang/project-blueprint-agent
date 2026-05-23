# Project Blueprint

**智能项目结构分析工具** - 一键生成项目蓝图文档

## 🎯 简介

Project Blueprint 是一款面向开发者的智能工具，旨在解决"项目文件一多就忘记哪个文件夹干什么用"的痛点。通过自动扫描项目目录、分析代码文件，为每个文件夹生成清晰的功能说明，最终输出一份结构化的 Markdown 项目蓝图文档。

## ✨ 功能特点

- 📂 **智能目录扫描**：自动跳过 node_modules、\_\_pycache\_\_ 等无关目录
- 🌍 **多语言支持**：Python、JavaScript/TypeScript、Java、Go 等
- 🧠 **智能分析**：识别项目类型、技术栈、依赖关系
- 📝 **自动生成说明**：为每个文件夹生成准确的功能描述
- 🎨 **美观文档**：输出的 Markdown 文档结构清晰、可读性强
- 🔍 **快速导航**：提供快速定位关键文件的导航表

## 🚀 快速开始

### 安装

```bash
git clone <repository-url>
cd project_blueprint
pip install -e .
```

### 使用方式

**方式一：命令行使用**

```bash
# 分析当前目录
python -m project_blueprint

# 分析指定目录
python -m project_blueprint /path/to/your/project

# 自定义输出文件名
python -m project_blueprint -o MY_PROJECT_MAP.md

# 设置最大扫描深度
python -m project_blueprint -d 5
```

**方式二：在 Python 代码中调用**

```python
from project_blueprint import analyze_project

result = analyze_project('/path/to/project')
print(result)
```

## 📋 输出示例

生成的 `PROJECT_BLUEPRINT.md` 包含以下内容：

### 项目概览
- 项目名称和类型
- 技术栈和依赖
- 入口文件

### 目录结构
- 树形结构展示
- 配置文件标记

### 文件说明
- 每个文件夹的功能描述
- 主要文件列表

### 快速导航
- 关键功能快速定位
- 文件数量统计

### 运行方式
- 安装依赖命令
- 启动项目命令

## 🛠️ 项目结构

```
project_blueprint/
├── __init__.py          # 包初始化
├── constants.py         # 常量定义
├── scanner.py           # 目录扫描器
├── analyzer.py          # 项目分析器
├── generator.py         # 说明生成器
├── documenter.py        # 文档生成器
└── main.py              # 主入口
```

## 🔧 技术栈

- Python 3.8+
- 标准库：pathlib, json, re, datetime

无外部依赖，纯 Python 实现！

## 📖 使用场景

- **接手新项目**：快速理解陌生项目结构
- **项目重构**：梳理现有代码结构
- **团队协作**：生成项目文档供团队参考
- **个人管理**：整理多个项目的结构

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

感谢所有开源贡献者！
