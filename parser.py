# parser.py


class ParserError(Exception):
    pass


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos]


    # ---------------- UTILITY ---------------- #

    def advance(self):

        self.pos += 1

        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]


    def eat(self, token_type, value=None):

        if self.current.type == token_type:

            if value is None or self.current.value == value:
                self.advance()

            else:
                self.error(
                    f"Expected {value}, got {self.current.value}"
                )

        else:
            self.error(
                f"Expected {token_type}, got {self.current.type}"
            )


    def error(self, msg):

        raise ParserError("Syntax Error: " + msg)


    # ---------------- MAIN ---------------- #

    def parse(self):

        # program -> ENTRY statements EXIT

        self.eat("KEYWORD", "ENTRY")

        self.skip_newlines()


        while self.current.value != "EXIT":

            self.statement()
            self.skip_newlines()


        self.eat("KEYWORD", "EXIT")

        # ✅ FIX: Skip blank lines before EOF
        self.skip_newlines()

        self.eat("EOF")

        print("✅ Parsing Successful!")


    # ---------------- STATEMENTS ---------------- #

    def statement(self):

        if self.current.value == "LET":
            self.let_statement()

        elif self.current.value == "PRINT":
            self.print_statement()

        elif self.current.value == "IF":
            self.if_statement()

        else:
            self.error(
                f"Invalid statement near '{self.current.value}'"
            )


    # ---------------- LET ---------------- #

    def let_statement(self):

        # LET id = expr

        self.eat("KEYWORD", "LET")

        self.eat("IDENTIFIER")

        self.eat("OPERATOR", "=")

        self.expression()


    # ---------------- PRINT ---------------- #

    def print_statement(self):

        # PRINT expr

        self.eat("KEYWORD", "PRINT")

        self.expression()


    # ---------------- IF / ELSE / ELSE-IF ---------------- #

    def if_statement(self):

        # IF condition ?
        self.eat("KEYWORD", "IF")

        self.condition()

        self.eat("OPERATOR", "?")

        self.skip_newlines()


        # IF body (single statement)
        self.statement()

        self.skip_newlines()


        # ELSE / ELSE IF
        while self.current.type == "KEYWORD" and self.current.value == "ELSE":

            self.eat("KEYWORD", "ELSE")


            # ELSE IF
            if self.current.type != "OPERATOR" or self.current.value != "?":

                self.condition()

                self.eat("OPERATOR", "?")

                self.skip_newlines()

                self.statement()

                self.skip_newlines()


            # ELSE
            else:

                self.eat("OPERATOR", "?")

                self.skip_newlines()

                self.statement()

                self.skip_newlines()


    # ---------------- CONDITION ---------------- #

    def condition(self):

        # expr OP expr

        self.expression()

        if self.current.type != "OPERATOR":
            self.error("Expected comparison operator")

        self.advance()

        self.expression()


    # ---------------- EXPRESSIONS ---------------- #

    def expression(self):

        if self.current.type in ["IDENTIFIER", "NUMBER", "STRING"]:
            self.advance()

        else:
            self.error(
                f"Invalid expression near '{self.current.value}'"
            )


    # ---------------- HELPERS ---------------- #

    def skip_newlines(self):

        while self.current.type == "NEWLINE":
            self.advance()