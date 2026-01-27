# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ParseError(Exception):
    """Ошибка синтаксического анализа."""
    message: str
    position: int

    def __str__(self) -> str:
        return f"{self.message} (позиция {self.position})"
