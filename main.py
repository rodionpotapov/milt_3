# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional

from validator import analyze
from pretty import tree_to_str

TASK_TEXT = """ИДЗ-3. Построение синтаксического анализатора.

Вариант: правильная скобочная запись с двумя видами скобок () и [].
Дополнительное ограничение: подряд могут стоять не более двух одинаковых скобок.

Примеры:
  Правильная:   [(()[])](()[()])
  Неправильная: [()([]([]()()))]

Ввод: строка, состоящая только из символов '()[]' (без пробелов).
Вывод: принадлежит ли строка языку; при успехе печатается дерево разбора.
"""

def _prompt() -> str:
    return input("Введите выражение (пустая строка = выход): ").strip()

def main() -> int:
    print(TASK_TEXT)
    while True:
        s = _prompt()
        if s == "":
            return 0

        res = analyze(s)
        if res.ok:
            print("OK: строка принадлежит языку.")
            print(tree_to_str(res.tree))  # type: ignore[arg-type]
        else:
            err = res.error
            print("NO: строка не принадлежит языку.")
            print(str(err))
        print()

if __name__ == "__main__":
    raise SystemExit(main())
