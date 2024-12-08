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
        self.tableOfLabel[label] = len(self.tableOfLabel)
        return label

    def add_variable(self, var_name, var_type):
        if var_name not in self.tableOfVar:
            self.tableOfVar[var_name] = (len(self.tableOfVar), var_type)
        else:
            print(f"Warning: Variable '{var_name}' is already defined.")

    def add_constant(self, const_value, const_type):
        if const_value not in self.tableOfConst:
            self.tableOfConst[const_value] = (len(self.tableOfConst), const_type)
        else:
            print(f"Warning: Constant '{const_value}' is already defined.")

    def emit(self, opcode, operand=None):
        self.postfixCodeTSM.append((opcode, operand))


def save_postfix_code(file_name, generator):
    fname = f"{file_name}.postfix"
    with open(fname, 'w') as f:
        f.write(".target: Postfix Machine\n.version: 0.2\n")

        # Змінні
        f.write("\n.vars(\n")
        for var, var_type in generator.tableOfVar.items():
            f.write(f"   {var:<6}{var_type:<10}\n")
        f.write(")\n")

        # Константи
        f.write("\n.constants(\n")
        for const, const_type in generator.tableOfConst.items():
            f.write(f"   {const:<6}{const_type:<10}\n")
        f.write(")\n")

        # Код
        f.write("\n.code(\n")
        for opcode, operand in generator.postfixCodeTSM:
            if operand is not None:
                f.write(f"   {opcode:<6}{operand}\n")
            else:
                f.write(f"   {opcode:<6}\n")
        f.write(")\n")
    print(f"Postfix code saved to {fname}")
