from Lexer import tableOfSymb


class Semantic:
    def __init__(self, symbols_table):
        self.symbols_table = symbols_table
        self.variables = {}
        self.errors = []
        self.current_index = 1  # To keep track of position in the symbols table

    def analyze(self):
        for entry in self.symbols_table:
            line, lexeme, token_type, additional = entry
            self.current_index = self.symbols_table.index(entry)  # Set index for current entry

            if token_type == "id":
                if lexeme not in self.variables:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before declaration.")
                elif not self.variables[lexeme]["initialized"]:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before initialization.")
            elif token_type == "keyword":
                if lexeme == "val" or lexeme == "var":
                    self.handle_declaration(line, lexeme)
                elif lexeme == "if" or lexeme == "while":
                    self.handle_control_structure(line, lexeme)
            elif token_type == "assign_op":
                self.handle_assignment(line, lexeme)
            elif token_type in ["add_op", "mult_op", "divide_op"]:
                self.handle_operation(line, lexeme)

        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print("Semantic analysis completed successfully.")

    def handle_declaration(self, line, decl_type):
        var_name = self.get_next_token("id")
        var_type = self.get_next_token("type")

        if var_name is None or var_type is None:
            self.errors.append(f"Error on line {line}: Declaration is incomplete.")
            return

        if var_name in self.variables:
            self.errors.append(f"Error on line {line}: Variable '{var_name}' redeclared.")
        else:
            self.variables[var_name] = {
                "type": var_type,
                "initialized": decl_type == "val",
                "immutable": decl_type == "val"
            }

    def handle_assignment(self, line, lexeme):
        # Проверяем, существует ли переменная в словаре
        if lexeme not in self.variables:
            self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before declaration.")
            return

        # Проверяем, была ли переменная инициализирована
        if not self.variables[lexeme]["initialized"]:
            self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before initialization.")
            return

        # Дальше идет код для обработки присвоения значения переменной
        expr_type = self.evaluate_expression()  # Подсчет типа выражения
        if self.variables[lexeme]["immutable"]:
            self.errors.append(f"Error on line {line}: Cannot assign to immutable variable '{lexeme}'.")
        elif self.variables[lexeme]["type"] != expr_type:
            self.errors.append(f"Error on line {line}: Type mismatch in assignment to '{lexeme}'.")

        self.variables[lexeme]["initialized"] = True  # Помечаем как инициализированную

    def handle_operation(self, line, operator):
        left_operand_type = self.get_operand_type()
        right_operand_type = self.get_operand_type()

        if left_operand_type != right_operand_type:
            self.errors.append(f"Error on line {line}: Type mismatch in operation '{operator}'.")

        if operator == "/" and right_operand_type == "int" and self.get_operand_value() == 0:
            self.errors.append(f"Error on line {line}: Division by zero.")

    def handle_control_structure(self, line, structure_type):
        condition_type = self.evaluate_expression()
        if condition_type != "boolean":
            self.errors.append(f"Error on line {line}: Condition in '{structure_type}' should be boolean.")

    def get_next_token(self, expected=None):
        """Retrieve the next token based on expected type."""
        self.current_index += 1
        if self.current_index < len(self.symbols_table):
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if expected and token_type != expected:
                self.errors.append(f"Error on line {line}: Expected {expected} but found {token_type}.")
            return lexeme
        return None

    def get_previous_token(self, expected=None):
        """Retrieve the previous token based on expected type."""
        if self.current_index > 0:
            self.current_index -= 1
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if expected and token_type != expected:
                self.errors.append(f"Error on line {line}: Expected {expected} but found {token_type}.")
            return lexeme
        return None

    def evaluate_expression(self):
        expr_type = None
        expr_start = self.current_index
        while self.current_index < len(self.symbols_table):
            _, lexeme, token_type, additional = self.symbols_table[self.current_index]

            if token_type == "comp_op":  # Проверка на операцию сравнения
                expr_type = "boolean"
                break

            if token_type == "type":
                expr_type = lexeme

            self.current_index += 1
        self.current_index = expr_start  # Сброс индекса
        return expr_type or "unknown"

    def get_operand_type(self):
        """Retrieve operand type for binary operation."""
        operand = self.get_next_token()
        if operand in self.variables:
            return self.variables[operand]["type"]
        return "unknown"

    def get_operand_value(self):
        """Retrieve operand value, primarily for division check."""
        operand = self.get_next_token()
        if operand.isdigit():
            return int(operand)
        elif operand in self.variables:
            return self.variables[operand].get("value", None)
        return None


analyzer = Semantic(list(tableOfSymb.values()))
analyzer.analyze()
