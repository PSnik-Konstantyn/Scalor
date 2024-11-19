from Lexer import tableOfSymb


class SemanticError(Exception):
    """Клас для обробки семантичних помилок."""
    pass


class Variable:
    """Клас для представлення змінної."""
    def __init__(self, name, var_type, is_constant):
        self.name = name
        self.type = var_type
        self.is_constant = is_constant
        self.value = None  # Значення змінної


class SymbolTable:
    """Клас для зберігання таблиці символів."""
    def __init__(self):
        self.variables = {}

    def declare(self, name, var_type, is_constant=False):
        if name in self.variables:
            raise SemanticError(f"Повторне оголошення змінної '{name}'.")
        self.variables[name] = Variable(name, var_type, is_constant)

    def assign(self, name, value, value_type):
        if name not in self.variables:
            raise SemanticError(f"Змінна '{name}' не оголошена.")
        variable = self.variables[name]
        if variable.is_constant:
            raise SemanticError(f"Змінну '{name}' не можна змінювати (val).")
        if variable.type != value_type:
            raise SemanticError(f"Тип змінної '{name}' не збігається з типом виразу.")
        variable.value = value

    def get(self, name):
        if name not in self.variables:
            raise SemanticError(f"Змінна '{name}' не оголошена.")
        return self.variables[name]


class SemanticAnalyzer:
    """Семантичний аналізатор."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = SymbolTable()

    def analyze(self):
        current_line = 0

        for token in tableOfSymb.values():
            line, value, token_type, ref_id = token

            if line != current_line:
                current_line = line
                print(f"Обробка рядка {line}: {value}")

            # Обробка ключових слів
            if token_type == 'keyword':
                if value == 'var':
                    self.process_variable_declaration(line)
                elif value == 'val':
                    self.process_constant_declaration(line)
                else:
                    print(f"Пропускається ключове слово: {value}")

    def process_variable_declaration(self, line):
        """Обробляє оголошення змінних."""
        print(f"Оголошення змінної на рядку {line}.")

    def process_constant_declaration(self, line):
        """Обробляє оголошення констант."""


        print(f"Оголошення константи на рядку {line}.")
        # Логіка обробки для 'val' буде схожа на 'var'

    def assign_value(self, name, value, value_type, line):
        """Обробляє присвоєння значення змінній."""
        try:
            self.symbol_table.assign(name, value, value_type)
            print(f"Успішне присвоєння змінній '{name}' значення '{value}' на рядку {line}.")
        except SemanticError as e:
            print(f"Помилка на рядку {line}: {e}")

    def process_assignment(self, line, tokens):
        """Обробляє операцію присвоєння."""
        print(f"Обробка присвоєння на рядку {line}.")
        # Логіка для обробки присвоєння (шукає id, значення, тип)

    def process_operation(self, operator, left_operand, right_operand, line):
        """Перевіряє семантику операції."""
        print(f"Перевірка операції '{operator}' між {left_operand} і {right_operand} на рядку {line}.")
        # Логіка перевірки операції, типів операндів тощо

    def check_division_by_zero(self, right_value, line):
        """Перевіряє ділення на нуль."""
        if right_value == 0:
            raise SemanticError(f"Ділення на нуль на рядку {line}.")

    def execute_program(self):
        """Виконує аналіз на основі всіх токенів."""
        for token in self.tokens:
            line, value, token_type, ref_id = token
            if token_type == 'assign_op':
                print(f"Знайдено оператор присвоєння '=' на рядку {line}.")
                # Логіка присвоєння значення

            elif token_type in ['add_op', 'mult_op', 'comp_op', 'divide_op']:
                print(f"Знайдено оператор '{value}' на рядку {line}.")
                # Перевірка правильності типів у виразі

            elif token_type == 'type_op':
                print(f"Знайдено оператор типу '{value}' на рядку {line}.")
                # Перевірка типу змінної

            else:
                print(f"Інший токен: {value} ({token_type}) на рядку {line}.")


analyzer = SemanticAnalyzer(list(tableOfSymb))
analyzer.analyze()
