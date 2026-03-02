# lexer.py

import re


# ---------------- TOKEN TYPES ---------------- #

TOKEN_KEYWORD = "KEYWORD"
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_STRING = "STRING"
TOKEN_NUMBER = "NUMBER"
TOKEN_OPERATOR = "OPERATOR"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_EOF = "EOF"


# ---------------- KEYWORDS ---------------- #

KEYWORDS = {

    # Print
    "ezhutuka": "PRINT",

    # Condition
    "sathyamano": "IF",
    "athava": "ELSE",

    # Variables
    "iduka": "LET",
    "urapp": "CONST",

    # Loop
    "varunna_vare": "WHILE",

    # Function
    "pravarthanam": "FUNCTION",
    "thirichu_nalkuka": "RETURN",

    # Control
    "nirthuka": "BREAK",
    "tudaruka": "CONTINUE",

    # Program start / end
    "namaskaram": "ENTRY",
    "nanni": "EXIT"
}


# ---------------- OPERATORS ---------------- #

OPERATORS = [
    "+", "-", "*", "/", "%",
    "=", "==", "!=",
    ">", "<", ">=", "<=",
    "(", ")", "{", "}",
    "?"
]


# ---------------- TOKEN ---------------- #

class Token:

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type} : {self.value}"


# ---------------- LEXER ---------------- #

class Lexer:

    def __init__(self, text):
        self.text = text
        self.tokens = []


    def tokenize(self):

        lines = self.text.split("\n")

        for line in lines:

            line = line.strip()

            # Skip empty line
            if line == "":
                continue


            # ----- Handle strings -----

            string_pattern = r'"(.*?)"'
            strings = re.findall(string_pattern, line)

            temp_line = re.sub(string_pattern, "STRING", line)

            words = temp_line.split()

            string_index = 0


            for word in words:

                # STRING
                if word == "STRING":

                    value = strings[string_index]
                    self.tokens.append(Token(TOKEN_STRING, value))
                    string_index += 1


                # KEYWORD
                elif word in KEYWORDS:

                    self.tokens.append(
                        Token(TOKEN_KEYWORD, KEYWORDS[word])
                    )


                # NUMBER
                elif word.isdigit():

                    self.tokens.append(
                        Token(TOKEN_NUMBER, word)
                    )


                # OPERATOR
                elif word in OPERATORS:

                    self.tokens.append(
                        Token(TOKEN_OPERATOR, word)
                    )


                # IDENTIFIER
                else:

                    self.tokens.append(
                        Token(TOKEN_IDENTIFIER, word)
                    )


            # New line
            self.tokens.append(Token(TOKEN_NEWLINE, "\\n"))


        # End of file
        self.tokens.append(Token(TOKEN_EOF, "EOF"))

        return self.tokens