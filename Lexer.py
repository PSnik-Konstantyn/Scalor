tokenTable = {
    '^': 'power_op', '!=': 'comp_op', '==': 'comp_op', '<=': 'comp_op', '>=': 'comp_op',  # Добавляем двухсимвольные операторы
    '+': 'add_op', '-': 'add_op', '*': 'mult_op', '/': 'divide_op', '!': 'comp_op',
    '(': 'par_op', ')': 'par_op', '{': 'brace_op', '}': 'brace_op',
    '.': 'dot', '\t': 'ws', ' ': 'ws', '\n': 'end', '=': 'assign_op', ':': 'type_op',
    'val': 'keyword', 'var': 'keyword', 'Int': 'type', 'Float': 'type',
    'Boolean': 'type', 'String': 'type', '>': 'comp_op', '<': 'comp_op',  # Одиночные операторы
    'while': 'keyword', 'if': 'keyword', 'else': 'keyword', 'print': 'keyword', 'StringLiteral': 'string', 'true': 'keyword', '//': 'comment'
}

tokStateTable = {
    2: 'id', 4: 'int', 6: 'float', 8: 'comp_op', 9: 'assign_op', 13: 'par_op', 20: 'divide_op', 23: 'string'
}

stf = {
    (0, 'WhiteSpace'): 0,
    (0, 'end'): 14,
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
    (7, '='): 8,  # Переход для >= и <=
    (7, 'OtherChar'): 9,  # Одиночный оператор < или >

    (0, '='): 10,
    (10, '='): 11,  # Переход для == (двойное равно)
    (10, 'OtherChar'): 12,

    (0, '!'): 15,
    (15, '='): 16,

    (17, '/'): 18,
    (17, 'OtherChar'): 20,
    (17, 'Letter'): 20,
    (17, 'Digit'): 20,

    (18, 'Letter'): 18,
    (18, 'Digit'): 18,
    (18, 'OtherChar'): 18,
    (18, 'end'): 19,
    (19, 'OtherChar'): 0,
    (19, 'Digit'): 0,
    (19, 'Letter'): 0,
    (19, 'WhiteSpace'): 0,

    (20, 'Digit'): 0,
    (0, '!'): 15,
    (15, '='): 16,
    (15, 'OtherChar'): 102,
    (15, 'Letter'): 102,
    (15, 'Digit'): 102,

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

    (0, '"'): 21,
    (21, 'Letter'): 21,
    (21, 'Digit'): 21,
    (21, 'WhiteSpace'): 21,
    (21, '"'): 23,
    (23, 'OtherChar'): 0,

    (0, 'OtherChar'): 100
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

f = open('main.txt', 'r')
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
            if char == '\n':
                classCh = 'end'

            if char == '!':
                classCh = 'Digit'

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


def classOfChar(char):
    if char == '.':
        return "Dot"
    elif char.isalpha():
        return "Letter"
    elif char.isdigit():
        return "Digit"
    elif char.isspace():
        return "WhiteSpace"
    elif char in ['\n', '\r', '$']:
        return "end"
    elif char in "()+-*/{}^:=><\!\",":
        return char
    else:
        return 'OtherChar'


def processing():
    global state, lexeme, char, numLine, numChar, tableOfSymb
    lexeme = lexeme.strip()
    if state == 19:
        lexeme = ''
        state = initState
        numLine += 1
        return
    if state == 14:
        numLine += 1
        state = initState
    elif state == 23:
        lexeme = lexeme.strip('"')
        token = getToken(state, lexeme)
        if token != 'keyword' and token != 'type':
            index = indexIdConst(state, lexeme)
            if isinstance(index, tuple):
                index = index[1]
        print(f'{numLine:<3d} "{lexeme}"   {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = initState
    elif state in (2, 4, 6, 8, 9):
        token = getToken(state, lexeme)
        if token != 'keyword' and token != 'type':
            index = indexIdConst(state, lexeme)
            if isinstance(index, tuple):
                index = index[1]
            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s} {index:<5d}')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, index)
        else:
            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        numChar = putCharBack(numChar)
        state = initState
    elif state in (12, 11, 8, 13, 20, 16):
        lexeme += char
        lexeme = lexeme.strip()
        token = getToken(state, lexeme)
        print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = initState

    if state in Ferror:
        fail()


def nextState(state, classCh):
    try:
        return stf[(state, classCh)]
    except KeyError:
        if state in Ferror:
            return state
        return stf.get((state, 'OtherChar'), 100)


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
        if state == 23:
            return 'string'
        return tokenTable[lexeme]
    except KeyError:
        return tokStateTable[state]


def is_final(state):
    return state in F


def nextChar():
    global numChar
    numChar += 1
    return sourceCode[numChar]


def putCharBack(numChar):
    return numChar - 1


def indexIdConst(state, lexeme):
    indx = 0
    if state == 2:
        indx = tableOfId.get(lexeme)
        if indx is None:
            indx = len(tableOfId) + 1
            tableOfId[lexeme] = indx
    if state in (4, 6, 23):
        indx = tableOfConst.get(lexeme)
        if indx is None:
            indx = len(tableOfConst) + 1
            tableOfConst[lexeme] = (tokStateTable[state], indx)
    return indx


lex()

print('-' * 30)
print(f'tableOfSymb: {tableOfSymb}')
print(f'tableOfId: {tableOfId}')
print(f'tableOfConst: {tableOfConst}')
