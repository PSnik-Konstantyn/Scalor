from Lexer import tableOfSymb
from Postfix import PostfixGenerator
from SaveCIL import saveCIL
from Semantic import Semantic


def find_next_if_or_else(start_index):

    for index in range(start_index, len(tableOfSymb) + 1):
        token = tableOfSymb.get(index)
        if token and token[1] in {"if", "else"}:
            return token[1], index
    return None


def has_else_block(start_index):
    next_token = find_next_if_or_else(start_index + 1)
    if next_token:
        token_type, token_index = next_token
        if token_type == "else":
            return True
        elif token_type == "if":
            return False
    return False


class Poliz:
    def __init__(self, symbols_table):
        self.symbols_table = symbols_table
        self.variables = {}
        self.errors = []
        self.current_index = -1
        self.generator = PostfixGenerator()

    def analyze(self):
        while self.current_index < len(self.symbols_table) - 1:
            self.current_index += 1
            entry = self.symbols_table[self.current_index]
            line, lexeme, token_type, additional = entry
            if token_type == "id":
                if lexeme in ["true", "false"]:
                    continue
                if lexeme not in self.variables:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before declaration.")
                elif not self.variables[lexeme]["initialized"]:
                    self.errors.append(f"Error on line {line}: Variable '{lexeme}' used before initialization.")
            elif token_type == "assign_op" and lexeme == '=':
                self.handle_assignment(line)
            elif token_type in ["add_op", "mult_op", "divide_op", "comp_op"]:
                self.handle_operation(line, lexeme)
            elif token_type == "keyword":
                if lexeme in ["val", "var"]:
                    self.handle_declaration(line, lexeme)
                elif lexeme == "input":
                    self.handle_input(line)
                elif lexeme == "print":
                    self.handle_print(line)
                elif lexeme in ["if", "while"]:
                    self.handle_control_structure(line, lexeme)

        if self.errors:
            for error in self.errors:
                print(error)

    def format_types(self):
        type_mapping = {
            "int": "Int",
            "float": "Float",
            "boolean": "Boolean"
        }

        self.generator.tableOfVar = {
            var: type_mapping.get(value[1].lower(), value[1])
            for var, value in self.generator.tableOfVar.items()
        }

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

        self.generator.emit(var_name, "l-val")
        self.generator.emit("IN", "input")

    def handle_print(self, line):
        self.get_next_token("par_op")
        value = self.get_next_token()

        if value is None or value == "undefined_token":
            self.errors.append(f"Помилка на лінії {line}: Очікувалось ім'я змінної або константа для 'print'.")
            return

        if value.isdigit():
            self.generator.emit(value, "Int")
        else:
            try:
                float(value)
                self.generator.emit(value, "Float")
            except ValueError:
                if value in ('true', 'false'):
                    self.generator.emit(value, "Boolean")
                elif value.startswith('"') and value.endswith('"'):
                    self.generator.emit(value, "String")
                else:
                    if value not in self.variables:
                        self.errors.append(
                            f"Error on line {line}: Variable '{value}' used in 'input' before declaration.")
                        return
                    self.generator.emit(value, "r-val")


        self.generator.emit("OUT", "print")

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
            self.variables[var_name] = {
                "type": var_type,
                "initialized": True,
                "immutable": decl_type == "val"
            }
            new_v = var_type.lower()
            self.generator.tableOfVar[var_name] = (len(self.generator.tableOfVar) + 1, new_v)

            self.generator.emit(var_name, "l-val")
            expr_type = self.evaluate_expression()
            if expr_type != "unknown" and expr_type != var_type:
                self.errors.append(
                    f"Error on line {line}: Type mismatch in initialization of '{var_name}'. Expected {var_type}, but got {expr_type}.")
                return


            self.generator.emit("=", "assign_op")
            self.current_index -= 1

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

        self.generator.emit(var_name, "l-val")

        self.get_next_token("assign_op")

        expr_type = self.evaluate_expression()
        if expr_type == "Mismatched Types":
            self.errors.append(f"Error on line {line}: Type mismatch in assignment expression.")
        elif self.variables[var_name]["type"] != expr_type:
            self.errors.append(
                f"Error on line {line}: Type mismatch in assignment to '{var_name}'. Expected {self.variables[var_name]['type']}, but got {expr_type}."
            )

        self.variables[var_name]["initialized"] = True
        self.generator.emit("=", "assign_op")
        self.current_index -= 1

    def handle_control_structure(self, line, structure_type):
        if structure_type == "if":
            condition_type = self.evaluate_expression()
            if condition_type != "Boolean":
                self.errors.append(f"Error on line {line}: Condition in 'if' should be boolean.")
                return
            next_if = self.generator.generate_label()
            leave = self.generator.generate_label()

            self.generator.emit(next_if, "label")
            self.generator.add_JF(next_if)

            self.process_block()
            self.generator.emit(leave, "label")
            self.generator.add_JMP(leave)

            if not has_else_block(self.current_index):
                self.generator.init_label(next_if)
            else:
                self.generator.init_label(next_if)

                self.current_index -= 1
                next_token = self.get_next_token()
                if next_token != "else":
                    self.errors.append(f"Error on line {line}: Expected 'else' after 'if' block.")
                    return

                brace_open = self.get_next_token("brace_op")
                if brace_open != "{":
                    self.errors.append(f"Error on line {line}: Expected '{{' to start 'else' block.")
                    return

                self.process_block()

            self.generator.init_label(leave)
            self.current_index -= 1

        elif structure_type == "while":
            loop_start_label = self.generator.generate_label()
            loop_end_label = self.generator.generate_label()

            self.generator.init_label(loop_start_label)

            condition_type = self.evaluate_expression()
            if condition_type != "Boolean":
                self.errors.append(f"Error on line {line}: Condition in 'if' should be boolean.")
                return

            self.generator.emit(loop_end_label, "label")
            self.generator.add_JF(loop_end_label)

            self.process_block()

            self.generator.emit(loop_start_label, "label")
            self.generator.add_JMP(loop_start_label)

            self.generator.init_label(loop_end_label)
            self.current_index -= 1

    def process_block(self):
        while self.current_index < len(self.symbols_table):
            line, lexeme, token_type, _ = self.symbols_table[self.current_index]
            if lexeme == "}":
                self.current_index += 1
                break
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
                self.current_index -= 1
            elif token_type in ["add_op", "mult_op", "divide_op", "comp_op"]:
                self.handle_operation(line, lexeme)

            self.current_index += 1

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
            if expected is None:
                return lexeme
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

        operand_stack = []
        operator_stack = []

        while self.current_index < len(self.symbols_table):
            line_number, lexeme, token_type, _ = self.symbols_table[self.current_index]

            if line_number != current_line:
                break

            if lexeme in ["false", "true"]:
                expr_type = self.update_type(expr_type, "Boolean")
                self.generator.emit(lexeme, "Boolean")
                operand_stack.append(lexeme)
                if lexeme not in self.generator.tableOfConst:
                    self.generator.tableOfConst[lexeme] = "Boolean"
                self.current_index += 1
                continue

            if token_type == "comp_op" or lexeme in ["<=", ">=", "!=", "=="]:
                found_operator = True
                expr_type = "Boolean"
                operator_stack.append(lexeme)
                self.current_index += 1
                continue

            if token_type == "int" or lexeme.isdigit():
                expr_type = self.update_type(expr_type, "Int")
                self.generator.emit(lexeme, "Int")
                operand_stack.append(lexeme)
                if lexeme not in self.generator.tableOfConst:
                    self.generator.tableOfConst[lexeme] = "Int"
            elif token_type == "float" or self.is_float_literal(lexeme):
                expr_type = self.update_type(expr_type, "Float")
                self.generator.emit(lexeme, "Float")
                operand_stack.append(lexeme)
                if lexeme not in self.generator.tableOfConst:
                    self.generator.tableOfConst[lexeme] = "Float"

            elif token_type == "string":
                expr_type = self.update_type(expr_type, "String")
                self.generator.emit(lexeme, "String")
                operand_stack.append(lexeme)
                if lexeme not in self.generator.tableOfConst:
                    self.generator.tableOfConst[lexeme] = "String"

            elif token_type == "id" and lexeme in self.variables:
                var_type = self.variables[lexeme]["type"]
                expr_type = self.update_type(expr_type, var_type)
                self.generator.emit(lexeme, "r-val")
                operand_stack.append(lexeme)

            if token_type in ["add_op", "mult_op", "divide_op", "comp_op"] or lexeme in ["+", "-", "*", "/", "^"]:
                found_operator = True
                operator_stack.append(lexeme)

            self.current_index += 1

        while operator_stack:
            if len(operand_stack) < 2:
                operator = operator_stack.pop()
                if operator == "-":

                    self.generator.emit("NEG",  "add_op")
                else:
                    self.errors.append(f"Error: Missing operand for operator '{operator_stack[-1]}'.")
                break

            operator = operator_stack.pop()
            type_of_op = "op"

            if operator in ["+", "-"]:
                type_of_op = "add_op"
            elif operator == "*":
                type_of_op = "mult_op"
            elif operator == "/":
                type_of_op = "divide_op"
            elif operator == "^":
                type_of_op = "pow_op"

            self.generator.emit(operator, type_of_op)

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

# parser = Parser(tableOfSymb)
# result = parser.parse()

check = Semantic(list(tableOfSymb.values()))
result = check.analyze()


def save_postfix_code(file_name, generator, variables):
    fname = f"{file_name}.postfix"
    with open(fname, 'w') as f:
        f.write(".target: Postfix Machine\n.version: 0.2\n")
        f.write("\n.vars(\n")
        for var, var_details in variables.items():
            f.write(f"   {var:<6}{var_details['type']:<10}\n")
        f.write(")\n")
        f.write("\n.labels(\n")
        for lbl, pos in generator.tableOfLabel.items():
            if pos is None:
                pos = "undefined"
            f.write(f"   {lbl:<6}{pos}\n")
        f.write(")\n")
        f.write("\n.constants(\n")
        for const, const_type in generator.tableOfConst.items():
            f.write(f"   {const:<6}{const_type:<10}\n")
        f.write(")\n")
        f.write("\n.code(\n")
        for opcode, operand in generator.postfixCodeTSM:
            if operand is not None:
                f.write(f"   {opcode:<6}{operand}\n")
            else:
                f.write(f"   {opcode:<6}\n")
        f.write(")\n")
    print(f"Postfix code saved to {fname}")



if result:
    print('\n---------------------\n')

    analyzer = Poliz(list(tableOfSymb.values()))
    analyzer.analyze()
    analyzer.format_types()
    save_postfix_code("output", analyzer.generator, analyzer.variables)
    saveCIL("example", analyzer.generator.tableOfVar, analyzer.generator.postfixCodeTSM)

else:
    print("Semantic analysis aborted due to syntax errors.")