from Lexer import tableOfSymb


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 1

    def parse(self):
        """Основной метод для запуска парсинга программы."""
        while self.pos < len(self.tokens):
            self.statement()

    def statement(self):
        """Метод для разбора отдельных выражений или операторов."""
        if self.lookahead('keyword', 'val') or self.lookahead('keyword', 'var'):
            self.variable_declaration()
        elif self.lookahead('keyword', 'if'):
            self.if_statement()
        elif self.lookahead('keyword', 'while'):
            self.while_statement()
        elif self.lookahead('keyword', 'print'):
            self.print_statement()
        elif self.lookahead('id'):
            # Добавляем поддержку присвоения переменной
            self.assignment_statement()
        else:
            self.expression()

    def variable_declaration(self):
        keyword_token = self.consume('keyword')

        if keyword_token not in ['var', 'val']:
            raise SyntaxError(f"Expected 'var' or 'val', got {keyword_token[1]}")

        identifier = self.consume('id')  # Ожидается имя переменной
        self.consume('type_op', ':')  # Ожидается ':'
        var_type = self.consume('type')  # Ожидается тип (Int, Float и т.д.)

        # Если есть оператор присвоения, обрабатываем его
        if self.peek()[2] == 'assign_op':
            self.consume('assign_op', '=')  # Ожидается '='
            expr = self.expression()  # Получаем выражение или значение для присвоения

            # Выводим информацию об объявлении переменной
            print(f"Variable declaration: {keyword_token} {identifier} : {var_type} = {expr}")
        else:
            print(f"Variable declaration: {keyword_token} {identifier} : {var_type} (no assignment)")

    def assignment_statement(self):
        """Метод для разбора оператора присвоения."""
        identifier = self.consume('id')  # Ожидается имя переменной
        self.consume('assign_op', '=')  # Ожидается '='
        expr = self.expression()  # Получаем выражение или значение для присвоения
        print(f"Assignment: {identifier} = {expr}")

    def expression(self):
        """Метод для разбора арифметических или логических выражений."""
        left = self.term()
        while self.lookahead('add_op') or self.lookahead('comp_op'):  # Добавляем проверку сравнительных операторов
            operator = self.consume('add_op') if self.lookahead('add_op') else self.consume(
                'comp_op')  # Потребляем оператор
            right = self.term()
            left = (operator, left, right)
        return left

    def term(self):
        """Метод для обробки множення/ділення."""
        left = self.factor()
        while self.lookahead('mult_op') or self.lookahead('divide_op'):  # Додано підтримку divide_op
            operator = self.consume('mult_op') if self.lookahead('mult_op') else self.consume(
                'divide_op')  # Обробляємо і '*' і '/'
            right = self.factor()
            left = (operator, left, right)
        return left

    def factor(self):
        """Method for handling factors (constants, identifiers, or parenthesized expressions)."""
        left = self.primary()
        while self.lookahead('power_op'):  # Handle the power operator '^'
            operator = self.consume('power_op')
            right = self.primary()  # Right side of the power operation
            left = (operator, left, right)
        return left

    def primary(self):
        """Method for processing basic primary units such as integers, floats, ids, or parenthesized expressions."""
        if self.lookahead('int'):
            return self.consume('int')
        elif self.lookahead('float'):
            return self.consume('float')
        elif self.lookahead('id'):
            return self.consume('id')
        elif self.lookahead('keyword', 'true') or self.lookahead('keyword', 'false'):
            return self.consume('keyword')
        elif self.lookahead('string'):
            return self.consume('string')  # Handle string tokens
        elif self.lookahead('par_op', '('):
            self.consume('par_op', '(')
            expr = self.expression()
            self.consume('par_op', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")

    def if_statement(self):
        """Парсер для условных операторов."""
        self.consume('keyword', 'if')
        self.consume('par_op', '(')
        condition = self.expression()  # Условие в if
        self.consume('par_op', ')')
        self.consume('brace_op', '{')
        print(f"If statement with condition: {condition}")

        # Обрабатываем тело if
        while not self.lookahead('brace_op', '}'):
            self.statement()
        self.consume('brace_op', '}')

        # Проверяем наличие else
        if self.lookahead('keyword', 'else'):
            self.consume('keyword', 'else')  # Потребляем else
            self.consume('brace_op', '{')  # Ожидаем открывающую фигурную скобку
            print("Else statement:")

            # Обрабатываем тело else
            while not self.lookahead('brace_op', '}'):
                self.statement()
            self.consume('brace_op', '}')  # Закрывающая фигурная скобка

    def while_statement(self):
        """Парсер для цикла while."""
        self.consume('keyword', 'while')
        self.consume('par_op', '(')
        condition = self.expression()
        self.consume('par_op', ')')
        self.consume('brace_op', '{')
        print(f"While loop with condition: {condition}")

        while not self.lookahead('brace_op', '}'):
            print("-------")  # Печатаем разделитель
            self.statement()  # Парсим и выполняем оператор внутри цикла

        self.consume('brace_op', '}')

    def print_statement(self):
        # Oжидаем 'print' (уже должно быть найдено в statement)
        self.consume('keyword', 'print')

        # Ожидаем открывающую скобку '('
        print(f"Текущий токен перед открывающей скобкой: {self.peek()}")  # Отладка
        self.consume('par_op', '(')

        # Парсим аргумент для print (в твоем случае это переменная или строка)
        print(f"Токен внутри скобок: {self.peek()}")  # Отладка
        self.expression()  # Это твой метод для выражения

        # Ожидаем закрывающую скобку ')'
        print(f"Текущий токен перед закрывающей скобкой: {self.peek()}")  # Отладка
        self.consume('par_op', ')')

        print("Оператор print успешно распознан.")  # Успешное распознавание

    def lookahead(self, token_type, lexeme=None):
        """Проверка следующего токена."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token[2] == token_type:
                if lexeme is None or token[1] == lexeme:
                    return True
        return False

    def consume(self, token_type, lexeme=None):
        """Получение следующего токена, если он соответствует ожидаемому типу/лексеме."""
        if self.lookahead(token_type, lexeme):
            current_token = self.tokens[self.pos]
            self.pos += 1
            return current_token[1]
        raise SyntaxError(f"Expected {token_type} '{lexeme}', got {self.peek()}")

    def peek(self):
        """Возвращает текущий токен."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None


# Використання парсера з таблицею токенів з лексера
tokens = [(1, 'val', 'keyword'), (1, 'x', 'id'), (1, '=', 'assign_op'), (1, '10', 'int'), (2, 'print', 'keyword'), (2, '(', 'par_op'), (2, 'x', 'id'), (2, ')', 'par_op')]
parser = Parser(tableOfSymb)
parser.parse()