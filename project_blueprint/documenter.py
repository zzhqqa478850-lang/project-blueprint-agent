"""
文档生成器模块
负责将分析结果生成为美观的 Markdown 文档
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from .scanner import DirectoryNode
from .analyzer import ProjectInfo
from .generator import FolderDescription
from .constants import DEFAULT_OUTPUT_FILENAME


class DocumentGenerator:
    """文档生成器类"""

    def __init__(self, output_filename: Optional[str] = None):
        """
        初始化文档生成器

        Args:
            output_filename: 输出文件名
        """
        self.output_filename = output_filename or DEFAULT_OUTPUT_FILENAME

    def generate(
        self,
        root_node: DirectoryNode,
        project_info: ProjectInfo,
        folder_descriptions: Dict[str, FolderDescription],
        output_path: Path
    ) -> str:
        """
        生成 Markdown 文档

        Args:
            root_node: 目录树根节点
            project_info: 项目信息
            folder_descriptions: 文件夹描述
            output_path: 输出路径

        Returns:
            str: 文档内容
        """
        from .scanner import DirectoryScanner

        scanner = DirectoryScanner()
        tree_string = scanner.get_directory_tree_string(root_node)

        doc = self._build_document(
            project_info,
            tree_string,
            folder_descriptions,
            root_node
        )

        output_file = output_path / self.output_filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc)

        return doc

    def _build_document(
        self,
        project_info: ProjectInfo,
        tree_string: str,
        folder_descriptions: Dict[str, FolderDescription],
        root_node: DirectoryNode
    ) -> str:
        """
        构建文档内容

        Args:
            project_info: 项目信息
            tree_string: 目录树字符串
            folder_descriptions: 文件夹描述
            root_node: 目录树根节点

        Returns:
            str: Markdown 文档内容
        """
        lines = []

        lines.append("# 📋 Project Blueprint")
        lines.append("")
        lines.append("> 本文档由 Project Blueprint 自动生成")
        lines.append("")

        lines.extend(self._build_project_overview(project_info))
        
        lines.extend(self._build_architecture_conventions(project_info))

        lines.append("")
        lines.append("## 📁 目录结构")
        lines.append("")
        lines.append("```")
        lines.append(tree_string)
        lines.append("```")
        lines.append("")

        lines.extend(self._build_folder_descriptions(folder_descriptions))

        from .generator import DescriptionGenerator
        gen = DescriptionGenerator()
        navigation = gen.get_quick_navigation(root_node)

        if navigation:
            lines.append("")
            lines.append("## 🎯 快速导航")
            lines.append("")
            lines.append("| 功能 | 路径 | 文件数 |")
            lines.append("|------|------|--------|")
            for nav in navigation:
                lines.append(f"| {nav['function']} | `{nav['path']}` | {nav['file_count']} |")
            lines.append("")

        lines.extend(self._build_run_instructions(project_info))

        lines.append("")
        lines.append("---")
        lines.append(f"*📅 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("*🔧 使用 Project Blueprint 生成*")

        return "\n".join(lines)

    def _build_project_overview(self, project_info: ProjectInfo) -> List[str]:
        """
        构建项目概览部分

        Args:
            project_info: 项目信息

        Returns:
            List[str]: Markdown 行列表
        """
        lines = []
        lines.append("## 📊 项目概览")
        lines.append("")

        lines.append(f"- **项目名称**：{project_info.name}")
        lines.append(f"- **项目类型**：{project_info.project_type}")
        lines.append(f"- **主要语言**：{project_info.language}")

        if project_info.framework:
            lines.append(f"- **框架**：{project_info.framework}")

        if project_info.tech_stack:
            tech_stack_str = "、".join(project_info.tech_stack[:10])
            if len(project_info.tech_stack) > 10:
                tech_stack_str += f" 等（共 {len(project_info.tech_stack)} 个）"
            lines.append(f"- **技术栈**：{tech_stack_str}")

        lines.append(f"- **生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        if project_info.dependencies:
            lines.append("**主要依赖**：")
            lines.append("")
            lines.append("```")
            dep_items = list(project_info.dependencies.items())
            for name, version in dep_items[:15]:
                lines.append(f"{name}: {version}")
            if len(dep_items) > 15:
                lines.append(f"... 还有 {len(dep_items) - 15} 个依赖")
            lines.append("```")
            lines.append("")

        if project_info.entry_points:
            lines.append("**入口文件**：")
            lines.append("")
            for entry in project_info.entry_points[:5]:
                lines.append(f"- `{entry}`")
            lines.append("")

        return lines

    def _build_architecture_conventions(self, project_info: ProjectInfo) -> List[str]:
        """
        构建架构规范部分
        """
        lines = []
        if not project_info.architecture_conventions:
            return lines

        lines.append("")
        lines.append("## 🛡️ 架构规范与守卫")
        lines.append("")
        lines.append("> 以下是该项目必须遵守的架构约定，Agent 修改代码前应严格遵循：")
        lines.append("")
        
        for rule in project_info.architecture_conventions:
            lines.append(f"- {rule}")
            
        lines.append("")
        return lines

    def _build_folder_descriptions(
        self,
        folder_descriptions: Dict[str, FolderDescription]
    ) -> List[str]:
        """
        构建文件夹描述部分

        Args:
            folder_descriptions: 文件夹描述字典

        Returns:
            List[str]: Markdown 行列表
        """
        lines = []
        lines.append("## 📄 文件说明")
        lines.append("")

        if not folder_descriptions:
            lines.append("*暂无文件夹描述*")
            return lines

        sorted_paths = sorted(
            folder_descriptions.keys(),
            key=lambda x: (x.count('/'), x)
        )

        for path in sorted_paths:
            desc = folder_descriptions[path]
            lines.append(f"### {path}")
            lines.append("")
            lines.append(f"**{desc.description}**")
            lines.append("")

            if desc.main_files:
                lines.append(f"**主要文件**（共 {desc.file_count} 个文件）：")
                lines.append("")

                for file_info in desc.main_files[:8]:
                    config_marker = " ⚙️" if file_info.get('is_config') else ""
                    lines.append(f"- `{file_info['name']}` - {file_info['type']}{config_marker}")

                if len(desc.main_files) > 8:
                    lines.append(f"- *... 还有 {len(desc.main_files) - 8} 个文件*")

            lines.append("")

        return lines

    def _build_run_instructions(self, project_info: ProjectInfo) -> List[str]:
        """
        构建运行说明部分

        Args:
            project_info: 项目信息

        Returns:
            List[str]: Markdown 行列表
        """
        lines = []
        lines.append("## 🔧 运行方式")
        lines.append("")

        run_commands = []

        if 'JavaScript' in project_info.language or 'package.json' in project_info.config_files:
            run_commands.extend([
                "```bash",
                "# 安装依赖",
                "npm install",
                "",
                "# 开发模式",
                "npm run dev",
                "",
                "# 生产构建",
                "npm run build",
                "```"
            ])

        elif 'Python' in project_info.language:
            run_commands.extend([
                "```bash",
                "# 安装依赖",
                "pip install -r requirements.txt",
                "",
                "# 运行项目",
                "python main.py",
                "```"
            ])

        elif 'Java' in project_info.language:
            if 'pom.xml' in project_info.config_files:
                run_commands.extend([
                    "```bash",
                    "# 编译项目",
                    "mvn compile",
                    "",
                    "# 运行项目",
                    "mvn exec:java",
                    "",
                    "# 打包",
                    "mvn package",
                    "```"
                ])
            elif 'build.gradle' in project_info.config_files:
                run_commands.extend([
                    "```bash",
                    "# 编译项目",
                    "./gradlew build",
                    "",
                    "# 运行项目",
                    "./gradlew run",
                    "",
                    "# 打包",
                    "./gradlew jar",
                    "```"
                ])

        if run_commands:
            lines.extend(run_commands)
        else:
            lines.append("*暂无运行说明*")

        return lines
