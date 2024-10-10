# Оновлена таблиця лексем для підтримки автомата
tokenTable = {
    'program': 'keyword', 'end': 'keyword', ':=': 'assign_op',
    '+': 'add_op', '-': 'add_op', '*': 'mult_op', '/': 'mult_op',
    '(': 'par_op', ')': 'par_op', '{': 'brace_op', '}': 'brace_op',
    '.': 'dot', '\t': 'ws', ' ': 'ws', '\n': 'nl', '=': 'assign_op', ':': "type_op",
    'val': 'keyword', 'var': 'keyword', 'Int': 'type', 'Float': 'type',
    'Boolean': 'type', 'String': 'type', '>': 'comp_op', '<': 'comp_op', '!=': 'comp_op', '==': 'comp_op',
    'while': 'keyword', 'if': 'keyword', 'else': 'keyword', 'print': 'keyword'
}

# Решта токенів визначається за заключним станом
tokStateTable = {2: 'id', 4: 'int', 6: 'float', 8: 'comp_op', 9: 'assign_op'}

stf = {
    # Початковий стан 0: починаємо з читання символу
    (0, 'WhiteSpace'): 0,  # Пропускаємо пробіли
    (0, 'Letter'): 1,  # Якщо це літера, переходимо в стан розпізнавання ідентифікатора
    (1, 'Letter'): 1,  # Ідентифікатор може складатися з літер і цифр
    (1, 'Digit'): 1,
    (1, 'OtherChar'): 2,  # Завершуємо розпізнавання ідентифікатора

    (0, 'Digit'): 3,  # Якщо цифра, переходимо в стан розпізнавання числа
    (3, 'Digit'): 3,  # Читаємо цілу частину числа
    (3, 'OtherChar'): 4,  # Завершуємо розпізнавання цілого числа
    (3, 'Dot'): 5,  # Точка може бути початком числа з плаваючою точкою
    (5, 'Digit'): 5,  # Читаємо дробову частину числа
    (5, 'OtherChar'): 6,  # Завершуємо розпізнавання числа з плаваючою точкою

    (0, '>'): 7,  # Розпізнаємо оператор більше
    (0, '<'): 7,  # Розпізнаємо оператор менше
    (7, '='): 8,  # Розпізнаємо оператор порівняння (>= або <=)
    (7, 'OtherChar'): 9,  # Якщо немає '=', то це просто '>' або '<'

    (0, '='): 10,  # Розпізнаємо оператор присвоєння або порівняння
    (10, '='): 11,  # Якщо після '=' є ще один '=', то це оператор порівняння '=='
    (10, 'OtherChar'): 12,  # Якщо немає другого '=', то це оператор присвоєння '='

    # Арифметичні оператори і дужки
    (0, '+'): 13,  # Додаємо підтримку оператора +
    (0, '-'): 13,  # Оператор -
    (0, '*'): 13,  # Оператор *
    (0, '/'): 17,  # Оператор / (може бути початком коментаря)
    (0, '('): 13,  # Відкриваюча дужка (
    (0, ')'): 13,  # Закриваюча дужка )
    (0, '{'): 13,  # Відкриваюча фігурна дужка {
    (0, '}'): 13,  # Закриваюча фігурна дужка }
    (0, ':'): 13,

    # Коментарі
    (17, '/'): 18,  # Початок однорядкового коментаря //
    (18, 'OtherChar'): 18,  # Ігноруємо всі символи в межах коментаря
    (18, 'EndOfLine'): 19,  # Кінець коментаря на новому рядку
    (19, 'OtherChar'): 0,  # Повертаємось у початковий стан після кінця коментаря

    (0, '"'): 21,  # Початок рядкового літералу
    (21, 'Letter'): 21,  # Все, що в лапках — це допустимі символи
    (21, 'Digit'): 21,  # Цифри всередині рядка
    (21, 'Symbol'): 21,  # Інші символи всередині рядка
    (21, 'WhiteSpace'): 21,  # Дозволяємо пробіли всередині рядка
    (21, '"'): 23,  # Завершення рядка на другій лапці
    (23, 'OtherChar'): 0,

    # Обробка помилок
    (0, 'OtherChar'): 100,  # Невідомий символ у початковому стані — помилка
}

F = {2, 4, 6, 8, 9, 11, 12, 13, 14, 19, 20, 23, 100, 102}
Fstar = {2, 4, 6, 19, 20, 23}

# Початковий стан і множина фінальних станів
initState = 0
Ferror = {100, 102}

tableOfId = {}
tableOfConst = {}
tableOfSymb = {}

state = initState
FSuccess = ('Lexer', False)

# Відкриваємо файл з кодом
f = open('main.scalor', 'r')
sourceCode = f.read()
f.close()

lenCode = len(sourceCode) - 1
numLine = 1
numChar = -1
char = ''
lexeme = ''


def lex():
    global state, numLine, char, lexeme, numChar, FSuccess
    try:
        while numChar < lenCode:
            char = nextChar()
            classCh = classOfChar(char)
            state = nextState(state, classCh)
            if is_final(state):
                processing()
            elif state == initState:
                lexeme = ''
            else:
                lexeme += char
        print('Lexer: Лексичний аналіз завершено успішно')
        FSuccess = ('Lexer', True)
    except SystemExit as e:
        print(f'Lexer: Аварійне завершення програми з кодом {e}')


def processing():
    global state, lexeme, char, numLine, numChar, tableOfSymb
    lexeme = lexeme.strip()  # Видалити зайві пробіли з лексеми
    if state == 13:  # \n
        numLine += 1
        state = initState
    if state in (2, 4, 6, 8, 9, 23):  # id, float, int, assign_op, comp_op, string
        token = getToken(state, lexeme)
        if token != 'keyword':
            index = indexIdConst(state, lexeme)
            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s} {index:<5d} ')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, index)
        else:
            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        numChar = putCharBack(numChar)
        state = initState
    if state == 12 or state == 14:
        lexeme += char
        lexeme = lexeme.strip()  # Видалити зайві пробіли з лексеми
        token = getToken(state, lexeme)
        print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = initState
    if state in Ferror:
        fail()


def fail():
    global state, numLine, char
    if state == 100:
        print(f'Lexer: у рядку {numLine} неочікуваний символ {char}')
        exit(100)
    if state == 102:
        print(f'Lexer: у рядку {numLine} очікувався символ =, а не {char}')
        exit(102)


def is_final(state):
    return state in F


def nextState(state, classCh):
    try:
        return stf[(state, classCh)]
    except KeyError:
        if state in Ferror:
            return state  # залишаємось у стані помилки
        return stf.get((state, 'OtherChar'), 100)  # або перехід у стан помилки


def nextChar():
    global numChar
    numChar += 1
    return sourceCode[numChar]


def putCharBack(numChar):
    return numChar - 1


def classOfChar(char):
    if char == '.':
        return "Dot"
    elif char.isalpha():
        return "Letter"
    elif char.isdigit():
        return "Digit"
    elif char.isspace():
        return "WhiteSpace"
    elif char == '\n':
        return "EndOfLine"
    elif char in "()+-*/{}^:=><!":
        return char
    else:
        return 'OtherChar'


def getToken(state, lexeme):
    try:
        return tokenTable[lexeme]
    except KeyError:
        return tokStateTable[state]


def indexIdConst(state, lexeme):
    indx = 0
    if state == 2:
        indx = tableOfId.get(lexeme)
        if indx is None:
            indx = len(tableOfId) + 1
            tableOfId[lexeme] = indx
    if state in (4, 6):
        indx = tableOfConst.get(lexeme)
        if indx is None:
            indx = len(tableOfConst) + 1
            tableOfConst[lexeme] = (tokStateTable[state], indx)
    return indx


# запуск лексичного аналізатора
lex()

# Виведення таблиць
print('-' * 30)
print(f'tableOfSymb: {tableOfSymb}')
print(f'tableOfId: {tableOfId}')
print(f'tableOfConst: {tableOfConst}')
