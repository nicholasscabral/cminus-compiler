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
        self.state = 1

    def analyze(self):
        while self.position < len(self.input_string):
            if self.state == 1:  # Identifier, number, or symbol
                if self.input_string[self.position : self.position + 1] in self.symbols:
                    self.add_token(
                        self.input_string[self.position : self.position + 1], "sym"
                    )
                    self.position += 1
                    self.state = 1
                elif self.input_string[self.position : self.position + 1].isdigit():
                    self.state = 3
                elif self.input_string[self.position : self.position + 1].isalpha():
                    self.state = 4
                else:
                    self.invalid_symbol()
            elif self.state == 2:  # Symbol
                self.add_token(
                    self.input_string[self.position : self.position + 1], "sym"
                )
                self.position += 1
                self.state = 1
            elif self.state == 3:  # Number
                while (
                    self.position < len(self.input_string)
                    and self.input_string[self.position].isdigit()
                ):
                    self.position += 1
                self.add_token(self.input_string[self.position :], "num")
                self.state = 1
            elif self.state == 4:  # Identifier
                while self.position < len(self.input_string) and (
                    self.input_string[self.position].isalpha()
                    or self.input_string[self.position].isdigit()
                ):
                    self.position += 1
                identifier = self.input_string[self.position :]
                if identifier in self.keywords:
                    self.add_token(identifier, "kw")
                else:
                    self.add_token(identifier, "id")
                self.state = 1

    def add_token(self, value, category):
        token = Token(value, category)
        self.token_list.append(token)

    def invalid_symbol(self):
        # print("Symbol outside the grammar! Lexical analysis not OK!")
        raise SystemExit

    def get_tokens(self):
        return self.token_list

    def test_chain(self, input_string):
        self.input_string = input_string
        self.position = 0
        self.token_list = []
        # return all(token.category != "out" for token in self.token_list)
        try:
            self.analyze()
            return True
        except SystemExit:
            return False


# chains = [
#     "(A12345+(a1+22)*42)",
#     "(B4567-35*(b2/2))",
#     "(CDE*3+(fgh/5))",
#     "(123+456)",
#     "(invalid@chain)",
# ]

# for chain in chains:
#     analyzer = LexicalAnalyzer(chain)
#     is_valid = analyzer.test_chain(chain)
#     if is_valid:
#         print(f'Chain "{chain}" ==> VALID.')
#     else:
#         print(f'Chain "{chain}" ==> INVALID.')
