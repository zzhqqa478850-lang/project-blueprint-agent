"""
说明生成器模块
负责为每个文件夹生成功能说明
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from .scanner import DirectoryNode, FileInfo
from .analyzer import ProjectInfo
from .constants import FOLDER_NAME_PATTERNS, CONFIG_FILES


@dataclass
class FolderDescription:
    """文件夹描述数据类"""
    path: str
    description: str
    main_files: List[Dict[str, str]]
    file_count: int
    confidence: float

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'path': self.path,
            'description': self.description,
            'main_files': self.main_files,
            'file_count': self.file_count,
            'confidence': self.confidence
        }


class DescriptionGenerator:
    """说明生成器类"""

    def __init__(self):
        """初始化说明生成器"""
        self.project_info: Optional[ProjectInfo] = None
        self.folder_descriptions: Dict[str, FolderDescription] = {}

    def generate(
        self,
        root_node: DirectoryNode,
        project_info: ProjectInfo
    ) -> Dict[str, FolderDescription]:
        """
        为所有文件夹生成描述

        Args:
            root_node: 目录树根节点
            project_info: 项目信息

        Returns:
            Dict[str, FolderDescription]: 文件夹路径到描述的映射
        """
        self.project_info = project_info
        self.folder_descriptions = {}

        self._process_node(root_node)

        return self.folder_descriptions

    def _process_node(self, node: DirectoryNode) -> None:
        """
        处理目录节点

        Args:
            node: 目录节点
        """
        if node.name != '.' and node.relative_path != '.':
            description = self._analyze_folder(node)
            if description:
                self.folder_descriptions[node.relative_path] = description

        for subdir in node.subdirectories:
            self._process_node(subdir)

    def _analyze_folder(self, node: DirectoryNode) -> Optional[FolderDescription]:
        """
        分析文件夹并生成描述

        Args:
            node: 目录节点

        Returns:
            Optional[FolderDescription]: 文件夹描述
        """
        folder_name = node.name.lower()
        relative_path = str(node.relative_path)

        description_parts = []
        confidence = 0.5
        main_files = []

        pattern_description = self._check_folder_pattern(node, folder_name)
        if pattern_description:
            description_parts.append(pattern_description)
            confidence += 0.2

        config_description = self._check_config_files(node)
        if config_description:
            description_parts.append(config_description)
            confidence += 0.1

        content_description = self._analyze_content(node)
        if content_description:
            description_parts.append(content_description)
            confidence += 0.2

        for file_info in node.files[:10]:
            main_files.append({
                'name': file_info.name,
                'type': file_info.file_type,
                'is_config': file_info.is_config
            })

        if not description_parts:
            description_parts.append(f"包含 {len(node.files)} 个文件")

        final_description = "。".join(description_parts[:3])

        confidence = min(confidence, 1.0)

        return FolderDescription(
            path=relative_path,
            description=final_description,
            main_files=main_files,
            file_count=node.get_file_count(),
            confidence=confidence
        )

    def _check_folder_pattern(
        self,
        node: DirectoryNode,
        folder_name: str
    ) -> Optional[str]:
        """
        检查文件夹名称模式

        Args:
            node: 目录节点
            folder_name: 文件夹名称（小写）

        Returns:
            Optional[str]: 描述文本
        """
        if folder_name in FOLDER_NAME_PATTERNS:
            base_description = FOLDER_NAME_PATTERNS[folder_name]

            if node.files:
                file_types = set(f.file_type for f in node.files)
                if len(file_types) == 1:
                    file_type = list(file_types)[0]
                    if 'Python' in file_type or 'JavaScript' in file_type:
                        return f"{base_description}（{file_type}）"

            return base_description

        return None

    def _check_config_files(self, node: DirectoryNode) -> Optional[str]:
        """
        检查配置文件

        Args:
            node: 目录节点

        Returns:
            Optional[str]: 描述文本
        """
        config_in_folder = [f for f in node.files if f.is_config]

        if not config_in_folder:
            return None

        config_names = [f.name for f in config_in_folder]

        if 'package.json' in config_names:
            return "Node.js 项目配置"
        elif 'requirements.txt' in config_names or 'pyproject.toml' in config_names:
            return "Python 依赖配置"
        elif 'pom.xml' in config_names or 'build.gradle' in config_names:
            return "Java 项目构建配置"

        return None

    def _analyze_content(self, node: DirectoryNode) -> Optional[str]:
        """
        分析文件夹内容

        Args:
            node: 目录节点

        Returns:
            Optional[str]: 描述文本
        """
        if not node.files:
            return None

        file_names = [f.name for f in node.files]
        file_extensions = set(f.extension for f in node.files)

        if len(file_extensions) == 1:
            ext = list(file_extensions)[0]
            if ext == '.py':
                return self._analyze_python_files(node)
            elif ext in ['.js', '.jsx', '.ts', '.tsx']:
                return self._analyze_js_files(node)

        if len(node.files) <= 3:
            file_list = "、".join(file_names[:3])
            return f"包含文件：{file_list}"

        return None

    def _analyze_python_files(self, node: DirectoryNode) -> str:
        """
        分析 Python 文件

        Args:
            node: 目录节点

        Returns:
            str: 描述文本
        """
        keywords = {
            'test': '测试相关功能',
            'model': '数据模型定义',
            'view': '视图处理',
            'form': '表单处理',
            'api': 'API 接口',
            'serializer': '数据序列化',
            'validator': '数据验证',
            'middleware': '中间件',
            'exception': '异常处理',
            'utils': '工具函数',
            'helper': '辅助函数',
            'service': '业务服务',
            'manager': '管理器',
            'handler': '处理器',
            'controller': '控制器',
            'repository': '数据仓库',
        }

        for keyword, description in keywords.items():
            if any(keyword in f.name.lower() for f in node.files):
                return description

        return "Python 模块"

    def _analyze_js_files(self, node: DirectoryNode) -> str:
        """
        分析 JavaScript 文件

        Args:
            node: 目录节点

        Returns:
            str: 描述文本
        """
        keywords = {
            'test': '测试相关功能',
            'model': '数据模型',
            'component': 'React/Vue 组件',
            'page': '页面组件',
            'container': '容器组件',
            'service': '服务层',
            'api': 'API 接口',
            'store': '状态管理',
            'context': 'React Context',
            'hook': '自定义 Hook',
            'util': '工具函数',
            'helper': '辅助函数',
            'router': '路由配置',
            'route': '路由定义',
            'middleware': '中间件',
            'interceptor': '请求拦截器',
        }

        for keyword, description in keywords.items():
            if any(keyword in f.name.lower() for f in node.files):
                return description

        return "JavaScript/TypeScript 模块"

    def get_quick_navigation(
        self,
        root_node: DirectoryNode
    ) -> List[Dict[str, str]]:
        """
        生成快速导航表

        Args:
            root_node: 目录树根节点

        Returns:
            List[Dict[str, str]]: 导航信息列表
        """
        navigation = []

        important_folders = [
            ('api', 'API 接口'),
            ('apis', 'API 接口'),
            ('controllers', '控制器'),
            ('services', '服务层'),
            ('models', '数据模型'),
            ('views', '视图'),
            ('components', '组件'),
            ('pages', '页面'),
            ('routes', '路由'),
            ('middleware', '中间件'),
            ('utils', '工具函数'),
            ('config', '配置'),
            ('tests', '测试'),
            ('docs', '文档'),
        ]

        for subdir in root_node.subdirectories:
            folder_name = subdir.name.lower()

            for pattern, description in important_folders:
                if pattern in folder_name:
                    navigation.append({
                        'function': description,
                        'path': str(subdir.relative_path),
                        'file_count': str(subdir.get_file_count())
                    })
                    break

        return navigation
