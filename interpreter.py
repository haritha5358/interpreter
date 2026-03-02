# interpreter.py


class Interpreter:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos]

        # Variable storage
        self.variables = {}


    # ---------------- UTILITY ---------------- #

    def advance(self):

        self.pos += 1

        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]


    def skip_newlines(self):

        while self.current.type == "NEWLINE":
            self.advance()


    # ---------------- MAIN ---------------- #

    def run(self):

        # Skip ENTRY
        self.advance()
        self.skip_newlines()


        while self.current.value != "EXIT":

            self.execute_statement()
            self.skip_newlines()


        print("✅ Program Finished")


    # ---------------- STATEMENTS ---------------- #

    def execute_statement(self):

        if self.current.value == "LET":
            self.execute_let()

        elif self.current.value == "PRINT":
            self.execute_print()

        elif self.current.value == "IF":
            self.execute_if()

        else:
            self.advance()


    # ---------------- LET ---------------- #

    def execute_let(self):

        # LET name = value

        self.advance()  # LET

        var_name = self.current.value
        self.advance()  # IDENTIFIER

        self.advance()  # =

        value = self.get_value()

        self.variables[var_name] = value


    # ---------------- PRINT ---------------- #

    def execute_print(self):

        self.advance()  # PRINT

        value = self.get_value()

        print(value)


    # ---------------- IF ---------------- #

    def execute_if(self):

        self.advance()  # IF

        result = self.evaluate_condition()

        self.advance()  # ?

        self.skip_newlines()


        if result:
            self.execute_statement()
        else:
            self.skip_statement()


        self.skip_newlines()


        # ELSE / ELSE IF
        while self.current.value == "ELSE":

            self.advance()

            # ELSE IF
            if self.current.value != "?":

                cond = self.evaluate_condition()
                self.advance()
                self.skip_newlines()

                if cond:
                    self.execute_statement()
                    return
                else:
                    self.skip_statement()

            # ELSE
            else:

                self.advance()
                self.skip_newlines()

                self.execute_statement()
                return


    # ---------------- HELPERS ---------------- #

    def get_value(self):

        token = self.current

        if token.type == "NUMBER":
            value = int(token.value)

        elif token.type == "STRING":
            value = token.value

        elif token.type == "IDENTIFIER":
            value = self.variables.get(token.value, 0)

        else:
            value = 0


        self.advance()
        return value


    def evaluate_condition(self):

        left = self.get_value()

        op = self.current.value
        self.advance()

        right = self.get_value()


        if op == ">":
            return left > right
        if op == "<":
            return left < right
        if op == "==":
            return left == right
        if op == "!=":
            return left != right

        return False


    def skip_statement(self):

        # Skip one statement

        while self.current.type not in ["NEWLINE", "EOF"]:
            self.advance()