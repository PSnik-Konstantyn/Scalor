from Lexer import tableOfSymb
from Parser import Parser
from Postfix import PostfixGenerator


class Semantic:
    def __init__(self, symbols_table):
        self.symbols_table = symbols_table
        self.variables = {}
        self.errors = []
        self.current_index = -1
        self.generator = PostfixGenerator()

    def analyze(self):
        for entry in self.symbols_table:
            line, lexeme, token_type, additional = entry
            self.current_index = self.symbols_table.index(entry)

            if token_type == "id":
                if lexeme in ["true", "false"]:
                    continue
                if lexeme not in self.variables:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before declaration.")
                elif not self.variables[lexeme]["initialized"]:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before initialization.")
            elif token_type == "keyword":
                if lexeme in ["val", "var"]:
                    self.handle_declaration(line, lexeme)
                elif lexeme in ["if", "while"]:
                    self.handle_control_structure(line, lexeme)
                elif lexeme == "input":
                    self.handle_input(line)
                elif lexeme == "print":
                    self.handle_print(line)
            elif token_type == "assign_op" and lexeme == '=':
                self.handle_assignment(line)
            elif token_type in ["add_op", "mult_op", "divide_op", "comp_op"]:
                self.handle_operation(line, lexeme)

        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print("Semantic analysis completed successfully.")

    def handle_input(self, line):
        par_open = self.get_next_token("par_op")
        if par_open != "(":
            self.errors.append(f"Error on line {line}: Expected '(' after 'input'.")
            return

        var_name = self.get_next_token("id")
        if var_name is None or var_name == "undefined_token":
            self.errors.append(f"Error on line {line}: Expected variable name after 'input'.")
            return

        if var_name not in self.variables:
            self.errors.append(f"Error on line {line}: Variable '{var_name}' used in 'input' before declaration.")
            return

        if self.variables[var_name]["immutable"]:
            self.errors.append(f"Error on line {line}: Cannot use immutable variable '{var_name}' in 'input'.")
            return

        par_close = self.get_next_token("par_op")
        if par_close != ")":
            self.errors.append(f"Error on line {line}: Expected ')' after variable name in 'input'.")
            return

        self.generator.emit("input", var_name)

    def handle_print(self, line):
        self.get_next_token("par_op")
        value = self.get_next_token()

        if value is None or value == "undefined_token":
            self.errors.append(f"Помилка на лінії {line}: Очікувалось ім'я змінної або константа для 'print'.")
            return

        if value.isdigit():
            self.generator.emit("print", value)
        elif self.is_float_literal(value):
            self.generator.emit("print", value)
        elif value in ["true", "false"]:
            self.generator.emit("print", value)
        elif value in self.variables:
            self.generator.emit("print", value)
        else:
            self.generator.emit("print", value)

        self.get_next_token("par_op")

    def handle_declaration(self, line, decl_type):
        var_name = self.get_next_token("id")
        self.get_next_token("type_op")
        var_type = self.get_next_token("type")

        if var_name is None or var_type is None:
            self.errors.append(f"Error on line {line}: Incomplete declaration.")
            return

        if var_name in self.variables:
            if self.variables[var_name]["immutable"]:
                self.errors.append(
                    f"Error on line {line}: Variable '{var_name}' is immutable and cannot be redeclared.")
            else:
                self.errors.append(f"Error on line {line}: Variable '{var_name}' redeclared.")
        else:
            # Додаємо змінну до таблиці змінних
            self.variables[var_name] = {
                "type": var_type,
                "initialized": True,  # Завжди ініціалізована
                "immutable": decl_type == "val"
            }
            self.generator.tableOfVar[var_name] = (len(self.generator.tableOfVar) + 1, var_type)

            # Генерація коду для ініціалізації
            expr_type = self.evaluate_expression()  # Обчислення типу виразу для ініціалізації
            if expr_type != "unknown" and expr_type != var_type:
                self.errors.append(
                    f"Error on line {line}: Type mismatch in initialization of '{var_name}'. Expected {var_type}, but got {expr_type}.")
                return

            self.generator.emit(var_name, "l-val")  # Ліва частина присвоєння
            self.generator.emit("=", "assign_op")  # Операція присвоєння

    def handle_assignment(self, line):
        var_name = self.get_previous_token("id")

        if var_name is None or var_name == "undefined_token":
            return

        if var_name not in self.variables:
            self.errors.append(f"Error on line {line}: Variable '{var_name}' used before declaration.")
            return

        if self.variables[var_name]["immutable"]:
            self.errors.append(f"Error on line {line}: Cannot assign to immutable variable '{var_name}'.")
            return

        expr_type = self.evaluate_expression()
        if expr_type == "Mismatched Types":
            self.errors.append(f"Error on line {line}: Type mismatch in assignment expression.")
        elif self.variables[var_name]["type"] != expr_type:
            self.errors.append(
                f"Error on line {line}: Type mismatch in assignment to '{var_name}'. Expected {self.variables[var_name]['type']}, but got {expr_type}."
            )

        self.variables[var_name]["initialized"] = True

        self.generator.emit(var_name, "l-val")
        self.generator.emit("=", "assign_op")

    def handle_control_structure(self, line, structure_type):
        condition_type = self.evaluate_expression()
        if condition_type != "Boolean":
            self.errors.append(f"Error on line {line}: Condition in '{structure_type}' should be boolean.")

    def get_next_token(self, expected=None):
        self.current_index += 1
        if self.current_index < len(self.symbols_table):
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if expected is None:
                return lexeme
            if expected and token_type != expected:
                return "undefined_token"
            return lexeme if token_type == expected else "undefined_token"
        return "undefined_token"

    def save_postfix_code(self, file_name):
        fname = file_name + ".postfix"
        with open(fname, 'w') as f:
            f.write(".target: Postfix Machine\n.version: 0.2\n")
            f.write("\n.vars(\n")
            for var, var_details in self.variables.items():
                f.write(f"   {var:<6}{var_details['type']:<10}\n")
            f.write(")\n")
            f.write("\n.constants(\n")
            for const, const_type in self.generator.tableOfConst.items():
                f.write(f"   {const:<6}{const_type:<10}\n")
            f.write(")\n")
            f.write("\n.code(\n")
            for opcode, operand in self.generator.postfixCodeTSM:
                f.write(f"   {opcode:<6}{operand or ''}\n")
            f.write(")\n")
        print(f"Postfix code saved to {fname}")

    def get_previous_token(self, expected=None):
        if self.current_index > 0:
            self.current_index -= 1
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if expected and token_type != expected:
                return "undefined_token"
            return lexeme if token_type == expected else "undefined_token"
        return "undefined_token"

    def get_operand_type(self):
        self.current_index -= 1
        operand = self.get_next_token()

        if operand.isdigit():
            return "Int"
        elif self.is_float_literal(operand):
            return "Float"
        elif operand.startswith('"') and operand.endswith('"'):
            return "String"

        if operand in self.variables:
            return self.variables[operand]["type"]

        if operand in ["true", "false"]:
            return "Boolean"

        return "unknown"

    def is_float_literal(self, operand):
        try:
            float(operand)
            return True
        except ValueError:
            return False

    def handle_operation(self, line, operator):
        left_operand_type = self.get_operand_type()
        right_operand_type = self.get_operand_type()

        if left_operand_type == "Boolean" and right_operand_type == "Boolean" and operator in ["==", "!=", "&&", "||"]:
            return "Boolean"

        if left_operand_type in ["Int", "Float"] and right_operand_type in ["Int", "Float"]:
            if operator == "/":
                if self.get_operand_value() == 0:
                    self.errors.append(f"Error on line {line}: Division by zero.")
                return "Float" if left_operand_type == "Float" or right_operand_type == "Float" else "Int"

            if operator in ["+", "-", "*", "/"]:
                return "Float" if "Float" in [left_operand_type, right_operand_type] else "Int"

        if left_operand_type != right_operand_type and operator not in ["+"]:
            self.errors.append(
                f"Error on line {line}: Type mismatch in operation '{operator}' between {left_operand_type} and {right_operand_type}."
            )
            return "Mismatched Types"

        return left_operand_type

    def evaluate_expression(self):
        expr_type = None
        found_operator = False

        current_line, _, _, _ = self.symbols_table[self.current_index]

        while self.current_index < len(self.symbols_table):
            line_number, lexeme, token_type, _ = self.symbols_table[self.current_index]

            # Перевірка переходу на новий рядок
            if line_number != current_line:
                break

            # Обробка констант (Boolean)
            if lexeme in ["false", "true"]:
                expr_type = self.update_type(expr_type, "Boolean")
                self.current_index += 1
                continue

            # Обробка операторів порівняння
            if token_type == "comp_op" or lexeme in ["<=", ">=", "!=", "=="]:
                found_operator = True
                expr_type = "Boolean"
                self.current_index += 1
                continue

            # Обробка чисел (Int, Float)
            if token_type == "int" or lexeme.isdigit():
                expr_type = self.update_type(expr_type, "Int")
            elif token_type == "float" or self.is_float_literal(lexeme):
                expr_type = self.update_type(expr_type, "Float")

            # Обробка рядків
            elif token_type == "string":
                expr_type = self.update_type(expr_type, "String")

            # Обробка змінних
            elif token_type == "id" and lexeme in self.variables:
                var_type = self.variables[lexeme]["type"]
                expr_type = self.update_type(expr_type, var_type)

            # Обробка операторів
            if token_type in ["add_op", "mult_op", "divide_op", "comp_op"] or lexeme in ["<=", ">=", "!=", "=="]:
                found_operator = True

            self.current_index += 1

        return expr_type if found_operator or expr_type else "unknown"

    def update_type(self, current_type, new_type):
        if current_type is None:
            return new_type
        if current_type == new_type:
            return current_type
        if current_type == "Float" and new_type == "Int":
            return "Float"
        if current_type == "Int" and new_type == "Float":
            return "Float"
        if current_type == "Boolean" or new_type == "Boolean":
            if current_type in ["Int", "Float", "String"]:
                return "Mismatched Types"
            return "Boolean"
        return "Mismatched Types"

    def get_operand_value(self):
        _, operand, _, _ = self.symbols_table[self.current_index-1]
        # -1
        if operand and operand.isdigit():
            return int(operand)
        elif operand in self.variables:
            return self.variables[operand].get("value", None)
        return None

parser = Parser(tableOfSymb)
result = parser.parse()


def save_postfix_code(file_name, generator, variables):
    fname = f"{file_name}.postfix"  # Це дозволить передавати правильний тип
    with open(fname, 'w') as f:
        f.write(".target: Postfix Machine\n.version: 0.2\n")
        f.write("\n.vars(\n")
        for var, var_details in variables.items():  # Використовуємо 'variables' замість 'self.variables'
            f.write(f"   {var:<6}{var_details['type']:<10}\n")
        f.write(")\n")
        f.write("\n.constants(\n")
        for const, const_type in generator.tableOfConst.items():
            f.write(f"   {const:<6}{const_type:<10}\n")
        f.write(")\n")
        f.write("\n.code(\n")
        for opcode, operand in generator.postfixCodeTSM:
            # Ensure operand is not None before formatting
            if operand is not None:
                f.write(f"   {opcode:<6}{operand}\n")
            else:
                f.write(f"   {opcode:<6}\n")  # Якщо operand = None, вивести лише opcode
        # Handle case where operand is None
        f.write(")\n")
    print(f"Postfix code saved to {fname}")



if result:
    print('\n---------------------\n')
    analyzer = Semantic(list(tableOfSymb.values()))
    analyzer.analyze()
    save_postfix_code("output", analyzer.generator, analyzer.variables)


else:
    print("Semantic analysis aborted due to syntax errors.")