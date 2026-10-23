"""Structure checks for Lab 6: Morse Code.

These read `src/main.py` as Python, not as text, so the words in the story
and in comments do not count. Only real statements do. Each assertion message
says what was found and what was expected.
"""

import ast
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "src" / "main.py"


def tree():
    return ast.parse(SOURCE.read_text(encoding="utf-8"))


def function(name):
    for node in ast.walk(tree()):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"found no function named {name}: define it with def {name}(...)")


def inside(node, kind):
    return [n for n in ast.walk(node) if isinstance(n, kind)]


def called_names(node):
    names = set()
    for call in inside(node, ast.Call):
        if isinstance(call.func, ast.Name):
            names.add(call.func.id)
    return names


def test_the_books_are_built_in_loops():
    book = function("read_code_book")
    assert inside(book, ast.With), "found no `with open(...)` in read_code_book: open the file with a with block"
    assert inside(book, ast.For), "found no for loop in read_code_book: visit each line of the file"
    splits = [
        n for n in inside(book, ast.Call)
        if isinstance(n.func, ast.Attribute) and n.func.attr == "split"
    ]
    assert splits, "found no .split(...) in read_code_book: split each line at the comma"
    stores = [n for n in inside(book, ast.Subscript) if isinstance(n.ctx, ast.Store)]
    assert stores, "found no `book[...] = ...` in read_code_book: each line adds one entry"
    loops = [
        loop for loop in inside(tree(), ast.For)
        if isinstance(loop.iter, ast.Name) and loop.iter.id == "CODE"
    ]
    assert loops, "found no `for ... in CODE:` loop: one pass over the keys builds the reverse book"
    stores = [
        n for loop in loops for n in inside(loop, ast.Subscript)
        if isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name) and n.value.id == "LETTERS"
    ]
    assert stores, "found no `LETTERS[...] = ...` inside the loop: assign each pattern as a key, with its character as the value"


def test_to_morse_loops_over_the_text_and_checks_the_book():
    body = function("to_morse")
    assert inside(body, ast.For), "found no for loop in to_morse: visit each character of the text"
    checks = [
        n for n in inside(body, ast.Compare)
        if any(isinstance(op, (ast.In, ast.NotIn)) for op in n.ops)
    ]
    assert checks, "found no `in` or `not in` check in to_morse: skip a character the book does not have"


def test_the_key_is_read_in_while_loops_and_main_uses_the_functions():
    for name, least in (("press_length", 1), ("read_letter", 2), ("main", 1)):
        loops = inside(function(name), ast.While)
        assert len(loops) >= least, f"found {len(loops)} while loops in {name}, expected at least {least}"
    watching = [
        n for n in inside(function("press_length"), ast.Call)
        if isinstance(n.func, ast.Attribute) and n.func.attr == "value"
    ]
    assert watching, "found no button.value() call in press_length: the loop runs while the button reads 0"
    used = called_names(function("main"))
    missing = [name for name in ("read_letter", "from_morse", "to_morse") if name not in used]
    assert not missing, f"main does not call {', '.join(missing)}: main keys letters, decodes them and prints the patterns"
