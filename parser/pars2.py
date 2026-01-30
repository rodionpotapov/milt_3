#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class SyntaxErrorMLITA(Exception):
    pass


def parse(s: str, trace: bool = False) -> None:
    # Алфавит строго: ()[] , пробелы/табы/переводы строк НЕ допускаются
    for idx, ch in enumerate(s):
        if ch not in "()[]":
            raise SyntaxErrorMLITA(f"Недопустимый символ '{ch}' в позиции {idx}")

    i = 0
    n = len(s)
    call_stack = []

    def cur():
        return s[i] if i < n else None

    def _print_state(action: str):
        if not trace:
            return
        caret = " " * i + "^"
        stack = "верх\n" + "\n".join(reversed(call_stack)) + "\nниз"
        print(f"{action}\n{s}\n{caret}\n{stack}\n{'-'*50}")

    def eat(expected: str):
        nonlocal i
        _print_state(f"eat({expected})")
        if cur() != expected:
            found = cur()
            if found is None:
                raise SyntaxErrorMLITA(f"Ожидался '{expected}', найден конец строки (позиция {i})")
            raise SyntaxErrorMLITA(f"Ожидался '{expected}', найдено '{found}' (позиция {i})")
        i += 1

    # Грамматика:
    # S     -> Seq
    # Seq   -> ε | Block Seq1
    # Seq1  -> ε | Block
    # Block -> Round | Square
    # Round -> ( Seq )
    # Square -> [ Seq ]

    def parse_S():
        call_stack.append("S")
        _print_state("S")
        parse_Seq()
        call_stack.pop()

    def parse_Seq():
        call_stack.append("Seq")
        _print_state("Seq")
        if cur() in ("(", "["):
            parse_Block()
            parse_Seq1()
        # иначе ε
        call_stack.pop()

    def parse_Seq1():
        call_stack.append("Seq1")
        _print_state("Seq1")
        if cur() in ("(", "["):
            parse_Block()
        # иначе ε
        call_stack.pop()

    def parse_Block():
        call_stack.append("Block")
        _print_state("Block")
        if cur() == "(":
            parse_Round()
        elif cur() == "[":
            parse_Square()
        else:
            found = cur()
            if found is None:
                raise SyntaxErrorMLITA(f"Ожидался блок '(' или '[', найден конец строки (позиция {i})")
            raise SyntaxErrorMLITA(f"Ожидался блок '(' или '[', найдено '{found}' (позиция {i})")
        call_stack.pop()

    def parse_Round():
        call_stack.append("Round")
        _print_state("Round")
        eat("(")
        parse_Seq()
        eat(")")
        call_stack.pop()

    def parse_Square():
        call_stack.append("Square")
        _print_state("Square")
        eat("[")
        parse_Seq()
        eat("]")
        call_stack.pop()

    _print_state("START")
    parse_S()
    if i != n:
        raise SyntaxErrorMLITA(f"Лишний символ '{s[i]}' (позиция {i})")
    _print_state("ACCEPT")


def main():
    print("Вариант: правильная скобочная запись с двумя видами скобок")
    print("Ограничение: на каждом уровне подряд не более двух скобочных блоков (пары () или [])")
    print("Алфавит: ()[]  Пробелы/табы/переводы строк НЕ допускаются")
    print("Команды: exit/quit, trace on/off")
    print("-" * 60)

    trace = False
    while True:
        s = input("Строка> ")

        if s.lower() in {"exit", "quit"}:
            print("Выход.")
            return

        if s.lower() == "trace on":
            trace = True
            print("Трассировка: ВКЛ")
            continue
        if s.lower() == "trace off":
            trace = False
            print("Трассировка: ВЫКЛ")
            continue

        try:
            parse(s, trace=trace)
            print("OK")
        except SyntaxErrorMLITA as e:
            print(f"ERROR: {e}")
        print("-" * 60)


if __name__ == "__main__":
    main()