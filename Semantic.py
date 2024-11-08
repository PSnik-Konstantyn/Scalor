from Lexer import tableOfSymb

class Semantic:
    def __init__(self, symbols_table):
        self.symbols_table = symbols_table
        self.variables = {}
        self.errors = []
        self.current_index = 1

    def analyze(self):
        for entry in self.symbols_table:
            line, lexeme, token_type, additional = entry
            self.current_index = self.symbols_table.index(entry)

            if token_type == "id":
                if lexeme not in self.variables:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before declaration.")
                elif not self.variables[lexeme]["initialized"]:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before initialization.")
            elif token_type == "keyword":
                if lexeme in ["val", "var"]:
                    self.handle_declaration(line, lexeme)
                elif lexeme in ["if", "while"]:
                    self.handle_control_structure(line, lexeme)
            elif token_type == "assign_op" and lexeme == ':=':
                self.handle_assignment(line)
            elif token_type in ["add_op", "mult_op", "divide_op", "comp_op"]:
                self.handle_operation(line, lexeme)

        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print("Semantic analysis completed successfully.")

    def handle_declaration(self, line, decl_type):
        var_name = self.get_next_token("id")
        self.get_next_token("type_op")
        var_type = self.get_next_token("type")

        if var_name is None or var_type is None:
            self.errors.append(f"Error on line {line}: Incomplete declaration.")
            return

        if var_name in self.variables:
            self.errors.append(f"Error on line {line}: Variable '{var_name}' redeclared.")
        else:
            self.variables[var_name] = {
                "type": var_type,
                "initialized": decl_type == "val" or decl_type == "var",
                "immutable": decl_type == "val"
            }

    def handle_assignment(self, line):
        var_name = self.get_previous_token("id")

        if var_name not in self.variables:
            self.errors.append(f"Error on line {line}: Variable '{var_name}' used before declaration.")
            return

        if self.variables[var_name]["immutable"]:
            self.errors.append(f"Error on line {line}: Cannot assign to immutable variable '{var_name}'.")
            return

        expr_type = self.evaluate_expression()

        if self.variables[var_name]["type"] != expr_type:
            self.errors.append(f"Error on line {line}: Type mismatch in assignment to '{var_name}'.")

        self.variables[var_name]["initialized"] = True

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
        self.current_index += 1
        if self.current_index < len(self.symbols_table):
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if expected and token_type != expected:
                self.errors.append(f"Error on line {line}: Expected {expected} but found {token_type}.")
            return lexeme
        return None

    def get_previous_token(self, expected=None):
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

            if token_type == "comp_op":
                expr_type = "boolean"
                break

            if token_type == "type":
                expr_type = lexeme

            self.current_index += 1
        self.current_index = expr_start
        return expr_type or "unknown"

    def get_operand_type(self):
        operand = self.get_next_token()
        if operand in self.variables:
            return self.variables[operand]["type"]
        return "unknown"

    def get_operand_value(self):
        operand = self.get_next_token()
        if operand.isdigit():
            return int(operand)
        elif operand in self.variables:
            return self.variables[operand].get("value", None)
        return None

# Example usage
analyzer = Semantic(list(tableOfSymb.values()))
analyzer.analyze()
