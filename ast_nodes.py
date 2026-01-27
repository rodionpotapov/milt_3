# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Union

BracketKind = Literal["()", "[]"]

@dataclass(frozen=True)
class Node:
    """Узел дерева разбора."""
    pass

@dataclass(frozen=True)
class Seq(Node):
    """Последовательность элементов."""
    items: List[Node]

@dataclass(frozen=True)
class Pair(Node):
    """Скобочная пара с вложенным содержимым."""
    kind: BracketKind
    inside: Seq
