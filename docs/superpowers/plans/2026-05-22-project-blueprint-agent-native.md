# Project Blueprint 2.0 (Agent-Native Edition) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform Project Blueprint from a human-readable markdown generator into an agent-native architecture analysis engine that provides deep AST-level dependency graphs, micro-context indexes, and architecture conventions via JSON output.

**Architecture:** We will introduce an `ASTParser` to extract class/function definitions and import statements from Python files. The `ProjectAnalyzer` will be upgraded to consume this AST data, generating a dependency graph and inferring architecture rules. Finally, `main.py` will assemble these insights into a structured JSON payload when the `-j` flag is used.

**Tech Stack:** Python 3.8+, built-in `ast` module, `json`.

---

### Task 1: Create AST Parser for Python Files

**Files:**
- Create: `project_blueprint/ast_parser.py`
- Modify: `project_blueprint/__init__.py`

- [ ] **Step 1: Implement `ASTParser` class**

```python
# project_blueprint/ast_parser.py
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple

class ASTParser:
    """解析 Python 文件 AST，提取结构和依赖信息"""
    
    def parse_file(self, file_path: Path) -> Dict:
        """解析单个 Python 文件，返回定义的类、函数和导入的模块"""
        result = {
            "classes": [],
            "functions": [],
            "imports": set()
        }
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError, OSError):
            return result

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                result["functions"].append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    result["imports"].add(node.module.split('.')[0])
                    
        result["imports"] = list(result["imports"])
        return result
```

- [ ] **Step 2: Export `ASTParser`**

Modify `project_blueprint/__init__.py` to export the new parser:
```python
from .ast_parser import ASTParser
```

- [ ] **Step 3: Commit**

```bash
git add project_blueprint/ast_parser.py project_blueprint/__init__.py
git commit -m "feat: add ASTParser to extract python code structure and dependencies"
```

### Task 2: Upgrade ProjectAnalyzer with Deep Insights

**Files:**
- Modify: `project_blueprint/analyzer.py`

- [ ] **Step 1: Import `ASTParser` and update `ProjectInfo` dataclass**

Add `micro_index`, `dependency_graph`, and `architecture_conventions` fields to `ProjectInfo`.

```python
# In project_blueprint/analyzer.py
from .ast_parser import ASTParser

# Update ProjectInfo:
@dataclass
class ProjectInfo:
    name: str
    project_type: str
    tech_stack: List[str] = field(default_factory=list)
    language: str = ""
    framework: str = ""
    config_files: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)
    entry_points: List[str] = field(default_factory=list)
    description: str = ""
    # New fields for 2.0
    micro_index: Dict[str, List[str]] = field(default_factory=dict)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    architecture_conventions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'project_type': self.project_type,
            'tech_stack': self.tech_stack,
            'language': self.language,
            'framework': self.framework,
            'config_files': self.config_files,
            'dependencies': self.dependencies,
            'entry_points': self.entry_points,
            'description': self.description,
            'micro_index': self.micro_index,
            'dependency_graph': self.dependency_graph,
            'architecture_conventions': self.architecture_conventions
        }
```

- [ ] **Step 2: Add `_perform_deep_analysis` method to `ProjectAnalyzer`**

```python
# In project_blueprint/analyzer.py inside ProjectAnalyzer class

    def analyze(self, root_node: DirectoryNode, root_path: Path) -> ProjectInfo:
        # Existing logic...
        self.project_info = ProjectInfo(name=root_path.name, project_type="Unknown")
        all_files = root_node.get_all_files()
        config_files = [f for f in all_files if f.is_config]

        self._detect_project_type(config_files, root_path)
        self._extract_dependencies(config_files)
        self._find_entry_points(all_files)
        self._detect_framework(config_files, all_files)
        
        # New deep analysis step
        self._perform_deep_analysis(all_files, root_path)

        return self.project_info

    def _perform_deep_analysis(self, all_files: List[FileInfo], root_path: Path) -> None:
        parser = ASTParser()
        python_files = [f for f in all_files if f.extension == '.py']
        
        # Build micro index and dependency graph
        for f in python_files:
            try:
                rel_path = str(f.path.relative_to(root_path)).replace('\\', '/')
            except ValueError:
                rel_path = f.name
                
            ast_data = parser.parse_file(f.path)
            
            # Micro index: signatures
            signatures = [f"class {c}" for c in ast_data["classes"]] + [f"def {fn}" for fn in ast_data["functions"]]
            if signatures:
                self.project_info.micro_index[rel_path] = signatures
                
            # Dependency graph: imports
            if ast_data["imports"]:
                self.project_info.dependency_graph[rel_path] = ast_data["imports"]
                
        # Infer architecture conventions (basic example)
        self._infer_conventions()
        
    def _infer_conventions(self) -> None:
        # Example rule inference: if 'models' directory exists but doesn't import 'controllers'
        has_models = any('models' in path for path in self.project_info.micro_index.keys())
        has_controllers = any('controllers' in path for path in self.project_info.micro_index.keys())
        
        if has_models and has_controllers:
            self.project_info.architecture_conventions.append("Detected separation: Models layer exists independent of Controllers layer.")
            
        if self.project_info.framework:
            self.project_info.architecture_conventions.append(f"Follow {self.project_info.framework} idiomatic project structure conventions.")
```

- [ ] **Step 3: Commit**

```bash
git add project_blueprint/analyzer.py
git commit -m "feat: integrate AST deep analysis into ProjectAnalyzer"
```

### Task 3: Assemble and Output Super JSON in CLI

**Files:**
- Modify: `project_blueprint/main.py`
- Modify: `SKILL.md`

- [ ] **Step 1: Modify `main.py` JSON output block**

Ensure the JSON output includes the deep analysis fields. Update the end of `main.py`:

```python
# In project_blueprint/main.py

    if args.json:
        import json
        
        # We need access to the analyzer's project_info. 
        # For simplicity, we can instantiate analyzer here or modify analyze_project to return it.
        # Since analyze_project currently returns a string message, let's extract the raw data by re-running analysis locally or refactoring.
        # The cleanest way without breaking existing API is to refactor analyze_project to optionally return the ProjectInfo object.
```

Refactor `analyze_project` in `main.py`:

```python
# Update signature and return types in project_blueprint/main.py

def analyze_project(
    project_path: str,
    output_filename: str = DEFAULT_OUTPUT_FILENAME,
    max_depth: int = 10,
    return_raw_data: bool = False
):
    # ... existing logic ...
    
    print(f"\n📊 步骤 2/4：分析项目信息...")
    analyzer = ProjectAnalyzer()
    try:
        project_info = analyzer.analyze(root_node, project_path_obj)
        # ... existing logic ...

    if return_raw_data:
        return project_info

    message = f"""..."""
    return message
```

And update the CLI execution block:

```python
    try:
        if args.json:
            project_info = analyze_project(
                project_path=args.path,
                output_filename=args.output,
                max_depth=args.depth,
                return_raw_data=True
            )
        else:
            result = analyze_project(
                project_path=args.path,
                output_filename=args.output,
                max_depth=args.depth
            )
    finally:
        if args.json:
            sys.stdout = original_stdout

    if args.json:
        import json
        output_data = {
            "status": "success",
            "message": "项目深度分析完成",
            "project_info": {
                "name": project_info.name,
                "project_type": project_info.project_type,
                "tech_stack": project_info.tech_stack,
                "framework": project_info.framework
            },
            "micro_index": project_info.micro_index,
            "dependency_graph": project_info.dependency_graph,
            "architecture_conventions": project_info.architecture_conventions,
            "output_file": str(Path(args.path).resolve() / args.output)
        }
        print(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        print(result)
```

- [ ] **Step 2: Update `SKILL.md` Prompt**

Modify `SKILL.md` to instruct the Agent to use the new JSON fields:

```markdown
# Project Blueprint 

You are an advanced project architecture analyzer and convention enforcer. When a user asks you to analyze a project, structure, or generate a blueprint:

1. Execute `python run_blueprint.py` (or `python -m project_blueprint`) in the target directory with the `-j` flag.
2. The tool will output a rich JSON payload. Parse this JSON directly.
3. Use the `micro_index` to quickly locate classes and functions without searching files blindly.
4. Use the `dependency_graph` to understand how modules relate before proposing changes.
5. **Strictly adhere to** any rules listed in `architecture_conventions` when writing or modifying code.
6. Summarize the project's tech stack, core architecture, and module boundaries to the user based on the JSON data, and provide a link to the generated `PROJECT_BLUEPRINT.md` for full details.
```

- [ ] **Step 3: Commit**

```bash
git add project_blueprint/main.py SKILL.md
git commit -m "feat: expose deep AST analysis data via JSON and update SKILL prompt"
```