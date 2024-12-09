class PostfixGenerator:
    def __init__(self):
        self.tableOfVar = {}  # Таблиця змінних
        self.tableOfLabel = {}  # Таблиця міток
        self.tableOfConst = {}  # Таблиця констант
        self.postfixCodeTSM = []  # Постфіксний код
        self.labelCounter = 1

    def generate_label(self):
        label = f"m{self.labelCounter}"
        while label in self.tableOfLabel:
            self.labelCounter += 1
            label = f"m{self.labelCounter}"
        self.tableOfLabel[label] = "val_undef"  # Мітка ще не ініціалізована
        return label

    def init_label(self, label):
        if label not in self.tableOfLabel:
            raise ValueError(f"Label '{label}' not found in label table.")
        self.tableOfLabel[label] = len(self.postfixCodeTSM)  # Прив'язка мітки до поточного індексу
        self.postfixCodeTSM.append((label, "label"))
        self.postfixCodeTSM.append((":", "colon"))

    def add_JF(self, label):
        self.emit("JF", "jf")

    def add_JMP(self, label):
        self.emit("JMP", "jump")

    def emit(self, opcode, operand="undefined"):
        self.postfixCodeTSM.append((opcode, operand))

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