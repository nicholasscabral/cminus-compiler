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


class SyntaxAnalyzer:
    def __init__(self, token_list):
        self.token_list = token_list
        self.current_token = None
        self.token_index = 0

    def match(self, expected_category):
        if self.current_token.category == expected_category:
            self.token_index += 1
            if self.token_index < len(self.token_list):
                self.current_token = self.token_list[self.token_index]
            else:
                self.current_token = None
        else:
            print(
                f"Syntax error: Expected {expected_category}, got {self.current_token.category}"
            )
            raise SystemExit

    def program(self):
        self.declaration_list()

    def declaration_list(self):
        if self.current_token and self.current_token.category in ["kw", "id"]:
            self.declaration()
            self.declaration_list_prime()

    def declaration_list_prime(self):
        if self.current_token and self.current_token.category in ["kw", "id"]:
            self.declaration()
            self.declaration_list_prime()
        else:
            pass

    def declaration(self):
        if self.current_token.category == "kw" and self.current_token.value in [
            "int",
            "void",
        ]:
            self.match("kw")
            if self.current_token.category == "id":
                self.match("id")
                if (
                    self.current_token.category == "sym"
                    and self.current_token.value == "("
                ):
                    self.match("sym")
                    self.params()
                    if (
                        self.current_token.category == "sym"
                        and self.current_token.value == ")"
                    ):
                        self.match("sym")
                        self.compound_stmt()
                    else:
                        self.invalid_syntax()
                elif (
                    self.current_token.category == "sym"
                    and self.current_token.value == ";"
                ):
                    self.match("sym")
                else:
                    self.invalid_syntax()
            else:
                self.invalid_syntax()
        else:
            self.invalid_syntax()

    def params(self):
        if self.current_token.category == "kw" and self.current_token.value == "void":
            self.match("kw")
        elif self.current_token.category == "kw" and self.current_token.value == "int":
            self.match("kw")
            if self.current_token.category == "id":
                self.match("id")
                self.param_list()
            else:
                self.invalid_syntax()
        else:
            self.invalid_syntax()

    def param_list(self):
        if self.current_token.category == "sym" and self.current_token.value == ",":
            self.match("sym")
            if (
                self.current_token.category == "kw"
                and self.current_token.value == "int"
            ):
                self.match("kw")
                if self.current_token.category == "id":
                    self.match("id")
                    self.param_list()
                else:
                    self.invalid_syntax()
            else:
                self.invalid_syntax()
        else:
            pass

    def compound_stmt(self):
        if self.current_token.category == "sym" and self.current_token.value == "{":
            self.match("sym")
            self.local_declarations()
            self.statement_list()
            if self.current_token.category == "sym" and self.current_token.value == "}":
                self.match("sym")
            else:
                self.invalid_syntax()
        else:
            self.invalid_syntax()

    def local_declarations(self):
        if self.current_token and self.current_token.category in ["kw", "id"]:
            if (
                self.current_token.category == "kw"
                and self.current_token.value == "int"
            ):
                self.match("kw")
                if self.current_token.category == "id":
                    self.match("id")
                    self.local_declarations()
                else:
                    self.invalid_syntax()
            else:
                pass

    def statement_list(self):
        if self.current_token and self.current_token.category in ["kw", "id", "sym"]:
            self.statement()
            self.statement_list_prime()

    def statement_list_prime(self):
        if self.current_token and self.current_token.category in ["kw", "id", "sym"]:
            self.statement()
            self.statement_list_prime()
        else:
            pass

    def statement(self):
        if self.current_token.category == "sym" and self.current_token.value == ";":
            self.match("sym")
        elif self.current_token.category == "kw" and self.current_token.value == "if":
            self.match("kw")
            if self.current_token.category == "sym" and self.current_token.value == "(":
                self.match("sym")
                self.expression()
                if (
                    self.current_token.category == "sym"
                    and self.current_token.value == ")"
                ):
                    self.match("sym")
                    self.statement()
                    self.selection_stmt_prime()
                else:
                    self.invalid_syntax()
            else:
                self.invalid_syntax()
        elif (
            self.current_token.category == "kw" and self.current_token.value == "while"
        ):
            self.match("kw")
            if self.current_token.category == "sym" and self.current_token.value == "(":
                self.match("sym")
                self.expression()
                if (
                    self.current_token.category == "sym"
                    and self.current_token.value == ")"
                ):
                    self.match("sym")
                    self.statement()
                else:
                    self.invalid_syntax()
            else:
                self.invalid_syntax()
        else:
            self.expression_stmt()

    def selection_stmt_prime(self):
        if self.current_token.category == "kw" and self.current_token.value == "else":
            self.match("kw")
            self.statement()
        else:
            pass

    def expression_stmt(self):
        if self.current_token.category == "sym" and self.current_token.value == ";":
            self.match("sym")
        else:
            self.expression()
            if self.current_token.category == "sym" and self.current_token.value == ";":
                self.match("sym")
            else:
                self.invalid_syntax()

    def expression(self):
        self.var()
        if self.current_token.category == "sym" and self.current_token.value == "=":
            self.match("sym")
            self.expression()
        else:
            self.simple_expression()

    def var(self):
        if self.current_token.category == "id":
            self.match("id")
            self.var_prime()
        else:
            self.invalid_syntax()

    def var_prime(self):
        if self.current_token.category == "sym" and self.current_token.value == "[":
            self.match("sym")
            self.expression()
            if self.current_token.category == "sym" and self.current_token.value == "]":
                self.match("sym")
            else:
                self.invalid_syntax()
        else:
            pass

    def simple_expression(self):
        self.additive_expression()
        self.relop()
        self.additive_expression()

    def relop(self):
        if self.current_token.category == "sym" and self.current_token.value in [
            "<=",
            "<",
            ">",
            ">=",
            "==",
            "!=",
        ]:
            self.match("sym")
        else:
            self.invalid_syntax()

    def additive_expression(self):
        self.term()
        self.additive_expression_prime()

    def additive_expression_prime(self):
        if self.current_token.category == "sym" and self.current_token.value in [
            "+",
            "-",
        ]:
            self.match("sym")
            self.term()
            self.additive_expression_prime()
        else:
            pass

    def term(self):
        self.factor()
        self.term_prime()

    def term_prime(self):
        if self.current_token.category == "sym" and self.current_token.value in [
            "*",
            "/",
        ]:
            self.match("sym")
            self.factor()
            self.term_prime()
        else:
            pass

    def factor(self):
        if self.current_token.category == "sym" and self.current_token.value == "(":
            self.match("sym")
            self.expression()
            if self.current_token.category == "sym" and self.current_token.value == ")":
                self.match("sym")
            else:
                self.invalid_syntax()
        elif self.current_token.category == "id":
            self.match("id")
            self.factor_prime()
        elif self.current_token.category == "num":
            self.match("num")
        else:
            self.invalid_syntax()

    def factor_prime(self):
        if self.current_token.category == "sym" and self.current_token.value == "(":
            self.match("sym")
            self.args()
            if self.current_token.category == "sym" and self.current_token.value == ")":
                self.match("sym")
            else:
                self.invalid_syntax()
        elif self.current_token.category == "sym" and self.current_token.value == "[":
            self.match("sym")
            self.expression()
            if self.current_token.category == "sym" and self.current_token.value == "]":
                self.match("sym")
            else:
                self.invalid_syntax()
        else:
            pass

    def args(self):
        if self.current_token and self.current_token.category in [
            "kw",
            "id",
            "sym",
            "num",
        ]:
            self.expression()
            self.args_prime()

    def args_prime(self):
        if self.current_token.category == "sym" and self.current_token.value == ",":
            self.match("sym")
            self.expression()
            self.args_prime()
        else:
            pass

    def invalid_syntax(self, expected_category):
        print(
            f"Invalid syntax. Expected {expected_category} but got {self.current_token.value} ({self.current_token.category})."
        )
        raise SystemExit


# Example usage
input_string = "int main() { int x; x = 5; return x; }"
lexer = LexicalAnalyzer(input_string)
lexer.analyze()
tokens = lexer.get_tokens()

print("asdf")

syntax_analyzer = SyntaxAnalyzer(tokens)
try:
    syntax_analyzer.program()
    print("Syntax analysis successful.")
except SystemExit:
    print("Syntax analysis failed.")
