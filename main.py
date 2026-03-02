# main.py

from lexer import Lexer
from parser import Parser, ParserError
from interpreter import Interpreter


def main():

    filename = "examples/test.mgl"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

    except FileNotFoundError:
        print("❌ File not found:", filename)
        return


    # -------- LEXER --------
    lexer = Lexer(code)
    tokens = lexer.tokenize()


    # -------- PARSER --------
    parser = Parser(tokens)

    try:
        parser.parse()
    except ParserError as e:
        print("❌", e)
        return


    # -------- INTERPRETER --------
    interpreter = Interpreter(tokens)
    interpreter.run()


if __name__ == "__main__":
    main()