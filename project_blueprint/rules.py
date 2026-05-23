import json
from pathlib import Path
from typing import List, Dict

class RulesManager:
    """管理项目架构规则和约束"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.rules_file = self.project_path / '.blueprint_rules.json'

    def _load_rules(self) -> Dict:
        """加载规则文件"""
        if not self.rules_file.exists():
            return {"architecture_conventions": []}
        
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"architecture_conventions": []}

    def _save_rules(self, data: Dict) -> None:
        """保存规则到文件"""
        with open(self.rules_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_rules(self) -> List[str]:
        """获取所有自定义架构规则"""
        data = self._load_rules()
        return data.get("architecture_conventions", [])

    def add_rule(self, rule: str) -> None:
        """添加一条新规则"""
        data = self._load_rules()
        rules = data.get("architecture_conventions", [])
        if rule not in rules:
            rules.append(rule)
            data["architecture_conventions"] = rules
            self._save_rules(data)

    def remove_rule(self, identifier: str) -> bool:
        """
        移除一条规则
        可以通过索引（数字字符串）或完全匹配的文本来删除
        """
        data = self._load_rules()
        rules = data.get("architecture_conventions", [])
        
        if not rules:
            return False

        # 尝试按索引删除
        if identifier.isdigit():
            idx = int(identifier) - 1
            if 0 <= idx < len(rules):
                rules.pop(idx)
                data["architecture_conventions"] = rules
                self._save_rules(data)
                return True
                
        # 尝试按文本完全匹配删除
        if identifier in rules:
            rules.remove(identifier)
            data["architecture_conventions"] = rules
            self._save_rules(data)
            return True
            
        return False
