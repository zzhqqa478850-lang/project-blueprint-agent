# 📋 Project Blueprint

> 本文档由 Project Blueprint 自动生成

## 📊 项目概览

- **项目名称**：test_project
- **项目类型**：Python
- **主要语言**：Python
- **框架**：Flask
- **技术栈**：Requests、Flask
- **生成时间**：2026-05-22 20:32:54

**主要依赖**：

```
flask: 2.0.1
requests: >=2.26.0
```

**入口文件**：

- `D:\skills_create\test_project\app.py`


## 📁 目录结构

```
├── requirements.txt ⚙️
├── README.md
├── app.py
app/
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

### app

**应用程序主目录（Python）。Python 模块**

**主要文件**（共 9 个文件）：

- `__init__.py` - Python

### app\controllers

**控制器层（Python）。控制器**

**主要文件**（共 2 个文件）：

- `__init__.py` - Python
- `main_controller.py` - Python

### app\models

**数据模型（Python）。Python 模块**

**主要文件**（共 3 个文件）：

- `__init__.py` - Python
- `post.py` - Python
- `user.py` - Python

### app\utils

**工具函数库（Python）。表单处理**

**主要文件**（共 3 个文件）：

- `__init__.py` - Python
- `formatters.py` - Python
- `validators.py` - Python

## 🔧 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行项目
python main.py
```

---
*📅 生成时间：2026-05-22 20:32:54*
*🔧 使用 Project Blueprint 生成*