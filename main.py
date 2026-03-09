from lexer import Lexer
from parser import Parser, ParserError
from interpreter import Interpreter


def main():

    filename = "examples/test.mgl"

    with open(filename, "r") as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)

    try:
        parser.parse()
    except ParserError as e:
        print(e)
        return

    interpreter = Interpreter(tokens)
    interpreter.run()


if __name__ == "__main__":
    main()