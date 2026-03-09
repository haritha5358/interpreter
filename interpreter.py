class Interpreter:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos]

        self.variables = {}


    def advance(self):

        self.pos += 1

        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]


    def skip_newlines(self):

        while self.current.type == "NEWLINE":
            self.advance()


    def run(self):

        self.advance()
        self.skip_newlines()

        while self.current.value != "EXIT":

            self.execute_statement()

            self.skip_newlines()

        print("✅ Program Finished")


    def execute_statement(self):

        if self.current.type == "KEYWORD" and self.current.value == "PRINT":
            self.execute_print()

        elif self.current.type == "IDENTIFIER":
            self.execute_assignment()

        else:
            self.advance()


    def execute_assignment(self):

        var = self.current.value
        self.advance()
        self.advance()

        value = self.evaluate_expression()

        self.variables[var] = value


    def execute_print(self):

        self.advance()
        self.advance()

        value = self.evaluate_expression()

        self.advance()

        print(value)


    def evaluate_expression(self):

        left = self.evaluate_term()

        while self.current.value in ["+", "-"]:

            op = self.current.value
            self.advance()

            right = self.evaluate_term()

            if op == "+":
                left = str(left) + str(right) if isinstance(left,str) or isinstance(right,str) else left + right
            elif op == "-":
                left = left - right

        return left


    def evaluate_term(self):

        left = self.evaluate_factor()

        while self.current.value in ["*", "/"]:

            op = self.current.value
            self.advance()

            right = self.evaluate_factor()

            if op == "*":
                left = left * right
            elif op == "/":
                left = left / right

        return left


    def evaluate_factor(self):

        token = self.current

        if token.type == "NUMBER":
            self.advance()

            if "." in token.value:
                return float(token.value)
            else:
                return int(token.value)

        elif token.type == "STRING":

            self.advance()
            return token.value

        elif token.type == "IDENTIFIER":

            self.advance()
            return self.variables.get(token.value, 0)

        elif token.type == "KEYWORD" and token.value == "INPUT":

            self.advance()
            self.advance()

            prompt = ""

            if self.current.type == "STRING":
                prompt = self.current.value
                self.advance()

            self.advance()

            value = input(prompt)

            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return value

        return 0