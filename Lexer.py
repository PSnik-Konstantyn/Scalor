class Lexer:


    def __init__(self, lexer_config):
        self.letters = lexer_config['letters']
        self.digits = lexer_config['digits']
        self.signs = lexer_config['signs']
        self.token_table = lexer_config['token_table']
        self.tok_state_table = lexer_config['tok_state_table']
        self.stf = lexer_config['stf']
        self.initial_state = lexer_config['initial_state']
        self.F = lexer_config['F']
        self.F_star = lexer_config['F_star']
        self.F_error = lexer_config['F_error']
        self.F_ignore = lexer_config['F_ignore']

        self.current_line = 1
        self.current_state = self.initial_state
        self.tokens = []

    def analyze(self, source_code):
        current_token = ''
        for char in source_code:
            if char == '\n':
                self.current_line += 1


            char_type = self.get_char_type(char)

            state_key = (self.current_state, char_type)


            if state_key in self.stf:
                self.current_state = self.stf[state_key]
                current_token += char

                if self.current_state in self.F:
                    # End of token
                    if self.current_state in self.F_star:
                        self.tokens.append(current_token)
                        current_token = ''
            else:
                if self.current_state in self.F:

                    self.tokens.append(current_token)
                    current_token = ''
                    self.current_state = self.initial_state
                else:
                    raise Exception(f"Unexpected character '{char}' at line {self.current_line}")


        if current_token:
            self.tokens.append(current_token)

        return self.tokens

    def get_char_type(self, char):
        if char in self.letters:
            return "Letter"
        elif char in self.digits:
            return "Digit"
        elif char in self.signs:
            return "OtherChar"
        return "OtherChar"
