"""
Project Blueprint - 主入口文件
智能项目结构分析工具
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

from .scanner import DirectoryScanner
from .analyzer import ProjectAnalyzer
from .generator import DescriptionGenerator
from .documenter import DocumentGenerator
from .constants import DEFAULT_OUTPUT_FILENAME
from .rules import RulesManager


from typing import Union, Any

def analyze_project(
    project_path: str,
    output_filename: str = DEFAULT_OUTPUT_FILENAME,
    max_depth: int = 10,
    return_raw_data: bool = False,
    query: str = None,
    impact: str = None
) -> Union[str, Any]:
    """
    分析项目并生成蓝图文档

    Args:
        project_path: 项目路径
        output_filename: 输出文件名
        max_depth: 最大扫描深度

    Returns:
        str: 生成的消息
    """
    print(f"\n🔍 正在扫描项目目录：{project_path}")
    print(f"⏳ 这可能需要几秒钟时间...\n")

    project_path_obj = Path(project_path).resolve()

    if not project_path_obj.exists():
        return f"❌ 错误：目录不存在 - {project_path}"

    if not project_path_obj.is_dir():
        return f"❌ 错误：路径不是目录 - {project_path}"

    print(f"📂 步骤 1/4：扫描目录结构...")
    scanner = DirectoryScanner(max_depth=max_depth)
    try:
        root_node = scanner.scan(str(project_path_obj))
        file_count = root_node.get_file_count()
        print(f"   ✅ 扫描完成！发现 {file_count} 个文件")
    except Exception as e:
        return f"❌ 扫描目录时出错：{str(e)}"

    print(f"\n📊 步骤 2/4：分析项目信息...")
    analyzer = ProjectAnalyzer()
    try:
        project_info = analyzer.analyze(root_node, project_path_obj, query=query, impact=impact)
        print(f"   ✅ 项目类型：{project_info.project_type}")
        if project_info.tech_stack:
            print(f"   ✅ 技术栈：{', '.join(project_info.tech_stack[:5])}")
    except Exception as e:
        return f"❌ 分析项目信息时出错：{str(e)}"

    print(f"\n✍️  步骤 3/4：生成文件夹说明...")
    generator = DescriptionGenerator()
    try:
        folder_descriptions = generator.generate(root_node, project_info)
        print(f"   ✅ 生成 {len(folder_descriptions)} 个文件夹的说明")
    except Exception as e:
        return f"❌ 生成说明时出错：{str(e)}"

    print(f"\n📝 步骤 4/4：生成文档...")
    documenter = DocumentGenerator(output_filename=output_filename)
    try:
        doc = documenter.generate(
            root_node,
            project_info,
            folder_descriptions,
            project_path_obj
        )
        output_file = project_path_obj / output_filename
        print(f"   ✅ 文档已保存到：{output_file}")
    except Exception as e:
        return f"❌ 生成文档时出错：{str(e)}"

    if return_raw_data:
        return project_info

    message = f"""
✅ 分析完成！

📋 项目概览：
   - 项目名称：{project_info.name}
   - 项目类型：{project_info.project_type}
   - 发现文件：{file_count} 个
   - 分析文件夹：{len(folder_descriptions)} 个

📄 输出文档：{output_file}

💡 提示：
   - 打开 {output_filename} 查看完整分析结果
   - 文档包含目录结构、文件说明、快速导航等信息
   - 如需重新分析，可以删除生成的文档后再次运行
"""
    return message


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Project Blueprint - 智能项目结构分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python -m project_blueprint                    # 分析当前目录
  python -m project_blueprint /path/to/project   # 分析指定目录
  python -m project_blueprint -o MY_DOC.md       # 自定义输出文件名
  python -m project_blueprint -d 5               # 设置最大扫描深度为 5
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='要分析的项目路径（默认：当前目录）'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output',
        default=DEFAULT_OUTPUT_FILENAME,
        help=f'输出文件名（默认：{DEFAULT_OUTPUT_FILENAME}）'
    )

    parser.add_argument(
        '-d', '--depth',
        dest='depth',
        type=int,
        default=10,
        help='最大扫描深度（默认：10）'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Project Blueprint v1.0.0'
    )

    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='以 JSON 格式输出到标准输出（适合 Agent 调用）'
    )

    # 架构规则管理
    parser.add_argument('--add-rule', type=str, help='添加一条自定义架构规则')
    parser.add_argument('--remove-rule', type=str, help='移除一条自定义架构规则 (支持按文本或序号索引)')
    parser.add_argument('--list-rules', action='store_true', help='列出所有自定义架构规则')
    
    # 聚焦上下文和影响分析
    parser.add_argument('-q', '--query', type=str, help='只输出与特定模块相关的上下文')
    parser.add_argument('-i', '--impact', type=str, help='分析某个文件被哪些文件依赖 (影响分析)')

    args = parser.parse_args()

    project_path_obj = Path(args.path).resolve()
    
    # 处理规则管理命令
    if args.add_rule or args.remove_rule or args.list_rules:
        import json
        rules_manager = RulesManager(project_path_obj)
        result_data = {"status": "success", "architecture_conventions": []}
        
        if args.add_rule:
            rules_manager.add_rule(args.add_rule)
            result_data["message"] = f"Added rule: {args.add_rule}"
        elif args.remove_rule:
            success = rules_manager.remove_rule(args.remove_rule)
            result_data["message"] = "Rule removed successfully" if success else "Failed to remove rule"
            
        result_data["architecture_conventions"] = rules_manager.get_rules()
        
        if args.json:
            print(json.dumps(result_data, ensure_ascii=False, indent=2))
        else:
            print(result_data.get("message", "Current Rules:"))
            for i, rule in enumerate(result_data["architecture_conventions"]):
                print(f"{i+1}. {rule}")
        sys.exit(0)

    if args.json:
        # 在 JSON 模式下，重定向 stdout 以避免打印普通日志
        import io
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

    try:
        if args.json:
            project_info = analyze_project(
                project_path=args.path,
                output_filename=args.output,
                max_depth=args.depth,
                return_raw_data=True,
                query=args.query,
                impact=args.impact
            )
        else:
            result = analyze_project(
                project_path=args.path,
                output_filename=args.output,
                max_depth=args.depth,
                query=args.query,
                impact=args.impact
            )
    finally:
        if args.json:
            # 恢复 stdout
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
            "micro_index": getattr(project_info, 'micro_index', {}),
            "dependency_graph": getattr(project_info, 'dependency_graph', {}),
            "architecture_conventions": getattr(project_info, 'architecture_conventions', []),
            "output_file": str(Path(args.path).resolve() / args.output)
        }
        print(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        print(result)


if __name__ == '__main__':
    main()
