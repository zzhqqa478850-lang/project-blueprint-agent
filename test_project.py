# 快速测试脚本 - 测试 test_project 项目

import sys
from pathlib import Path

project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from project_blueprint.scanner import DirectoryScanner
from project_blueprint.analyzer import ProjectAnalyzer
from project_blueprint.generator import DescriptionGenerator
from project_blueprint.documenter import DocumentGenerator


def main():
    """主函数"""
    print("\n🔍 Project Blueprint - 智能项目结构分析工具")
    print("=" * 60)

    test_path = project_dir / 'test_project'
    print(f"\n正在分析示例项目目录：{test_path}")
    print(f"这可能需要几秒钟时间...\n")

    print("📂 步骤 1/4：扫描目录结构...")
    scanner = DirectoryScanner()
    try:
        root_node = scanner.scan(str(test_path))
        file_count = root_node.get_file_count()
        print(f"   ✅ 扫描完成！发现 {file_count} 个文件")
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return

    print("\n📊 步骤 2/4：分析项目信息...")
    analyzer = ProjectAnalyzer()
    try:
        project_info = analyzer.analyze(root_node, test_path)
        print(f"   ✅ 项目类型：{project_info.project_type}")
        if project_info.tech_stack:
            print(f"   ✅ 技术栈：{', '.join(project_info.tech_stack[:5])}")
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return

    print("\n✍️  步骤 3/4：生成文件夹说明...")
    generator = DescriptionGenerator()
    try:
        folder_descriptions = generator.generate(root_node, project_info)
        print(f"   ✅ 生成 {len(folder_descriptions)} 个文件夹的说明")
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return

    print("\n📝 步骤 4/4：生成文档...")
    documenter = DocumentGenerator()
    try:
        doc = documenter.generate(
            root_node,
            project_info,
            folder_descriptions,
            test_path
        )
        output_file = test_path / 'PROJECT_BLUEPRINT.md'
        print(f"   ✅ 文档已保存到：{output_file}")
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return

    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print(f"📄 打开 test_project/PROJECT_BLUEPRINT.md 查看完整分析结果")
    print("=" * 60)


if __name__ == '__main__':
    main()
