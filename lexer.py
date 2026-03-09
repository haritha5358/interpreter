import re

TOKEN_KEYWORD = "KEYWORD"
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_STRING = "STRING"
TOKEN_NUMBER = "NUMBER"
TOKEN_OPERATOR = "OPERATOR"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_EOF = "EOF"

KEYWORDS = {
    "ezhutuka": "PRINT",
    "edukuka": "INPUT",
    "namaskaram": "ENTRY",
    "nanni": "EXIT"
}

OPERATORS = [
    "+", "-", "*", "/", "=",
    "(", ")", ">", "<", "==",
    "!=", ">=", "<="
]


class Token:

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"


class Lexer:

    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):

        lines = self.text.split("\n")

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            string_pattern = r'"(.*?)"'
            strings = re.findall(string_pattern, line)

            temp_line = re.sub(string_pattern, "STRING", line)

            words = re.findall(r'\d+\.\d+|\w+|==|!=|>=|<=|[()+\-*/=><]', temp_line)

            string_index = 0

            for word in words:

                if word == "STRING":
                    value = strings[string_index]
                    self.tokens.append(Token(TOKEN_STRING, value))
                    string_index += 1

                elif word in KEYWORDS:
                    self.tokens.append(Token(TOKEN_KEYWORD, KEYWORDS[word]))

                elif re.match(r'^\d+\.\d+$', word):
                    self.tokens.append(Token(TOKEN_NUMBER, word))

                elif word.isdigit():
                    self.tokens.append(Token(TOKEN_NUMBER, word))
                elif word in OPERATORS:
                    self.tokens.append(Token(TOKEN_OPERATOR, word))

                else:
                    self.tokens.append(Token(TOKEN_IDENTIFIER, word))

            self.tokens.append(Token(TOKEN_NEWLINE, "\\n"))

        self.tokens.append(Token(TOKEN_EOF, "EOF"))

        return self.tokens