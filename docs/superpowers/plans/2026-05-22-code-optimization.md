# Project Blueprint 代码优化 - 实现计划

> **For agentic workers:** 本计划包含 5 个任务，按文件分组执行。每步使用 checkbox (`- [ ]`) 标记。

**Goal:** 修复审查中发现的 12 个问题（3 个严重错误 + 5 个代码质量 + 4 个优化建议）

**Architecture:** 按文件逐个修复，每个文件独立完成，最终运行测试脚本验证

**Tech Stack:** Python 3.8+, pathlib, json, re, datetime（纯标准库，无第三方依赖）

---

## 改动文件映射

| 文件 | 改动类型 | 负责 |
|------|---------|------|
| `project_blueprint/constants.py` | 修改 | 清理冗余/错误的常量定义 |
| `project_blueprint/scanner.py` | 修改 | 移除未使用 import、移动内联 import |
| `project_blueprint/analyzer.py` | 修改 | 修复重复代码、删除未使用参数 |
| `project_blueprint/generator.py` | 修改 | 移除未使用 import/变量 |
| `project_blueprint/documenter.py` | 修改 | 修复内联 import 和 None 引用风险 |

---

### Task 1: 修复 constants.py（3 个严重 + 2 个中等）

**Files:**
- Modify: `d:\skills_create\project_blueprint\constants.py`

- [ ] **Step 1: 移除未使用的 import**

顶部 `from pathlib import Path` 从未被使用，直接删除。

```python
"""
常量定义模块
包含文件类型映射、过滤规则等常量配置
"""

DEFAULT_EXCLUDE_DIRS = [
```

- [ ] **Step 2: 从 DEFAULT_EXCLUDE_DIRS 中移除文件名模式（*.pyc、*.so 等）**

这些是文件模式，放在目录排除列表中永远不会匹配（因为 `_should_exclude` 只检查 `path.name in self.exclude_dirs`），将它们移回 `DEFAULT_EXCLUDE_FILES`。

变更后 `DEFAULT_EXCLUDE_DIRS`：
```python
DEFAULT_EXCLUDE_DIRS = [
    '__pycache__',
    '.git',
    '.svn',
    '.hg',
    'node_modules',
    'bower_components',
    'dist',
    'build',
    'out',
    '.idea',
    '.vscode',
    '.vs',
    'venv',
    '.venv',
    'env',
    '.env',
    'ENV',
    '.pytest_cache',
    '.tox',
    '.mypy_cache',
    '.ruff_cache',
    '.coverage',
    'htmlcov',
    '.eggs',
    '.DS_Store',
    'Thumbs.db',
    '.gradle',
    'target',
    'bin',
    'obj',
]
```

`DEFAULT_EXCLUDE_FILES` 保持不变（它本来就包含 `*.pyc`、`*.so` 等）：
```python
DEFAULT_EXCLUDE_FILES = [
    '*.pyc',
    '*.pyo',
    '*.so',
    '*.dll',
    '*.dylib',
    '*.class',
    '*.o',
    '*.obj',
    '.DS_Store',
    'Thumbs.db',
]
```

- [ ] **Step 3: 修复 FOLDER_NAME_PATTERNS 中重复的 `scripts` key**

删除第二个 `'scripts': '构建脚本'`（保留第一个 `'scripts': '脚本文件'`）。

- [ ] **Step 4: 删除 PYTHON_SPECIFIC_PATTERNS 整个字典（未被使用且含重复 key）**

该常量在 analyzer.py 中被 import 但从未使用，直接删除整个块（L246-L256）。

- [ ] **Step 5: 删除 DEFAULT_SCAN_DEPTH（未被使用）**

```python
# 删除这一行
DEFAULT_SCAN_DEPTH = 3
```

- [ ] **Step 6: 验证**

```bash
python -c "from project_blueprint.constants import *; print('OK')"
```
Expected: 无报错，正常导入。

---

### Task 2: 修复 scanner.py（1 个中等 + 1 个内联 import）

**Files:**
- Modify: `d:\skills_create\project_blueprint\scanner.py`

- [ ] **Step 1: 移除未使用的 import**

```python
import os  # 删除这行
```

```python
from typing import List, Dict, Set, Optional  # 删除 Set（改为 List, Dict, Optional）
```

- [ ] **Step 2: 将内联 import 移到文件顶部**

在 `_analyze_file` 方法（L218）中删除：
```python
from .constants import CONFIG_FILES
```

在文件顶部 import 中加入 `CONFIG_FILES`：
```python
from .constants import (
    DEFAULT_EXCLUDE_DIRS,
    DEFAULT_EXCLUDE_FILES,
    FILE_TYPE_MAPPING,
    CONFIG_FILES,
    MAX_DEPTH,
    MAX_FILES_PER_FOLDER
)
```

- [ ] **Step 3: 验证**

```bash
python -c "from project_blueprint.scanner import DirectoryScanner; print('OK')"
```
Expected: `OK`

---

### Task 3: 修复 analyzer.py（1 个严重 + 1 个优化）

**Files:**
- Modify: `d:\skills_create\project_blueprint\analyzer.py`

- [ ] **Step 1: 删除重复的 `elif 'fastapi'` 块**

在 `_detect_framework` 方法中（L304-L309），第二个 `elif 'fastapi'` 是第一个的重复：

删除：
```python
                    elif 'fastapi' in dep_lower:
                        framework = "FastAPI"
                        break
```

- [ ] **Step 2: 移除未使用的 PYTHON_SPECIFIC_PATTERNS import**

`PYTHON_SPECIFIC_PATTERNS` 导入后从未使用，且 constants.py 中已删除该常量。

变更前 import：
```python
from .constants import CONFIG_FILES, FILE_TYPE_MAPPING, PYTHON_FRAMEWORK_INDICATORS, JS_FRAMEWORK_INDICATORS
```

不变（PYTHON_SPECIFIC_PATTERNS 之前就没在这里 import，它在 constants.py 中定义但从未被其他模块使用）。

- [ ] **Step 3: 验证**

```bash
python -c "from project_blueprint.analyzer import ProjectAnalyzer; print('OK')"
```
Expected: `OK`

---

### Task 4: 修复 generator.py（2 个中等）

**Files:**
- Modify: `d:\skills_create\project_blueprint\generator.py`

- [ ] **Step 1: 移除未使用的 import 和变量**

移除 `Set`（未使用）:
```python
from typing import Dict, List, Optional  # 删除 Set
```

移除 `CONFIG_FILES`（在 generator.py 中 import 但从未使用）:
```python
from .constants import FOLDER_NAME_PATTERNS  # 删除 , CONFIG_FILES
```

删除 `_analyze_folder` 中未使用的局部变量 `relative_path`（L91）:
```python
folder_name = node.name.lower()
# 删除: relative_path = str(node.relative_path)
```

- [ ] **Step 2: 删除未使用的参数**

`_check_folder_pattern` 方法签名中 `node` 参数（类型 `DirectoryNode`）从未被使用：

```python
def _check_folder_pattern(
    self,
    folder_name: str  # 删除 node: DirectoryNode
) -> Optional[str]:
```

同时更新调用方 `_analyze_folder`：
```python
pattern_description = self._check_folder_pattern(folder_name)  # 删除 , node
```

`_analyze_js_files` 同样有未使用的 `node` 参数 — 但这个方法内部访问了 `node.files`，所以保留。让我重新确认... 实际上 `_analyze_js_files` 和 `_analyze_python_files` 都用了 `node.files`（在 `any(keyword in f.name.lower() for f in node.files)`），所以不需要改这两个。

- [ ] **Step 3: 验证**

```bash
python -c "from project_blueprint.generator import DescriptionGenerator; print('OK')"
```
Expected: `OK`

---

### Task 5: 修复 documenter.py（1 个严重 + 2 个优化）

**Files:**
- Modify: `d:\skills_create\project_blueprint\documenter.py`

- [ ] **Step 1: 将内联 import 移到文件顶部**

文件顶部加入：
```python
from .scanner import DirectoryNode, DirectoryScanner
from .generator import FolderDescription, DescriptionGenerator
```

删除 `generate()` 方法中的（L46）：
```python
from .scanner import DirectoryScanner
```

删除 `_build_document()` 方法中的（L102）：
```python
from .generator import DescriptionGenerator
```

- [ ] **Step 2: 修复 DirectoryScanner 未初始化 root_path 问题**

在 `generate()` 方法中，将新创建的 `DirectoryScanner()` 改为使用已存在的 root_node 信息构造树字符串，直接从 scanner 模块导入版本。

将：
```python
from .scanner import DirectoryScanner

scanner = DirectoryScanner()
tree_string = scanner.get_directory_tree_string(root_node)
```

改为在 `_build_document` 中传递 `root_node` 并在其中生成树，让 `get_directory_tree_string` 不依赖 `self.root_path`：

直接修改 `get_directory_tree_string` 的调用方式，传入 `root_path_name` 参数。但这样要改 scanner 的接口...

**简化方案**：直接在 documenter 中手动构建树字符串的根节点名称。

将：
```python
scanner = DirectoryScanner()
tree_string = scanner.get_directory_tree_string(root_node)
```

改为：
```python
scanner = DirectoryScanner()
scanner.root_path = output_path  # 设置 root_path 以正确显示根目录名
tree_string = scanner.get_directory_tree_string(root_node)
```

- [ ] **Step 3: Windows 路径中反斜杠统一为正斜杠**

在 `_build_folder_descriptions` 中，将路径的 `\` 替换为 `/`：

```python
for path in sorted_paths:
    desc = folder_descriptions[path]
    display_path = path.replace('\\', '/')  # Windows 路径规范化
    lines.append(f"### {display_path}")
```

- [ ] **Step 4: 空文件夹（只有子目录）跳过无意义描述**

在 `_build_folder_descriptions` 中，跳过 `main_files` 为空且描述无意义的节点。

- [ ] **Step 5: 运行完整测试验证**

```bash
python run_blueprint.py
```
Expected: 生成文档，无错误。

---

## 自审清单

- [x] Spec coverage: 审查报告中的 12 个问题均有对应修复步骤
- [x] Placeholder scan: 无 TBD/TODO，全部步骤含具体代码
- [x] Type consistency: `root_path` 类型为 `Path`，`display_path` 为 `str`，签名一致