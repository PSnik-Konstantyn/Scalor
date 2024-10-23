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
        """Метод для обработки арифметических или логических выражений."""
        left = self.term()

        # Добавляем поддержку операторов сравнения и сложения
        while self.lookahead('comp_op') or self.lookahead_double_op() or self.lookahead('add_op'):
            if self.lookahead_double_op():
                operator = self.consume('comp_op')  # Двойные операторы сравнения (<=, >=, !=, ==)
            elif self.lookahead('comp_op'):
                operator = self.consume('comp_op')  # Операторы сравнения (<, >)
            elif self.lookahead('add_op'):
                operator = self.consume('add_op')  # Операторы сложения (+, -)
            else:
                raise SyntaxError(f"Unexpected token in expression: {self.peek()}")

            right = self.term()
            left = (left, operator, right)

        return left



    def term(self):
        """Метод для обробки множення/ділення."""
        left = self.factor()
        while self.lookahead('mult_op') or self.lookahead('divide_op'):  # Додано підтримку divide_op
            operator = self.consume('mult_op') if self.lookahead('mult_op') else self.consume(
                'divide_op')  # Обробляємо і '*' і '/'
            right = self.factor()
            left = (left, operator, right)
        return left

    def factor(self):
        """Method for handling factors (constants, identifiers, or parenthesized expressions)."""
        left = self.primary()
        while self.lookahead('power_op'):  # Handle the power operator '^'
            operator = self.consume('power_op')
            right = self.primary()  # Right side of the power operation
            left = (left, operator, right)
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
        """Parser for if statements."""
        self.consume('keyword', 'if')
        self.consume('par_op', '(')
        condition = self.expression()  # Condition in if
        self.consume('par_op', ')')
        self.consume('brace_op', '{')
        print(f"If statement with condition: {condition}")

        # Process the body of if with one level of indentation
        while not self.lookahead('brace_op', '}'):
            print("\t", end="")  # One tab for indentation
            self.statement()
        self.consume('brace_op', '}')

        # Check for the presence of else
        if self.lookahead('keyword', 'else'):
            self.consume('keyword', 'else')  # Consume 'else'
            self.consume('brace_op', '{')  # Expect opening brace
            print("\t\tElse statement:")  # Two tabs for else

            # Process the body of else with two levels of indentation
            while not self.lookahead('brace_op', '}'):
                print("\t\t", end="")  # Two tabs for indentation
                self.statement()
            self.consume('brace_op', '}')  # Closing brace

    def while_statement(self):
        """Parser for while loops."""
        self.consume('keyword', 'while')
        self.consume('par_op', '(')
        condition = self.expression()
        self.consume('par_op', ')')
        self.consume('brace_op', '{')
        print(f"While loop with condition: {condition}")

        # Process the body of the while loop with one level of indentation
        while not self.lookahead('brace_op', '}'):
            print("\t", end="")  # One tab for indentation
            self.statement()  # Parse and execute statements inside the loop

        self.consume('brace_op', '}')

    def print_statement(self):
        # Expect 'print' keyword (already found in statement)
        self.consume('keyword', 'print')

        # Expect opening parenthesis '('
        self.consume('par_op', '(')

        # Parse the argument for print (a variable or string in your case)
        expr = self.expression()

        # Expect closing parenthesis ')'
        self.consume('par_op', ')')
        print(f"Print statement recognized with argument: {expr}")

    def consume(self, token_type, lexeme=None):
        """Получает следующий токен, если он соответствует ожидаемому типу/лексеме."""
        if self.lookahead_double_op():
            # Составной оператор (например, <=, >=)
            current_token = self.tokens[self.pos][1] + self.tokens[self.pos + 1][1]  # Склеиваем составной оператор
            self.pos += 2  # Увеличиваем позицию на 2, так как два токена были объединены
            return current_token

        if self.lookahead(token_type, lexeme):
            current_token = self.tokens[self.pos]
            self.pos += 1  # Увеличиваем позицию после успешного потребления токена
            return current_token[1]

        raise SyntaxError(f"Expected {token_type} '{lexeme}', got {self.peek()}")

    def lookahead(self, token_type, lexeme=None):
        """Перевірка наступного токена."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token[2] == token_type:
                if lexeme is None or token[1] == lexeme:
                    return True
        return False

    def lookahead_double_op(self):
        """Проверяет, если текущий оператор и следующий составляют двойной оператор сравнения."""
        if self.pos + 1 < len(self.tokens):
            current_token = self.tokens[self.pos]
            next_token = self.tokens[self.pos + 1]

            # Проверка на составные операторы сравнения: <=, >=, !=, ==
            if current_token[1] in ['<', '>', '!', '='] and next_token[1] == '=':
                return True
        return False


    def peek(self):
        """Возвращает текущий токен."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None


# Використання парсера з таблицею токенів з лексера
tokens = [(1, 'val', 'keyword'), (1, 'x', 'id'), (1, '=', 'assign_op'), (1, '10', 'int'), (2, 'print', 'keyword'), (2, '(', 'par_op'), (2, 'x', 'id'), (2, ')', 'par_op')]
parser = Parser(tableOfSymb)
parser.parse()

