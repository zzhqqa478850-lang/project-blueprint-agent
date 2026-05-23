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
