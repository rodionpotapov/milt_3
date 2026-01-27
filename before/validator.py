# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from parser import Parser
from errors import ParseError
from ast_nodes import Seq

@dataclass(frozen=True)
class Result:
    ok: bool
    tree: Optional[Seq]
    error: Optional[ParseError]

def analyze(src: str) -> Result:
    try:
        tree = Parser(src).parse()
        return Result(True, tree, None)
    except ParseError as e:
        return Result(False, None, e)
