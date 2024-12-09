class PostfixGenerator:
    def __init__(self):
        self.tableOfVar = {}  # Таблиця змінних
        self.tableOfLabel = {}  # Таблиця міток
        self.tableOfConst = {}  # Таблиця констант
        self.postfixCodeTSM = []  # Постфіксний код
        self.labelCounter = 0

    def generate_label(self):
        label = f"m{self.labelCounter}"
        while label in self.tableOfLabel:
            self.labelCounter += 1
            label = f"m{self.labelCounter}"
        self.tableOfLabel[label] = len(self.postfixCodeTSM)
        return label

    def add_variable(self, var_name, var_type):
        if var_name not in self.tableOfVar:
            self.tableOfVar[var_name] = (len(self.tableOfVar), var_type.lower())
        else:
            print(f"Warning: Variable '{var_name}' is already defined.")

    def add_constant(self, const_value, const_type):
        if const_value not in self.tableOfConst:
            self.tableOfConst[const_value] = (len(self.tableOfConst), const_type)
        else:
            print(f"Warning: Constant '{const_value}' is already defined.")

    def emit(self, opcode, operand=None):
        self.postfixCodeTSM.append((opcode, operand))

