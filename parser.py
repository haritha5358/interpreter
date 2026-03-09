class ParserError(Exception):
    pass


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos]


    def advance(self):

        self.pos += 1

        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]


    def eat(self, token_type, value=None):

        if self.current.type == token_type:

            if value is None or self.current.value == value:
                self.advance()
            else:
                self.error(f"Expected {value}")

        else:
            self.error(f"Expected {token_type}")


    def error(self, msg):

        raise ParserError("Syntax Error: " + msg)


    def parse(self):

        self.eat("KEYWORD", "ENTRY")

        self.skip_newlines()

        while self.current.value != "EXIT":
            self.statement()
            self.skip_newlines()

        self.eat("KEYWORD", "EXIT")

        self.skip_newlines()

        self.eat("EOF")

        print("✅ Parsing Successful")


    def statement(self):

        if self.current.type == "KEYWORD" and self.current.value == "PRINT":
            self.print_statement()

        elif self.current.type == "IDENTIFIER":
            self.assignment()

        else:
            self.error("Invalid statement")


    def assignment(self):

        self.eat("IDENTIFIER")

        self.eat("OPERATOR", "=")

        self.expression()


    def print_statement(self):

        self.eat("KEYWORD", "PRINT")

        self.eat("OPERATOR", "(")

        self.expression()

        self.eat("OPERATOR", ")")


    def expression(self):

        self.term()

        while self.current.value in ["+", "-"]:
            self.advance()
            self.term()


    def term(self):

        self.factor()

        while self.current.value in ["*", "/"]:
            self.advance()
            self.factor()


    def factor(self):

        if self.current.type in ["NUMBER", "STRING", "IDENTIFIER"]:
            self.advance()

        elif self.current.type == "KEYWORD" and self.current.value == "INPUT":

            self.advance()

            self.eat("OPERATOR", "(")

            if self.current.type == "STRING":
                self.advance()

            self.eat("OPERATOR", ")")

        else:
            self.error("Invalid expression")


    def skip_newlines(self):

        while self.current.type == "NEWLINE":
            self.advance()