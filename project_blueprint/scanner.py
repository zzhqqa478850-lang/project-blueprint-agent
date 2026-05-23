"""
目录扫描器模块
负责递归扫描项目目录，生成结构化的目录树
"""

import os
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field
from .constants import (
    DEFAULT_EXCLUDE_DIRS,
    DEFAULT_EXCLUDE_FILES,
    FILE_TYPE_MAPPING,
    MAX_DEPTH,
    MAX_FILES_PER_FOLDER
)


@dataclass
class FileInfo:
    """文件信息数据类"""
    name: str
    path: Path
    extension: str
    file_type: str
    size: int
    is_config: bool = False

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'name': self.name,
            'path': str(self.path),
            'extension': self.extension,
            'file_type': self.file_type,
            'size': self.size,
            'is_config': self.is_config
        }


@dataclass
class DirectoryNode:
    """目录节点数据类"""
    name: str
    path: Path
    relative_path: str
    files: List[FileInfo] = field(default_factory=list)
    subdirectories: List['DirectoryNode'] = field(default_factory=list)
    depth: int = 0

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'name': self.name,
            'path': str(self.path),
            'relative_path': self.relative_path,
            'files': [f.to_dict() for f in self.files],
            'subdirectories': [s.to_dict() for s in self.subdirectories],
            'depth': self.depth
        }

    def get_all_files(self) -> List[FileInfo]:
        """获取所有文件（包括子目录）"""
        all_files = self.files.copy()
        for subdir in self.subdirectories:
            all_files.extend(subdir.get_all_files())
        return all_files

    def get_file_count(self) -> int:
        """获取文件总数"""
        return len(self.files) + sum(s.get_file_count() for s in self.subdirectories)


class DirectoryScanner:
    """目录扫描器类"""

    def __init__(
        self,
        exclude_dirs: Optional[List[str]] = None,
        exclude_files: Optional[List[str]] = None,
        max_depth: int = MAX_DEPTH
    ):
        """
        初始化目录扫描器

        Args:
            exclude_dirs: 需要排除的目录名列表
            exclude_files: 需要排除的文件模式列表
            max_depth: 最大扫描深度
        """
        self.exclude_dirs = set(exclude_dirs or DEFAULT_EXCLUDE_DIRS)
        self.exclude_files = set(exclude_files or DEFAULT_EXCLUDE_FILES)
        self.max_depth = max_depth
        self.root_path: Optional[Path] = None

    def scan(self, root_path: str) -> DirectoryNode:
        """
        扫描目录并生成目录树

        Args:
            root_path: 根目录路径

        Returns:
            DirectoryNode: 目录树根节点
        """
        self.root_path = Path(root_path).resolve()

        if not self.root_path.exists():
            raise FileNotFoundError(f"目录不存在: {root_path}")

        if not self.root_path.is_dir():
            raise NotADirectoryError(f"路径不是目录: {root_path}")

        return self._scan_directory(self.root_path, self.root_path, 0)

    def _scan_directory(
        self,
        current_path: Path,
        root_path: Path,
        current_depth: int
    ) -> DirectoryNode:
        """
        递归扫描目录

        Args:
            current_path: 当前目录路径
            root_path: 根目录路径
            current_depth: 当前深度

        Returns:
            DirectoryNode: 目录节点
        """
        if current_path == root_path:
            rel_path = '.'
        else:
            rel_path = current_path.relative_to(root_path)
        
        node = DirectoryNode(
            name=current_path.name,
            path=current_path,
            relative_path=str(rel_path),
            depth=current_depth
        )

        if current_depth > self.max_depth:
            return node

        try:
            items = list(current_path.iterdir())
        except PermissionError:
            return node

        files = []
        subdirs = []

        for item in items:
            if self._should_exclude(item):
                continue

            if item.is_file():
                file_info = self._analyze_file(item)
                if file_info:
                    files.append(file_info)
            elif item.is_dir():
                subdir_node = self._scan_directory(item, root_path, current_depth + 1)
                if subdir_node.get_file_count() > 0 or len(subdir_node.subdirectories) > 0:
                    subdirs.append(subdir_node)

        files.sort(key=lambda x: (not x.is_config, x.name))
        subdirs.sort(key=lambda x: x.name)

        node.files = files[:MAX_FILES_PER_FOLDER]
        node.subdirectories = subdirs

        return node

    def _should_exclude(self, path: Path) -> bool:
        """
        检查路径是否应该被排除

        Args:
            path: 文件路径

        Returns:
            bool: 是否排除
        """
        if path.name in self.exclude_dirs:
            return True

        for pattern in self.exclude_files:
            if pattern.startswith('*.'):
                ext = pattern[1:]
                if path.name.endswith(ext):
                    return True

        return False

    def _analyze_file(self, file_path: Path) -> Optional[FileInfo]:
        """
        分析文件信息

        Args:
            file_path: 文件路径

        Returns:
            Optional[FileInfo]: 文件信息，如果文件有效则返回
        """
        try:
            stat = file_path.stat()
            size = stat.st_size
        except (OSError, PermissionError):
            size = 0

        name = file_path.name
        extension = file_path.suffix.lower()
        file_type = FILE_TYPE_MAPPING.get(extension, 'Unknown')

        from .constants import CONFIG_FILES
        is_config = name in CONFIG_FILES

        return FileInfo(
            name=name,
            path=file_path,
            extension=extension,
            file_type=file_type,
            size=size,
            is_config=is_config
        )

    def get_directory_tree_string(self, node: DirectoryNode, prefix: str = "", is_last: bool = True, is_root: bool = True) -> str:
        """
        生成目录树的字符串表示

        Args:
            node: 目录节点
            prefix: 前缀字符串
            is_last: 是否是最后一个
            is_root: 是否是根节点

        Returns:
            str: 目录树字符串
        """
        lines = []

        if node.name != '.' and not is_root:
            if prefix == "":
                lines.append(f"{node.name}/")
            else:
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{node.name}/")

            new_prefix = prefix + ("    " if is_last else "│   ")
        else:
            new_prefix = prefix
            if is_root and node.name == '.':
                lines.append(f"{self.root_path.name}/")

        for i, file_info in enumerate(node.files):
            is_last_file = (i == len(node.files) - 1) and len(node.subdirectories) == 0
            connector = "└── " if is_last_file else "├── "
            config_marker = " ⚙️" if file_info.is_config else ""
            lines.append(f"{new_prefix}{connector}{file_info.name}{config_marker}")

        for i, subdir in enumerate(node.subdirectories):
            is_last_subdir = (i == len(node.subdirectories) - 1)
            lines.append(self.get_directory_tree_string(
                subdir,
                new_prefix,
                is_last_subdir,
                is_root=False
            ))

        return "\n".join(lines)
