"""Runs generated analysis inside the disposable no-network container."""

import ast
import io
import json
import math
import os
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


class CappedOutput(io.StringIO):
    def write(self, value):
        if self.tell() + len(value.encode("utf-8", "replace")) > 6000:
            raise RuntimeError("Analysis output exceeded its limit")
        return super().write(value)


def validate(tree):
    blocked_calls = {"eval", "exec", "compile", "input", "globals", "locals", "vars", "getattr", "setattr", "delattr", "breakpoint", "help"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Imports are disabled in the analysis script")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise ValueError("Dunder attributes are disabled")
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            raise ValueError("Dunder names are disabled")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in blocked_calls:
            raise ValueError("This operation is disabled")


class StripPreloadedImports(ast.NodeTransformer):
    """Allow harmless imports for names already injected into the sandbox scope."""
    allowed = {
        "pandas": "pd",
        "matplotlib.pyplot": "plt",
        "json": "json",
        "math": "math",
        "statistics": "statistics",
    }

    def visit_Import(self, node):
        for alias in node.names:
            expected = self.allowed.get(alias.name)
            if expected is None:
                raise ValueError("Only preloaded analysis libraries are available")
            if expected != alias.asname and not (
                alias.name in ("json", "math", "statistics") and alias.asname is None
            ):
                raise ValueError("Only preloaded analysis libraries are available")
        return None

    def visit_ImportFrom(self, node):
        raise ValueError("Imports from modules are disabled")


def main():
    os.makedirs("/tmp/mpl", exist_ok=True)
    os.environ["MPLCONFIGDIR"] = "/tmp/mpl"
    source = open("/workspace/analysis.py", "r", encoding="utf-8").read()
    tree = ast.parse(source, filename="analysis.py", mode="exec")
    tree = StripPreloadedImports().visit(tree)
    tree = ast.fix_missing_locations(tree)
    validate(tree)
    safe_builtins = {
        "abs": abs, "all": all, "any": any, "bool": bool, "dict": dict,
        "enumerate": enumerate, "filter": filter, "float": float, "int": int,
        "len": len, "list": list, "map": map, "max": max, "min": min,
        "range": range, "repr": repr, "reversed": reversed, "round": round,
        "print": print,
        "set": set, "sorted": sorted, "str": str, "sum": sum, "tuple": tuple,
        "zip": zip,
    }
    stdout = CappedOutput()
    scope = {
        "__builtins__": safe_builtins,
        "pd": pd,
        "plt": plt,
        "json": json,
        "math": math,
        "statistics": statistics,
    }
    old_stdout = sys.stdout
    try:
        sys.stdout = stdout
        exec(compile(tree, "analysis.py", "exec"), scope, scope)
    finally:
        sys.stdout = old_stdout
    with open("/workspace/result.txt", "w", encoding="utf-8") as output:
        output.write(stdout.getvalue()[:6000])


if __name__ == "__main__":
    main()
