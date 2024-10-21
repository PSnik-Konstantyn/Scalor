from Lexer import lex
from Lexer import tableOfSymb

# Викликаємо лексичний аналізатор
FSucces = lex()

# Друкуємо таблицю символів
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-'*30)

# Ініціалізуємо номер рядка таблиці розбору/лексем/символів програми
numRow = 1

# Довжина таблиці символів програми
len_tableOfSymb = len(tableOfSymb)
print(('len_tableOfSymb', len_tableOfSymb))

# Допоміжна функція для зсуву токена
def next_token():
    global numRow
    numRow += 1

# Основна функція для розбору програми
def parseProgram():
        next_token()
        parseDeclSection()  # Розбір секції декларацій
        parseDoSection()    # Розбір секції виконання

def parseDeclaration():
    print(f"Current token: {current_token()}")  # Додаємо для перевірки поточного токену
    if current_token()[1] == 'var':  # Заміна ['token'] на [1]
        next_token()
        parseVarDecl()
    elif current_token()[1] == 'val':  # Заміна ['token'] на [1]
        next_token()
        parseValDecl()
    else:
        raise SyntaxError("Expected 'var' or 'val' in declaration")

# Розбір секції декларацій
def parseDeclSection():
    parseDeclarList()

# Розбір списку декларацій
def parseDeclarList():
    parseDeclaration()
    while current_token() and current_token()['token'] == ',':
        next_token()
        parseDeclaration()

# Розбір оголошення змінної
def parseVarDecl():
    parseIdentList()
    if current_token()['token'] == ':':
        next_token()
        parseType()
        if current_token() and current_token()['token'] == '=':
            next_token()
            parseExpression()

# Розбір оголошення константи
def parseValDecl():
    parseIdentList()
    if current_token()['token'] == ':':
        next_token()
        parseType()
        if current_token() and current_token()['token'] == '=':
            next_token()
            parseExpression()

# Розбір списку ідентифікаторів
def parseIdentList():
    parseIdent()
    while current_token()['token'] == ',':
        next_token()
        parseIdent()

# Розбір секції виконання (списку операторів)
def parseDoSection():
    parseStatementList()

# Розбір списку операторів
def parseStatementList():
    while current_token() and current_token()['token'] != 'end':
        parseStatement()

# Розбір одного оператора
def parseStatement():
    if current_token()['token'] == 'identifier':
        parseAssign()
    elif current_token()['token'] == 'if':
        parseIfStatement()
    elif current_token()['token'] == 'while':
        parseWhileStatement()
    elif current_token()['token'] == 'print':
        parsePrintStatement()
    else:
        raise SyntaxError(f"Unexpected token {current_token()['token']} in statement")

# Розбір присвоєння
def parseAssign():
    parseIdent()
    if current_token()['token'] == '=':
        next_token()
        parseExpression()
    else:
        raise SyntaxError("Expected '=' in assignment")

# Розбір умовного оператора if
def parseIfStatement():
    if current_token()['token'] == 'if':
        next_token()
        if current_token()['token'] == '(':
            next_token()
            parseExpression()
            if current_token()['token'] == ')':
                next_token()
                parseDoBlock()
                if current_token()['token'] == 'else':
                    next_token()
                    parseDoBlock()
            else:
                raise SyntaxError("Expected ')' in if statement")
        else:
            raise SyntaxError("Expected '(' in if statement")

# Розбір циклу while
def parseWhileStatement():
    if current_token()['token'] == 'while':
        next_token()
        if current_token()['token'] == '(':
            next_token()
            parseExpression()
            if current_token()['token'] == ')':
                next_token()
                parseDoBlock()
            else:
                raise SyntaxError("Expected ')' in while statement")
        else:
            raise SyntaxError("Expected '(' in while statement")

# Розбір блоку операторів
def parseDoBlock():
    if current_token()['token'] == '{':
        next_token()
        parseStatementList()
        if current_token()['token'] == '}':
            next_token()
        else:
            raise SyntaxError("Expected '}' in do block")
    else:
        parseStatement()

# Розбір оператора друку
def parsePrintStatement():
    if current_token()['token'] == 'print':
        next_token()
        if current_token()['token'] == '(':
            next_token()
            parseExpression()
            if current_token()['token'] == ')':
                next_token()
            else:
                raise SyntaxError("Expected ')' in print statement")
        else:
            raise SyntaxError("Expected '(' in print statement")

# Розбір виразу
def parseExpression():
    # Поки що спрощена обробка арифметичних виразів
    if current_token()['token'] in ['number', 'identifier', 'true', 'false']:
        next_token()
    else:
        raise SyntaxError("Expected an expression")

def current_token():
    global numRow
    if numRow < len_tableOfSymb:
        return tableOfSymb[numRow]
    return None

# Інші приклади заміни:
def parseIdent():
    if current_token()[1] == 'identifier':  # Заміна ['token'] на [1]
        next_token()
    else:
        raise SyntaxError("Expected identifier")

def parseType():
    if current_token()[1] in ['Int', 'Float', 'Boolean', 'String']:  # Заміна ['token'] на [1]
        next_token()
    else:
        raise SyntaxError("Expected a valid type")

# Запускаємо парсинг програми
parseProgram()
