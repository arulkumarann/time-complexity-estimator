import pytest
from core.ast_parser import ASTParser

@pytest.mark.parametrize("code,expected_loops,expected_nesting", [
    ("for i in range(10): pass", 1, 1),
    ("for i in range(10):\n  for j in range(10): pass", 2, 2),
    ("while True:\n  pass", 1, 1),
    ("def f():\n  for i in range(5):\n    for j in range(5):\n      for k in range(5): pass", 3, 3),
])
def test_ast_parser_loops_and_nesting(code, expected_loops, expected_nesting):
    parser = ASTParser()
    result = parser.parse(code)
    assert len(result.loops) == expected_loops
    assert result.max_nesting_level == expected_nesting 