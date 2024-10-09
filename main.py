from Lexer import Lexer
from config import lexer_config

lexer = Lexer(lexer_config)

with open("example.scalor", "r", encoding="utf8") as source_code:
    tokens = lexer.analyze(source_code.read())
    print("Tokens:", tokens)
