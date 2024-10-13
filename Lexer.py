tokenTable = {
    'program': 'keyword', 'end': 'keyword', ':=': 'assign_op',
    '+': 'add_op', '-': 'add_op', '*': 'mult_op', '/': 'mult_op',
    '(': 'par_op', ')': 'par_op', '{': 'brace_op', '}': 'brace_op',
    '.': 'dot', '\t': 'ws', ' ': 'ws', '\n': 'nl', '=': 'assign_op', ':': "type_op",
    'val': 'keyword', 'var': 'keyword', 'Int': 'type', 'Float': 'type',
    'Boolean': 'type', 'String': 'type', '>': 'comp_op', '<': 'comp_op', '!=': 'comp_op', '==': 'comp_op',
    'while': 'keyword', 'if': 'keyword', 'else': 'keyword', 'print': 'keyword', 'StringLiteral': 'string',
    '!': 'not_op'  # додано оператор '!'
}

tokStateTable = {
    2: 'id', 4: 'int', 6: 'float', 8: 'comp_op', 9: 'assign_op', 23: 'string'
}

stf = {
    (0, 'WhiteSpace'): 0,
    (0, 'Letter'): 1,
    (1, 'Letter'): 1,
    (1, 'Digit'): 1,
    (1, 'OtherChar'): 2,

    (0, 'Digit'): 3,
    (3, 'Digit'): 3,
    (3, 'OtherChar'): 4,
    (3, 'Dot'): 5,
    (5, 'Digit'): 5,
    (5, 'OtherChar'): 6,

    (0, '>'): 7,
    (0, '<'): 7,
    (7, '='): 8,
    (7, 'OtherChar'): 9,

    (0, '='): 10,
    (10, '='): 11,
    (10, 'OtherChar'): 12,

    (0, '+'): 13,
    (0, '-'): 13,
    (0, '*'): 13,
    (0, '/'): 17,
    (0, '('): 13,
    (0, ')'): 13,
    (0, '^'): 13,
    (0, '{'): 13,
    (0, '}'): 13,
    (0, ':'): 13,
    (0, ','): 13,

    (0, '/'): 17,  # початок обробки оператора '/'
    (17, '/'): 18,  # якщо два '/', це коментар
    (17, 'OtherChar'): 13,  # якщо немає другого '/', це оператор ділення

    (18, 'OtherChar'): 18,  # продовжуємо коментар
    (18, 'EndOfLine'): 19,  # кінець коментаря на кінці рядка
    (0, 'EndOfLine'): 14,
    (19, 'OtherChar'): 0,

    (0, '"'): 21,  # початок обробки рядка
    (21, 'Letter'): 21,
    (21, 'Digit'): 21,
    (21, 'Symbol'): 21,
    (21, 'WhiteSpace'): 21,
    (21, '"'): 23,  # кінець рядка
    (23, 'OtherChar'): 0,

    (0, '!'): 13,  # додано оператор '!' як логічне заперечення

    (0, 'OtherChar'): 100,  # помилка для непередбачуваних символів
}

F = {2, 4, 6, 8, 9, 11, 12, 13, 14, 19, 20, 23, 100, 102}
Fstar = {2, 4, 6, 19, 20, 23}

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


# Лексичний аналізатор для мови 'Scalor'

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

    if state in (13, 19):  # Перевірка символа нового рядка
        numLine += 1
        state = initState

    elif state == 23:  # Обробка стрічкових літералів
        lexeme = lexeme.strip('"')  # Видаляємо лише лапки
        token = getToken(state, lexeme)
        print(f'{numLine:<3d} "{lexeme}"   {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = initState

    elif state in (2, 4, 6, 8, 9):  # Обробка ідентифікаторів, чисел, операторів
        token = getToken(state, lexeme)
        if token != 'keyword':
            index = indexIdConst(state, lexeme)

            # Check if index is a tuple and extract the correct value
            if isinstance(index, tuple):
                index = index[1]  # Extract the index part of the tuple

            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s} {index:<5d}')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, index)
        else:
            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        numChar = putCharBack(numChar)
        state = initState

    elif state == 12 or state == 14:
        lexeme += char
        lexeme = lexeme.strip()  # Видаляємо зайві пробіли
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


def getToken(state, lexeme):
    try:
        if state == 23:  # Стрічковий літерал
            return 'string'
        return tokenTable[lexeme]
    except KeyError:
        return tokStateTable[state]


def is_final(state):
    return state in F


def nextState(state, classCh):
    try:
        return stf[(state, classCh)]
    except KeyError:
        if state in Ferror:
            return state  # залишаємося в стані помилки
        return stf.get((state, 'OtherChar'), 100)  # або перехід в стан помилки


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
    elif char in "()+-*/{}^:=><\!\",.":
        return char
    else:
        return 'OtherChar'


def indexIdConst(state, lexeme):
    indx = 0
    if state == 2:  # Ідентифікатор
        indx = tableOfId.get(lexeme)
        if indx is None:
            indx = len(tableOfId) + 1
            tableOfId[lexeme] = indx
    if state in (4, 6):  # Константи Int та Float
        indx = tableOfConst.get(lexeme)
        if indx is None:
            indx = len(tableOfConst) + 1
            tableOfConst[lexeme] = (tokStateTable[state], indx)
    return indx


# Запуск лексичного аналізатора
lex()

# Виведення таблиць
print('-' * 30)
print(f'tableOfSymb: {tableOfSymb}')
print(f'tableOfId: {tableOfId}')
print(f'tableOfConst: {tableOfConst}')
