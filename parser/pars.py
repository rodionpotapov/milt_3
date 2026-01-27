class SyntaxErrorMLITA(Exception):
    """Синтаксическая ошибка."""
    pass


def parse(s: str, trace: bool = False) -> None:
    # Проверка алфавита
    for idx, ch in enumerate(s):
        if ch not in "()[]":
            raise SyntaxErrorMLITA(f"Недопустимый символ '{ch}' в позиции {idx}. Алфавит: ()[]")

    # Запрет '(((', ')))', '[[[', ']]]'
    for idx in range(len(s) - 2):
        if s[idx] == s[idx + 1] == s[idx + 2]:
            raise SyntaxErrorMLITA(f"Запрещено: '{s[idx]*3}' (начиная с позиции {idx}).")

    i = 0
    n = len(s)
    call_stack = []  # сюда кладём строки вида "Spos", "T()pos"

    def cur():
        return s[i] if i < n else None

    def _print_state(action: str):
        if not trace:
            return
        caret_line = " " * i + "^"
        stack_view = "верх\n" + ("\n".join(reversed(call_stack)) + "\n" if call_stack else "") + "низ"
        shown = s if s else "ε (пустая строка)"
        print(f"{action}\n{shown}\n{caret_line}\n{stack_view}\n{'-'*50}")

    def eat(expected: str):
        nonlocal i
        _print_state(f"eat('{expected}') — попытка")
        found = cur()
        if found != expected:
            if found is None:
                raise SyntaxErrorMLITA(f"Ожидался '{expected}', но конец строки (позиция {i}).")
            raise SyntaxErrorMLITA(f"Ожидался '{expected}', но найдено '{found}' (позиция {i}).")
        i += 1
        _print_state(f"eat('{expected}') — успешно, i := {i}")

    def S():
        call_stack.append(f"S{i}")
        _print_state("enter S")
        # S -> T S | ε
        while cur() in ("(", "["):
            _print_state("S: видим открывающую => вызвать T")
            T()
        # ε: на ')', ']', или конец
        _print_state("S: видим ')', ']' или конец => S -> ε (возврат)")
        call_stack.pop()

    def T():
        call_stack.append(f"T{i}")
        _print_state("enter T")
        # T -> ( S ) | [ S ]
        if cur() == "(":
            eat("(")
            S()
            eat(")")
        elif cur() == "[":
            eat("[")
            S()
            eat("]")
        else:
            found = cur()
            if found is None:
                raise SyntaxErrorMLITA(f"Ожидалась '(' или '[', но конец строки (позиция {i}).")
            raise SyntaxErrorMLITA(f"Ожидалась '(' или '[', но найдено '{found}' (позиция {i}).")
        _print_state("exit T")
        call_stack.pop()

    _print_state("START")
    S()
    if i != n:
        raise SyntaxErrorMLITA(f"Лишний символ '{s[i]}' (позиция {i}).")
    _print_state("ACCEPT: строка принята")


def main():
    print("Вариант: правильная скобочная запись с двумя видами скобок.")
    print("Ограничение: запрещены '(((', ')))', '[[[', ']]]'. Алфавит: ()[]")
    print("Ввод: строка без пробелов. Команды: exit/quit. Трассировка: trace on/off")
    print("-" * 60)

    trace = False
    while True:
        s = input("Строка> ").strip()

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