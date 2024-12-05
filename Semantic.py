from Lexer import tableOfSymb
from Parser import Parser


class Semantic:
    def __init__(self, symbols_table):
        self.symbols_table = symbols_table
        self.variables = {}
        self.errors = []
        self.current_index = -1

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
        self.get_next_token("par_op")
        var_name = self.get_next_token("id")

        if var_name is None:
            self.errors.append(f"Error on line {line}: Expected variable name after 'input'.")
            return

        if var_name not in self.variables:
            self.errors.append(f"Error on line {line}: Variable '{var_name}' used in 'input' before declaration.")
            return

        if self.variables[var_name]["immutable"]:
            self.errors.append(f"Error on line {line}: Cannot use immutable variable '{var_name}' in 'input'.")

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
                self.errors.append(f"Error on line {line}: Variable '{var_name}' is immutable and cannot be redeclared.")
            else:
                self.errors.append(f"Error on line {line}: Variable '{var_name}' redeclared.")
        else:
            expr_type = self.evaluate_expression()
            if expr_type != var_type:
                self.errors.append(
                    f"Error on line {line}: Type mismatch in initialization of '{var_name}'. Expected {var_type}, but got {expr_type}.")
                return
            self.variables[var_name] = {
                "type": var_type,
                "initialized": decl_type == "val" or decl_type == "var",
                "immutable": decl_type == "val"
            }


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

    def handle_control_structure(self, line, structure_type):
        condition_type = self.evaluate_expression()
        if condition_type != "Boolean":
            self.errors.append(f"Error on line {line}: Condition in '{structure_type}' should be boolean.")

    def get_next_token(self, expected=None):
        self.current_index += 1
        if self.current_index < len(self.symbols_table):
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if expected and token_type != expected:
                return "undefined_token"
            return lexeme if token_type == expected else "undefined_token"
        return "undefined_token"

    def get_previous_token(self, expected=None):
        if self.current_index > 0:
            self.current_index -= 1
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if expected and token_type != expected:
                return "undefined_token"
            return lexeme if token_type == expected else "undefined_token"
        return "undefined_token"

    def get_operand_type(self):
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

        # Перевірка на типи Int і Float
        if (left_operand_type == "Int" and right_operand_type == "Float") or \
                (left_operand_type == "Float" and right_operand_type == "Int"):
            return "Float"  # Результат операції Int + Float або Float + Int - це Float

        # Перевірка на невідповідність типів, якщо вони не включають приведення Int + Float
        if left_operand_type != right_operand_type and operator not in ["+"]:
            self.errors.append(
                f"Error on line {line}: Type mismatch in operation '{operator}' between {left_operand_type} and {right_operand_type}."
            )
            return "Mismatched Types"

        if operator == "/":
            if self.get_operand_value() == 0:
                self.errors.append(f"Error on line {line}: Division by zero.")
            if left_operand_type == "Int":
                return "Int"
            elif left_operand_type == "Float":
                return "Float"

        if operator == "+":
            if "String" in [left_operand_type, right_operand_type]:
                return "String"
            return left_operand_type

        return left_operand_type

    def evaluate_expression(self):
        expr_type = None
        found_operator = False

        current_line, _, _, _ = self.symbols_table[self.current_index]

        while self.current_index < len(self.symbols_table):
            line_number, lexeme, token_type, _  = self.symbols_table[self.current_index]

            if line_number != current_line:
                break

          #  print(f'{line_number} _____ {lexeme}')

            if lexeme in ["false", "true"]:
                expr_type = "Boolean"
                break

            if token_type == "comp_op" or lexeme in ["<=", ">=", "!=", "=="]:
                found_operator = True
                expr_type = "Boolean"
                break

            if token_type == "int" or lexeme.isdigit():
                if expr_type is None or expr_type == "Int":
                    expr_type = "Int"
                elif expr_type == "Float":
                    expr_type = "Float"
                else:
                    expr_type = "Mismatched Types"
            elif token_type == "float" or self.is_float_literal(lexeme):
                if expr_type is None or expr_type in ["Int", "Float"]:
                    expr_type = "Float"
                else:
                    expr_type = "Mismatched Types"

            elif token_type == "string":
                if expr_type is None:
                    expr_type = "String"
                else:
                    expr_type = "String"

            elif token_type == "id" and lexeme in self.variables:
                var_type = self.variables[lexeme]["type"]
                if expr_type is None:
                    expr_type = var_type
                elif expr_type != var_type:
                    if expr_type == "Float" and var_type == "Int":
                        expr_type = "Float"
                    else :
                        expr_type = "Mismatched Types"

            if token_type in ["add_op", "mult_op", "divide_op", "comp_op"] or lexeme in ["<=", ">=", "!=", "=="]:
                found_operator = True

            self.current_index += 1

        return expr_type if found_operator or expr_type else "unknown"

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

if result:
    print('\n---------------------\n')
    analyzer = Semantic(list(tableOfSymb.values()))
    analyzer.analyze()
else:
    print("Semantic analysis aborted due to syntax errors.")