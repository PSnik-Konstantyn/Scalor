from Lexer import tableOfSymb

indent_level = 0

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 1

    def parse(self):
        try:
            while self.pos < len(self.tokens):
                self.statement()
            print("Syntax analysis completed successfully.")
            return True
        except SyntaxError as e:
            print(f"Syntax Error at token {self.pos}: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        return False

    def statement(self):
        if self.lookahead('keyword', 'val') or self.lookahead('keyword', 'var'):
            self.variable_declaration()
        elif self.lookahead('keyword', 'if'):
            self.if_statement()
        elif self.lookahead('keyword', 'while'):
            self.while_statement()
        elif self.lookahead('keyword', 'print'):
            self.print_statement()
        elif self.lookahead('id'):
            self.assignment_statement()
        else:
            raise SyntaxError(f"Unknown statement starting at token {self.peek()}.")

    def variable_declaration(self):
        try:
            keyword_token = self.consume('keyword')
            identifier = self.consume('id')
            self.consume('type_op', ':')
            var_type = self.consume('type')

            if self.peek()[2] == 'assign_op':
                self.consume('assign_op', '=')
                expr = self.expression()
                self.print_with_indent(f"Variable declaration: {keyword_token} {identifier} : {var_type} = {expr}")
            else:
                self.print_with_indent(f"Variable declaration: {keyword_token} {identifier} : {var_type} (no assignment)")
        except SyntaxError as e:
            raise SyntaxError(f"Error in variable declaration: {e}")

    def assignment_statement(self):
        try:
            identifier = self.consume('id')
            self.consume('assign_op', '=')
            expr = self.expression()
            self.print_with_indent(f"Assignment: {identifier} = {expr}")
        except SyntaxError as e:
            raise SyntaxError(f"Error in assignment: {e}")

    def expression(self):
        try:
            left = self.term()
            while self.lookahead('comp_op') or self.lookahead_double_op() or self.lookahead('add_op'):
                if self.lookahead_double_op():
                    operator = self.consume('comp_op')
                elif self.lookahead('comp_op'):
                    operator = self.consume('comp_op')
                elif self.lookahead('add_op'):
                    operator = self.consume('add_op')
                right = self.term()
                left = (left, operator, right)
            return left
        except SyntaxError as e:
            raise SyntaxError(f"Error in expression: {e}")

    def term(self):
        try:
            left = self.factor()
            while self.lookahead('mult_op') or self.lookahead('divide_op'):
                operator = self.consume('mult_op') if self.lookahead('mult_op') else self.consume('divide_op')
                right = self.factor()
                left = (left, operator, right)
            return left
        except SyntaxError as e:
            raise SyntaxError(f"Error in term: {e}")

    def factor(self):
        try:
            left = self.primary()
            if self.lookahead('power_op'):
                operator = self.consume('power_op')
                right = self.factor()
                left = (left, operator, right)
            return left
        except SyntaxError as e:
            raise SyntaxError(f"Error in factor: {e}")

    def primary(self):
        if self.lookahead('add_op', '-') and self.lookahead_next_is_numeric():
            self.consume('add_op', '-')
            return f"-{self.primary()}"

        if self.lookahead('int'):
            return self.consume('int')
        elif self.lookahead('float'):
            return self.consume('float')
        elif self.lookahead('id'):
            return self.consume('id')
        elif self.lookahead('keyword', 'true') or self.lookahead('keyword', 'false'):
            return self.consume('keyword')
        elif self.lookahead('string'):
            return self.consume('string')
        elif self.lookahead('par_op', '('):
            self.consume('par_op', '(')
            expr = self.expression()
            self.consume('par_op', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected token in primary expression: {self.peek()}")

    def lookahead_next_is_numeric(self):
        return (self.pos + 1 < len(self.tokens) and
                (self.tokens[self.pos + 1][2] == 'int' or self.tokens[self.pos + 1][2] == 'float'))

    def comparison_expression(self):
        try:
            left = self.expression_part()
            if self.lookahead('comp_op'):
                operator = self.consume('comp_op')
                right = self.expression_part()
                return (left, operator, right)
            else:
                raise SyntaxError("Expected comparison operator in if/while condition.")
        except SyntaxError as e:
            raise SyntaxError(f"Error in comparison expression: {e}")

    def expression_part(self):
        try:
            left = self.term()
            while self.lookahead('add_op'):
                operator = self.consume('add_op')
                right = self.term()
                left = (left, operator, right)
            return left
        except SyntaxError as e:
            raise SyntaxError(f"Error in expression part: {e}")

    def if_statement(self):
        try:
            global indent_level
            self.consume('keyword', 'if')
            self.consume('par_op', '(')
            condition = self.comparison_expression()
            self.consume('par_op', ')')
            self.consume('brace_op', '{')

            self.print_with_indent(f"If statement with condition: {condition}")
            indent_level += 1

            while not self.lookahead('brace_op', '}'):
                self.statement()
            self.consume('brace_op', '}')
            indent_level -= 1

            if self.lookahead('keyword', 'else'):
                self.consume('keyword', 'else')
                self.consume('brace_op', '{')
                self.print_with_indent(f"Else statement:")
                indent_level += 1

                while not self.lookahead('brace_op', '}'):
                    self.statement()
                self.consume('brace_op', '}')
                indent_level -= 1
        except SyntaxError as e:
            raise SyntaxError(f"Error in if-statement: {e}")

    def while_statement(self):
        try:
            global indent_level
            self.consume('keyword', 'while')
            self.consume('par_op', '(')
            condition = self.comparison_expression()
            self.consume('par_op', ')')
            self.consume('brace_op', '{')

            self.print_with_indent(f"While loop with condition: {condition}")
            indent_level += 1

            while not self.lookahead('brace_op', '}'):
                self.statement()
            self.consume('brace_op', '}')
            indent_level -= 1
        except SyntaxError as e:
            raise SyntaxError(f"Error in while-statement: {e}")

    def print_statement(self):
        try:
            self.consume('keyword', 'print')
            self.consume('par_op', '(')
            expr = self.expression()
            self.consume('par_op', ')')
            self.print_with_indent(f"Print statement recognized with argument: {expr}")
        except SyntaxError as e:
            raise SyntaxError(f"Error in print statement: {e}")

    def consume(self, token_type, lexeme=None):
        if self.lookahead_double_op():
            current_token = self.tokens[self.pos][1] + self.tokens[self.pos + 1][1]
            self.pos += 2
            return current_token

        if self.lookahead(token_type, lexeme):
            current_token = self.tokens[self.pos]
            self.pos += 1
            return current_token[1]

        raise SyntaxError(f"Expected {token_type} '{lexeme}', but got {self.peek()}")

    def lookahead(self, token_type, lexeme=None):
        if self.pos < len(self.tokens)+1:
            # +1
            token = self.tokens[self.pos]
            if token[2] == token_type:
                if lexeme is None or token[1] == lexeme:
                    return True
        return False

    def lookahead_double_op(self):
        if self.pos + 1 < len(self.tokens):
            current_token = self.tokens[self.pos]
            next_token = self.tokens[self.pos + 1]
            if current_token[1] in ['<', '>', '!', '='] and next_token[1] == '=':
                return True
        return False

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def print_with_indent(self, param):
        line_number = self.tokens[self.pos - 1][0]
        text = ":\t" + "\t" * indent_level + param
        print(f"{line_number}{text}")

parser = Parser(tableOfSymb)
parser.parse()
