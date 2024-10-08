class ScalorInterpreterError(Exception):
    pass

class ScalorLexer:
    def __init__(self):
        self.tokens = []
        self.variables = {}
        self.current_line = 1

    def analyze(self, source_code):
        self.tokens = []
        current_token = ''
        for char in source_code:
            if char in ' \n\t':
                if current_token:
                    self.tokens.append(current_token)
                    current_token = ''
                if char == '\n':
                    self.current_line += 1
            elif char in '+-*/^=(){}:,"':
                if current_token:
                    self.tokens.append(current_token)
                    current_token = ''
                self.tokens.append(char)
            else:
                current_token += char

        if current_token:
            self.tokens.append(current_token)
        return self.tokens

    def parse(self):
        self.current_token_index = 0
        while self.current_token_index < len(self.tokens):
            token = self._get_next_token()
            if token == 'var':
                self._variable_declaration()
            elif token == 'val':
                self._constant_declaration()
            elif token == 'while':
                self._while_loop()
            elif token == 'if':
                self._if_statement()
            elif token == 'print':
                self._print_statement()
            else:
                raise ScalorInterpreterError(f"Unknown token {token} at line {self.current_line}")

    def _variable_declaration(self):
        var_name = self._get_next_token()
        self._expect(':')
        var_type = self._get_next_token()
        self._expect('=')
        var_value = self._evaluate_expression()

        self.variables[var_name] = var_value
        print(f"Variable {var_name} of type {var_type} initialized with {var_value}")

    def _constant_declaration(self):
        const_name = self._get_next_token()
        self._expect(':')
        const_type = self._get_next_token()
        self._expect('=')
        const_value = self._evaluate_expression()

        self.variables[const_name] = const_value
        print(f"Constant {const_name} of type {const_type} initialized with {const_value}")

    def _while_loop(self):
        condition = self._evaluate_expression()
        self._expect('{')
        while condition:
            self._parse_block()
            condition = self._evaluate_expression()

    def _if_statement(self):
        condition = self._evaluate_expression()
        self._expect('{')
        if condition:
            self._parse_block()
        else:
            while self._get_next_token() != '}':
                pass

    def _print_statement(self):
        value = self._get_next_token()
        if value in self.variables:
            print(self.variables[value])
        else:
            print(value)

    def _parse_block(self):
        while self._get_next_token() != '}':
            self.current_token_index -= 1
            self.parse()

    def _evaluate_expression(self):
        expression = self._get_next_token()

        if expression.startswith('"') and expression.endswith('"'):
            return expression.strip('"')

        expression = expression.replace('true', 'True').replace('false', 'False')

        try:
            return eval(expression)
        except Exception as e:
            raise ScalorInterpreterError(f"Error in expression: {expression}, {e}")

    def _get_next_token(self):
        token = self.tokens[self.current_token_index]
        self.current_token_index += 1
        return token

    def _expect(self, expected_token):
        token = self._get_next_token()
        if token != expected_token:
            raise ScalorInterpreterError(f"Expected '{expected_token}', but got '{token}'")



source_code = """
var x: Int = 10
val y2: Float = 5.5
var isActive: Boolean = true
val message: String = "Hello, Scalor!"

while (x > 0) {
    print(x)
    x = x - 1
}

if (isActive) {
    print(message)
} else {
    print("Not active")
}

val w: Float = 10*2/(12/5^2+1-9)
print(w)
"""

interpreter = ScalorLexer()
tokens = interpreter.analyze(source_code)
print("Tokens:", tokens)

interpreter.parse()