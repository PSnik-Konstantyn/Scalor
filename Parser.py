from Lexer import tableOfSymb


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        """Основний метод для запуску парсингу програми."""
        while self.pos < len(self.tokens):
            self.statement()

    def statement(self):
        """Метод для розбору окремих виразів або операторів."""
        if self.lookahead('keyword', 'val') or self.lookahead('keyword', 'var'):
            self.variable_declaration()
        elif self.lookahead('keyword', 'if'):
            self.if_statement()
        elif self.lookahead('keyword', 'while'):
            self.while_statement()
        elif self.lookahead('keyword', 'print'):
            self.print_statement()
        else:
            self.expression()

    def variable_declaration(self):
        """Парсер для оголошення змінних."""
        keyword = self.consume('keyword')  # Очікується 'val' або 'var'
        identifier = self.consume('id')
        self.consume('assign_op', '=')  # Очікується оператор '='
        expr = self.expression()
        print(f"Variable declaration: {keyword} {identifier} = {expr}")

    def expression(self):
        """Метод для розбору арифметичних або логічних виразів."""
        left = self.term()
        while self.lookahead('add_op'):
            operator = self.consume('add_op')
            right = self.term()
            left = (operator, left, right)
        return left

    def term(self):
        """Метод для обробки множення/ділення."""
        left = self.factor()
        while self.lookahead('mult_op'):
            operator = self.consume('mult_op')
            right = self.factor()
            left = (operator, left, right)
        return left

    def factor(self):
        """Метод для обробки окремих факторів (констант або ідентифікаторів)."""
        if self.lookahead('int'):
            return self.consume('int')
        elif self.lookahead('float'):
            return self.consume('float')
        elif self.lookahead('id'):
            return self.consume('id')
        elif self.lookahead('par_op', '('):
            self.consume('par_op', '(')
            expr = self.expression()
            self.consume('par_op', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")

    def if_statement(self):
        """Парсер для умовних операторів."""
        self.consume('keyword', 'if')
        self.consume('par_op', '(')
        condition = self.expression()
        self.consume('par_op', ')')
        self.consume('brace_op', '{')
        print(f"If statement with condition: {condition}")
        while not self.lookahead('brace_op', '}'):
            self.statement()
        self.consume('brace_op', '}')

    def while_statement(self):
        """Парсер для циклу."""
        self.consume('keyword', 'while')
        self.consume('par_op', '(')
        condition = self.expression()
        self.consume('par_op', ')')
        self.consume('brace_op', '{')
        print(f"While loop with condition: {condition}")
        while not self.lookahead('brace_op', '}'):
            self.statement()
        self.consume('brace_op', '}')

    def print_statement(self):
        """Парсер для оператора виводу."""
        self.consume('keyword', 'print')
        self.consume('par_op', '(')
        expr = self.expression()
        self.consume('par_op', ')')
        print(f"Print statement: {expr}")

    def lookahead(self, token_type, lexeme=None):
        """Перевірка наступного токена."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token[2] == token_type:
                if lexeme is None or token[1] == lexeme:
                    return True
        return False

    def consume(self, token_type, lexeme=None):
        """Отримує наступний токен, якщо він відповідає очікуваному типу/лексемі."""
        if self.lookahead(token_type, lexeme):
            current_token = self.tokens[self.pos]
            self.pos += 1
            return current_token[1]
        raise SyntaxError(f"Expected {token_type} '{lexeme}', got {self.peek()}")

    def peek(self):
        """Повертає поточний токен."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None


# Використання парсера з таблицею токенів з лексера
tokens = [(1, 'val', 'keyword'), (1, 'x', 'id'), (1, '=', 'assign_op'), (1, '10', 'int'), (2, 'print', 'keyword'), (2, '(', 'par_op'), (2, 'x', 'id'), (2, ')', 'par_op')]
parser = Parser(tableOfSymb)
parser.parse()