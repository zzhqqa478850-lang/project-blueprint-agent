# 📋 Project Blueprint

> 本文档由 Project Blueprint 自动生成

## 📊 项目概览

- **项目名称**：skills_create
- **项目类型**：Python
- **主要语言**：Python
- **框架**：Flask
- **技术栈**：Flask、Requests
- **生成时间**：2026-05-23 15:07:51

**主要依赖**：

```
flask: 2.0.1
requests: >=2.26.0
```

**入口文件**：

- `D:\skills_create\project_blueprint\__main__.py`
- `D:\skills_create\project_blueprint\main.py`
- `D:\skills_create\test_project\app.py`


## 🛡️ 架构规范与守卫

> 以下是该项目必须遵守的架构约定，Agent 修改代码前应严格遵循：

- Do not use lodash
- Detected separation: Models layer exists independent of Controllers layer.
- Follow Flask idiomatic project structure conventions.


## 📁 目录结构

```
├── .blueprint_rules.json
├── PROJECT_BLUEPRINT.md
├── SKILL.md
├── USAGE.md
├── run_blueprint.py
├── run_blueprint.zip
├── skill.json
├── test_project.py
docs/
│   └── superpowers/
│       ├── plans/
│       │   ├── 2026-05-22-code-optimization.md
│       │   └── 2026-05-22-project-blueprint-agent-native.md
│       └── specs/
│           └── 2026-05-22-project-blueprint-design.md
project_blueprint/
│   ├── README.md
│   ├── __init__.py
│   ├── __main__.py
│   ├── analyzer.py
│   ├── ast_parser.py
│   ├── constants.py
│   ├── documenter.py
│   ├── generator.py
│   ├── main.py
│   ├── rules.py
│   └── scanner.py
test_project/
    ├── requirements.txt ⚙️
    ├── PROJECT_BLUEPRINT.md
    ├── README.md
    ├── app.py
    └── app/
        ├── __init__.py
        ├── controllers/
        │   ├── __init__.py
        │   └── main_controller.py
        ├── models/
        │   ├── __init__.py
        │   ├── post.py
        │   └── user.py
        └── utils/
            ├── __init__.py
            ├── formatters.py
            └── validators.py
```

## 📄 文件说明

### docs

**文档资料**


### docs\superpowers

**包含 0 个文件**


### docs\superpowers\plans

**包含文件：2026-05-22-code-optimization.md、2026-05-22-project-blueprint-agent-native.md**

**主要文件**（共 2 个文件）：

- `2026-05-22-code-optimization.md` - Markdown
- `2026-05-22-project-blueprint-agent-native.md` - Markdown

### docs\superpowers\specs

**测试代码。包含文件：2026-05-22-project-blueprint-design.md**

**主要文件**（共 1 个文件）：

- `2026-05-22-project-blueprint-design.md` - Markdown

### project_blueprint

**包含 11 个文件**

**主要文件**（共 11 个文件）：

- `README.md` - Markdown
- `__init__.py` - Python
- `__main__.py` - Python
- `analyzer.py` - Python
- `ast_parser.py` - Python
- `constants.py` - Python
- `documenter.py` - Python
- `generator.py` - Python
- *... 还有 2 个文件*

### test_project

**Python 依赖配置**

**主要文件**（共 13 个文件）：

- `requirements.txt` - Text ⚙️
- `PROJECT_BLUEPRINT.md` - Markdown
- `README.md` - Markdown
- `app.py` - Python

### test_project\app

**应用程序主目录（Python）。Python 模块**

**主要文件**（共 9 个文件）：

- `__init__.py` - Python

### test_project\app\controllers

**控制器层（Python）。控制器**

**主要文件**（共 2 个文件）：

- `__init__.py` - Python
- `main_controller.py` - Python

### test_project\app\models

**数据模型（Python）。Python 模块**

**主要文件**（共 3 个文件）：

- `__init__.py` - Python
- `post.py` - Python
- `user.py` - Python

### test_project\app\utils

**工具函数库（Python）。表单处理**

**主要文件**（共 3 个文件）：

- `__init__.py` - Python
- `formatters.py` - Python
- `validators.py` - Python


## 🎯 快速导航

| 功能 | 路径 | 文件数 |
|------|------|--------|
| 文档 | `docs` | 3 |

## 🔧 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行项目
python main.py
```

---
*📅 生成时间：2026-05-23 15:07:51*
*🔧 使用 Project Blueprint 生成*