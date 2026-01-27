# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List

from ast_nodes import Node, Seq, Pair

def tree_to_str(node: Node, indent: str = "") -> str:
    """Читаемое дерево разбора (для отчёта/проверки)."""
    lines: List[str] = []
    if isinstance(node, Seq):
        lines.append(f"{indent}Seq")
        for it in node.items:
            lines.append(tree_to_str(it, indent + "  "))
        return "\n".join(lines)
    if isinstance(node, Pair):
        lines.append(f"{indent}Pair {node.kind}")
        lines.append(tree_to_str(node.inside, indent + "  "))
        return "\n".join(lines)
    lines.append(f"{indent}{type(node).__name__}")
    return "\n".join(lines)
