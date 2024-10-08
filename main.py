from Lexer import  ScalorLexer
from config import lexer_config


interpreter = ScalorLexer()
with open("example.scalor", "r", encoding="utf8") as source_code:
    tokens = interpreter.analyze(source_code)
    print("Tokens:", tokens)

    interpreter.parse()