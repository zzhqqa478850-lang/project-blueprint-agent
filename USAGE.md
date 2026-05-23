# Project Blueprint - 使用指南

## 快速开始

### 基本使用

1. 确保你的电脑上安装了 Python（3.8 或更高版本）。

2. 运行工具：
```bash
python run_blueprint.py
```

这个命令会分析当前目录下的项目，生成 `PROJECT_BLUEPRINT.md 文档。

### 如何分析指定目录

你可以修改 `run_blueprint.py` 文件，或者直接用 Python 调用我们的工具。

## 功能特点

- 🔍 **智能目录扫描 - 自动跳过不需要的目录如 `node_modules`, `__pycache__` 等
- 🌍 **多语言支持** - Python, JavaScript, Java, Go 等多种语言
- 📊 **项目类型识别** - 自动识别项目类型和依赖
- ✍️ **自动说明生成** - 为每个文件夹生成功能描述
- 📝 **美观的文档输出** - 包含目录树、文件说明、快速导航
- 🔧 **运行方式提示** - 自动提取安装和运行命令

## 示例

你可以在 `test_project/` 目录下找到一个示例项目，里面已经有一个自动生成的 `PROJECT_BLUEPRINT.md 文档供参考！
