class Token:
    def __init__(self, value, category):
        self.value = value
        self.category = category


class LexicalAnalyzer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.position = 0
        self.token_list = []
        self.keywords = {"else", "if", "int", "return", "void", "while"}
        self.symbols = {
            "+",
            "-",
            "*",
            "/",
            "<",
            "<=",
            ">",
            ">=",
            "==",
            "!=",
            "=",
            ";",
            ",",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
        }
        self.operators = {"+", "-", "*", "/"}
        self.relational_operators = {"<=", "<", ">", ">=", "==", "!="}

    def analyze(self):
        while self.position < len(self.input_string):
            if self.input_string[self.position].isspace():
                self.position += 1
            elif self.input_string[self.position] in self.symbols:
                self.add_token(self.input_string[self.position], "sym")
                self.position += 1
            elif self.input_string[self.position].isdigit():
                num = ""
                while (
                    self.position < len(self.input_string)
                    and self.input_string[self.position].isdigit()
                ):
                    num += self.input_string[self.position]
                    self.position += 1
                self.add_token(num, "num")
            elif (
                self.input_string[self.position].isalpha()
                or self.input_string[self.position] == "_"
            ):
                identifier = ""
                while self.position < len(self.input_string) and (
                    self.input_string[self.position].isalpha()
                    or self.input_string[self.position].isdigit()
                    or self.input_string[self.position] == "_"
                ):
                    identifier += self.input_string[self.position]
                    self.position += 1
                if identifier in self.keywords:
                    self.add_token(identifier, "kw")
                else:
                    self.add_token(identifier, "id")
            else:
                self.invalid_symbol()

    def add_token(self, value, category):
        token = Token(value, category)
        self.token_list.append(token)

    def invalid_symbol(self):
        raise SystemExit

    def get_tokens(self):
        return self.token_list
