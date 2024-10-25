from Lexer import tableOfSymb

indent_level = 0

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 1

    def parse(self):
        while self.pos < len(self.tokens):
            self.statement()

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
            self.expression()

    def variable_declaration(self):
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

    def assignment_statement(self):
        identifier = self.consume('id')
        self.consume('assign_op', '=')
        expr = self.expression()
        self.print_with_indent(f"Assignment: {identifier} = {expr}")

    def expression(self):
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

    def term(self):
        left = self.factor()
        while self.lookahead('mult_op') or self.lookahead('divide_op'):
            operator = self.consume('mult_op') if self.lookahead('mult_op') else self.consume('divide_op')
            right = self.factor()
            left = (left, operator, right)
        return left

    def factor(self):
        left = self.primary()
        while self.lookahead('power_op'):
            operator = self.consume('power_op')
            right = self.primary()
            left = (left, operator, right)
        return left

    def primary(self):
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
            raise SyntaxError(f"Unexpected token: {self.peek()}")

    def if_statement(self):
        global indent_level
        self.consume('keyword', 'if')
        self.consume('par_op', '(')
        condition = self.expression()
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

    def while_statement(self):
        global indent_level
        self.consume('keyword', 'while')
        self.consume('par_op', '(')
        condition = self.expression()
        self.consume('par_op', ')')
        self.consume('brace_op', '{')

        self.print_with_indent(f"While loop with condition: {condition}")
        indent_level += 1

        while not self.lookahead('brace_op', '}'):
            self.statement()
        self.consume('brace_op', '}')
        indent_level -= 1

    def print_statement(self):
        self.consume('keyword', 'print')
        self.consume('par_op', '(')
        expr = self.expression()
        self.consume('par_op', ')')
        self.print_with_indent(f"Print statement recognized with argument: {expr}")

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

