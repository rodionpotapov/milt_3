# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional

from ast_nodes import Seq, Pair
from errors import ParseError

class Parser:
    """
    Рекурсивный спуск для языка правильных скобочных записей с двумя видами скобок: (), [].
    Доп. ограничение: не более двух одинаковых скобок подряд (например, "(((" запрещено).
    """

    def __init__(self, src: str) -> None:
        self.s = src
        self.n = len(src)
        self.i = 0

        # Контроль "не более двух одинаковых подряд"
        self._last_ch: Optional[str] = None
        self._run_len: int = 0

    def parse(self) -> Seq:
        tree = self._S()
        if self._peek() is not None:
            ch = self._peek()
            raise ParseError(f"Лишний символ '{ch}' после конца выражения", self.i)
        return tree

    # -------------------- Грамматика (LL(1)) --------------------
    # S -> T S | ε
    # T -> '(' S ')' | '[' S ']'
    #
    # Доп. ограничение на подряд идущие одинаковые терминалы проверяем при чтении.

    def _S(self) -> Seq:
        items = []
        while True:
            ch = self._peek()
            if ch in ("(", "["):
                items.append(self._T())
                continue
            # ε: выходим, если следующий символ закрывающая скобка или конец
            if ch in (")", "]", None):
                break
            raise ParseError(f"Недопустимый символ '{ch}'", self.i)
        return Seq(items)

    def _T(self) -> Pair:
        ch = self._peek()
        if ch == "(":
            self._read("(")
            inside = self._S()
            self._read(")")
            return Pair("()", inside)
        if ch == "[":
            self._read("[")
            inside = self._S()
            self._read("]")
            return Pair("[]", inside)
        raise ParseError("Ожидалась открывающая скобка '(' или '['", self.i)

    # -------------------- Лексика/чтение --------------------

    def _peek(self) -> Optional[str]:
        if self.i >= self.n:
            return None
        return self.s[self.i]

    def _read(self, expected: str) -> None:
        ch = self._peek()
        if ch != expected:
            got = "конец строки" if ch is None else f"'{ch}'"
            raise ParseError(f"Ожидалось '{expected}', получено {got}", self.i)

        # Проверка ограничения по подряд идущим одинаковым скобкам
        if self._last_ch == ch:
            self._run_len += 1
        else:
            self._last_ch = ch
            self._run_len = 1

        if self._run_len > 2:
            raise ParseError(f"Нарушено ограничение: более двух одинаковых скобок подряд ('{ch}')", self.i)

        self.i += 1
