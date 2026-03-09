import pytest
from lexer import Lexer
from parser import Parser, ParserError


def parse_code(code):

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    parser.parse()


# -----------------------------
# Test Program Structure
# -----------------------------

def test_program_structure():

    code = """
namaskaram
nanni
"""

    parse_code(code)


# -----------------------------
# Test Assignment
# -----------------------------

def test_assignment():

    code = """
namaskaram
x = 5
nanni
"""

    parse_code(code)


# -----------------------------
# Test Print Statement
# -----------------------------

def test_print():

    code = """
namaskaram
ezhutuka("hello")
nanni
"""

    parse_code(code)


# -----------------------------
# Test Input Statement
# -----------------------------

def test_input():

    code = """
namaskaram
x = edukuka("Enter:")
nanni
"""

    parse_code(code)


# -----------------------------
# Test Arithmetic Expression
# -----------------------------

def test_expression():

    code = """
namaskaram
x = 5 + 3
nanni
"""

    parse_code(code)


# -----------------------------
# Test Complex Expression
# -----------------------------

def test_complex_expression():

    code = """
namaskaram
x = 5 + 3 * 2
nanni
"""

    parse_code(code)


# -----------------------------
# Test Print Expression
# -----------------------------

def test_print_expression():

    code = """
namaskaram
x = 5
ezhutuka(x + 2)
nanni
"""

    parse_code(code)


# -----------------------------
# Test Syntax Error
# -----------------------------

def test_missing_exit():

    code = """
namaskaram
x = 5
"""

    with pytest.raises(ParserError):
        parse_code(code)


# -----------------------------
# Test Invalid Statement
# -----------------------------

def test_invalid_statement():

    code = """
namaskaram
+ 5
nanni
"""

    with pytest.raises(ParserError):
        parse_code(code)