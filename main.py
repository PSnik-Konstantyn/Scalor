from Lexer import Lexer
from config import lexer_config


lexer: Lexer = Lexer(**lexer_config)

with open("example.scalor", "r", encoding="utf8") as source_code:
    lexer.analyze(source_code.read())
