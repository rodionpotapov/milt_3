# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from graphviz import Digraph

OUT_DIR = "diagrams_ll1"

def _term(g: Digraph, name: str, label: str) -> None:
    g.node(name, label=label, shape="oval")

def _nonterm(g: Digraph, name: str, label: str) -> None:
    g.node(name, label=label, shape="box")

def _op(g: Digraph, name: str, label: str) -> None:
    g.node(name, label=label, shape="rectangle")

def _dec(g: Digraph, name: str, label: str) -> None:
    g.node(name, label=label, shape="diamond")

def _point(g: Digraph, name: str) -> None:
    g.node(name, label="", shape="point")

def _io(g: Digraph, name: str, label: str) -> None:
    g.node(name, label=label, shape="parallelogram")

def render_S(path_dir: str) -> None:
    g = Digraph("S")
    g.attr(rankdir="LR")

    _point(g, "in")
    _point(g, "out")
    _dec(g, "d", "peek ∈ { '(', '[' } ?")
    _nonterm(g, "T", "T")

    g.edge("in", "d")
    g.edge("d", "T", label="да")
    g.edge("T", "d")
    g.edge("d", "out", label="нет (ε)")

    os.makedirs(path_dir, exist_ok=True)
    g.render(filename=os.path.join(path_dir, "S"), format="png", cleanup=True)
    g.save(filename=os.path.join(path_dir, "S.dot"))

def render_T(path_dir: str) -> None:
    g = Digraph("T")
    g.attr(rankdir="LR")

    _point(g, "in")
    _point(g, "out")
    _dec(g, "d", "peek")

    _term(g, "lpar", "(")
    _nonterm(g, "S1", "S")
    _term(g, "rpar", ")")

    _term(g, "lbr", "[")
    _nonterm(g, "S2", "S")
    _term(g, "rbr", "]")

    g.edge("in", "d")

    g.edge("d", "lpar", label="'('")
    g.edge("lpar", "S1")
    g.edge("S1", "rpar")
    g.edge("rpar", "out")

    g.edge("d", "lbr", label="'['")
    g.edge("lbr", "S2")
    g.edge("S2", "rbr")
    g.edge("rbr", "out")

    os.makedirs(path_dir, exist_ok=True)
    g.render(filename=os.path.join(path_dir, "T"), format="png", cleanup=True)
    g.save(filename=os.path.join(path_dir, "T.dot"))

def render_PEEK(path_dir: str) -> None:
    g = Digraph("PEEK")
    g.attr(rankdir="LR")

    _point(g, "in")
    _point(g, "out")
    _dec(g, "d", "i >= n ?")
    _io(g, "ret_end", "return end")
    _io(g, "ret_ch", "return s[i]")

    g.edge("in", "d")
    g.edge("d", "ret_end", label="да")
    g.edge("d", "ret_ch", label="нет")
    g.edge("ret_end", "out")
    g.edge("ret_ch", "out")

    os.makedirs(path_dir, exist_ok=True)
    g.render(filename=os.path.join(path_dir, "PEEK"), format="png", cleanup=True)
    g.save(filename=os.path.join(path_dir, "PEEK.dot"))

def render_READ(path_dir: str) -> None:
    g = Digraph("READ")
    g.attr(rankdir="LR")

    _point(g, "in")
    _point(g, "out")

    _op(g, "get", "ch := peek()")
    _dec(g, "eq", "ch == expected ?")

    _io(g, "err_exp", "error: expected/ got")

    _dec(g, "same", "last_ch == ch ?")
    _op(g, "inc", "run_len := run_len + 1")
    _op(g, "reset", "last_ch := ch; run_len := 1")

    _dec(g, "too", "run_len > 2 ?")
    _io(g, "err_run", "error: >2 same in a row")

    _op(g, "adv", "i := i + 1")

    g.edge("in", "get")
    g.edge("get", "eq")
    g.edge("eq", "err_exp", label="нет")
    g.edge("eq", "same", label="да")

    g.edge("same", "inc", label="да")
    g.edge("same", "reset", label="нет")

    g.edge("inc", "too")
    g.edge("reset", "too")

    g.edge("too", "err_run", label="да")
    g.edge("too", "adv", label="нет")

    g.edge("err_exp", "out")
    g.edge("err_run", "out")
    g.edge("adv", "out")

    os.makedirs(path_dir, exist_ok=True)
    g.render(filename=os.path.join(path_dir, "READ"), format="png", cleanup=True)
    g.save(filename=os.path.join(path_dir, "READ.dot"))

def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    render_S(OUT_DIR)
    render_T(OUT_DIR)
    render_PEEK(OUT_DIR)
    render_READ(OUT_DIR)
    print(f"Готово: ./{OUT_DIR}/S.png, T.png, PEEK.png, READ.png (и .dot)")

if __name__ == "__main__":
    main() 