"""
项目分析器模块
负责分析项目类型、技术栈、关键配置信息
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from .scanner import DirectoryNode, FileInfo
from .constants import CONFIG_FILES, FILE_TYPE_MAPPING, PYTHON_FRAMEWORK_INDICATORS, JS_FRAMEWORK_INDICATORS
from .ast_parser import ASTParser
from .rules import RulesManager


@dataclass
class ProjectInfo:
    """项目信息数据类"""
    name: str
    project_type: str
    tech_stack: List[str] = field(default_factory=list)
    language: str = ""
    framework: str = ""
    config_files: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)
    entry_points: List[str] = field(default_factory=list)
    description: str = ""
    micro_index: Dict[str, List[str]] = field(default_factory=dict)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    architecture_conventions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """转换为字典格式"""
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


class ProjectAnalyzer:
    """项目分析器类"""

    def __init__(self):
        """初始化项目分析器"""
        self.project_info: Optional[ProjectInfo] = None

    def analyze(self, root_node: DirectoryNode, root_path: Path, query: str = None, impact: str = None) -> ProjectInfo:
        """
        分析项目信息

        Args:
            root_node: 目录树根节点
            root_path: 项目根路径
            query: 模块查询关键词
            impact: 影响分析的文件路径

        Returns:
            ProjectInfo: 项目信息
        """
        self.project_info = ProjectInfo(name=root_path.name, project_type="Unknown")

        all_files = root_node.get_all_files()
        config_files = [f for f in all_files if f.is_config]

        self._detect_project_type(config_files, root_path)
        self._extract_dependencies(config_files)
        self._find_entry_points(all_files)
        self._detect_framework(config_files, all_files)

        self._perform_deep_analysis(all_files, root_path, query=query, impact=impact)

        return self.project_info

    def _perform_deep_analysis(self, all_files: List[FileInfo], root_path: Path, query: str = None, impact: str = None) -> None:
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

        # Filter based on query or impact
        if query:
            filtered_index = {k: v for k, v in self.project_info.micro_index.items() if query.lower() in k.lower()}
            self.project_info.micro_index = filtered_index
            filtered_graph = {k: v for k, v in self.project_info.dependency_graph.items() if query.lower() in k.lower() or any(query.lower() in imp.lower() for imp in v)}
            self.project_info.dependency_graph = filtered_graph
            
        if impact:
            # Reverse lookup: find files that import the target impact module
            impact_module = Path(impact).stem
            filtered_index = {}
            filtered_graph = {}
            for k, imports in self.project_info.dependency_graph.items():
                if impact_module in imports or any(impact_module in imp for imp in imports):
                    filtered_graph[k] = imports
                    if k in self.project_info.micro_index:
                        filtered_index[k] = self.project_info.micro_index[k]
            self.project_info.micro_index = filtered_index
            self.project_info.dependency_graph = filtered_graph
                
        # Infer architecture conventions (basic example)
        self._infer_conventions(root_path)
        
    def _infer_conventions(self, root_path: Path) -> None:
        # Load dynamic rules from .blueprint_rules.json
        rules_manager = RulesManager(root_path)
        custom_rules = rules_manager.get_rules()
        if custom_rules:
            self.project_info.architecture_conventions.extend(custom_rules)

        # Example rule inference: if 'models' directory exists but doesn't import 'controllers'
        has_models = any('models' in path for path in self.project_info.micro_index.keys())
        has_controllers = any('controllers' in path for path in self.project_info.micro_index.keys())
        
        if has_models and has_controllers:
            self.project_info.architecture_conventions.append("Detected separation: Models layer exists independent of Controllers layer.")
            
        if self.project_info.framework:
            self.project_info.architecture_conventions.append(f"Follow {self.project_info.framework} idiomatic project structure conventions.")

    def _detect_project_type(self, config_files: List[FileInfo], root_path: Path) -> None:
        """
        检测项目类型

        Args:
            config_files: 配置文件列表
            root_path: 项目根路径
        """
        if not config_files:
            self.project_info.project_type = "通用项目"
            self.project_info.language = "Mixed"
            return

        detected_types: Set[str] = set()
        languages: Set[str] = set()

        for config_file in config_files:
            file_name = config_file.name
            if file_name in CONFIG_FILES:
                project_type = CONFIG_FILES[file_name]
                detected_types.add(project_type)

                if 'Python' in project_type:
                    languages.add('Python')
                elif 'JavaScript' in project_type or 'TypeScript' in project_type:
                    languages.add('JavaScript/TypeScript')
                elif 'Java' in project_type:
                    languages.add('Java')
                elif 'Go' in project_type:
                    languages.add('Go')
                elif 'Ruby' in project_type:
                    languages.add('Ruby')
                elif 'Rust' in project_type:
                    languages.add('Rust')
                elif 'PHP' in project_type:
                    languages.add('PHP')

        if len(detected_types) > 0:
            self.project_info.project_type = " / ".join(sorted(detected_types))
            self.project_info.config_files = [f.name for f in config_files]

        if languages:
            self.project_info.language = " / ".join(sorted(languages))

    def _extract_dependencies(self, config_files: List[FileInfo]) -> None:
        """
        提取项目依赖

        Args:
            config_files: 配置文件列表
        """
        for config_file in config_files:
            if config_file.name == 'package.json':
                self._parse_package_json(config_file.path)
            elif config_file.name in ['requirements.txt', 'pyproject.toml']:
                self._parse_python_deps(config_file)

    def _parse_package_json(self, file_path: Path) -> None:
        """
        解析 package.json 文件

        Args:
            file_path: package.json 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                data = json.loads(content)
                if 'name' in data and not self.project_info.name:
                    self.project_info.name = data['name']

                deps = {}
                if 'dependencies' in data:
                    deps.update(data['dependencies'])
                if 'devDependencies' in data:
                    deps.update(data['devDependencies'])

                self.project_info.dependencies = deps

                frameworks = []
                for dep in deps.keys():
                    if dep in JS_FRAMEWORK_INDICATORS:
                        frameworks.append(JS_FRAMEWORK_INDICATORS[dep])
                    elif any(indicator in dep.lower() for indicator in ['react', 'vue', 'angular', 'next', 'nuxt']):
                        frameworks.append(dep)

                self.project_info.tech_stack = list(set(frameworks))

            except json.JSONDecodeError:
                pass

        except (OSError, UnicodeDecodeError):
            pass

    def _parse_python_deps(self, config_file: FileInfo) -> None:
        """
        解析 Python 依赖文件

        Args:
            config_file: Python 配置文件
        """
        try:
            with open(config_file.path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            deps = {}

            if config_file.name == 'requirements.txt':
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('-'):
                        if '==' in line:
                            name, version = line.split('==', 1)
                            deps[name.strip()] = version.strip()
                        elif '>=' in line:
                            name, version = line.split('>=', 1)
                            deps[name.strip()] = f">={version.strip()}"
                        elif '~=' in line:
                            name, version = line.split('~=', 1)
                            deps[name.strip()] = f"~={version.strip()}"
                        else:
                            deps[line] = "latest"

            elif config_file.name == 'pyproject.toml':
                in_deps = False
                for line in lines:
                    if 'dependencies' in line.lower():
                        in_deps = True
                        continue
                    if in_deps:
                        if line.strip().startswith('['):
                            break
                        if '"' in line or "'" in line:
                            dep_str = line.strip().strip('",\'')
                            if dep_str:
                                deps[dep_str] = "latest"

            frameworks = []
            for dep_name in deps.keys():
                dep_lower = dep_name.lower().replace('-', '_').replace('_', '')
                for framework, name in PYTHON_FRAMEWORK_INDICATORS.items():
                    if framework.replace('-', '').replace('_', '') in dep_lower:
                        frameworks.append(name)

            self.project_info.dependencies = deps
            self.project_info.tech_stack = list(set(frameworks))

        except (OSError, UnicodeDecodeError):
            pass

    def _find_entry_points(self, all_files: List[FileInfo]) -> None:
        """
        查找项目入口文件

        Args:
            all_files: 所有文件列表
        """
        entry_point_patterns = [
            '__main__.py',
            'main.py',
            'app.py',
            'application.py',
            'index.js',
            'index.ts',
            'index.tsx',
            'index.jsx',
            'app.js',
            'app.ts',
            'App.js',
            'App.ts',
            'App.tsx',
            'App.jsx',
            'server.js',
            'server.ts',
            'server.py',
            'run.py',
            'cli.py',
            'manage.py',
            'wsgi.py',
            'asgi.py',
        ]

        entry_points = []

        for file_info in all_files:
            if file_info.name in entry_point_patterns:
                entry_points.append(str(file_info.path))

        self.project_info.entry_points = entry_points

    def _detect_framework(self, config_files: List[FileInfo], all_files: List[FileInfo]) -> None:
        """
        检测项目使用的框架

        Args:
            config_files: 配置文件列表
            all_files: 所有文件列表
        """
        framework = ""

        for config_file in config_files:
            if config_file.name == 'package.json':
                try:
                    with open(config_file.path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                        if 'next' in deps:
                            framework = "Next.js"
                        elif 'nuxt' in deps:
                            framework = "Nuxt.js"
                        elif '@nestjs/core' in deps:
                            framework = "NestJS"
                        elif 'gatsby' in deps:
                            framework = "Gatsby"
                        elif 'express' in deps:
                            framework = "Express.js"

                except (json.JSONDecodeError, OSError, UnicodeDecodeError):
                    pass

            elif config_file.name in ['requirements.txt', 'pyproject.toml']:
                for dep in self.project_info.dependencies.keys():
                    dep_lower = dep.lower()
                    if 'django' in dep_lower:
                        framework = "Django"
                        break
                    elif 'flask' in dep_lower:
                        framework = "Flask"
                        break
                    elif 'fastapi' in dep_lower:
                        framework = "FastAPI"
                        break

        if framework:
            self.project_info.framework = framework

        if framework and framework not in self.project_info.tech_stack:
            self.project_info.tech_stack.insert(0, framework)
