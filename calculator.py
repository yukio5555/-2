#!/usr/bin/env python3
"""Simple CLI calculator.

Usage:
  python calculator.py "1 + 2 * 3"
"""

from __future__ import annotations

import argparse
import ast
import operator


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorError(ValueError):
    """Raised when an expression is invalid."""


def eval_expr(expr: str) -> float:
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise CalculatorError("式の構文が正しくありません") from exc

    return _eval_node(tree.body)


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        try:
            return OPS[type(node.op)](left, right)
        except ZeroDivisionError as exc:
            raise CalculatorError("0で割ることはできません") from exc

    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
        return UNARY_OPS[type(node.op)](_eval_node(node.operand))

    raise CalculatorError("使用できるのは数値と + - * / // % ** と括弧のみです")


def main() -> int:
    parser = argparse.ArgumentParser(description="簡単なCLI電卓")
    parser.add_argument("expression", nargs="?", help="計算式。例: '1 + 2 * (3 - 4)'")
    args, unknown = parser.parse_known_args()

    tokens = []
    if args.expression is not None:
        tokens.append(args.expression)
    tokens.extend(unknown)

    if not tokens:
        parser.error("the following arguments are required: expression")

    expression = " ".join(tokens)

    try:
        result = eval_expr(expression)
    except CalculatorError as exc:
        print(f"エラー: {exc}")
        return 1

    # 整数値なら見やすく表示
    if isinstance(result, float) and result.is_integer():
        print(int(result))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
