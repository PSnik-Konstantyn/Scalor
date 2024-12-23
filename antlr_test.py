from gen.ScalorLexer import ScalorLexer
from gen.ScalorParser import ScalorParser
from antlr4 import *
from antlr4.tree.Trees import Trees


def main():
    with open("main.scalor", "r", encoding="utf-8") as file:
        code = file.read()

    def display_parse_tree(tree, parser, indent="", last=True):
        rule_names = parser.ruleNames
        rule_index = tree.getRuleIndex()
        rule_name = rule_names[rule_index]
        symbol = "`-- " if last else "/-- "
        print(f"{indent}{symbol}{rule_name}")

        next_indent = indent + ("  " if last else "/  ")
        for i in range(tree.getChildCount()):
            child = tree.getChild(i)
            is_last_child = i == (tree.getChildCount() - 1)
            if isinstance(child, TerminalNode):
                print(f"{next_indent}{'`-- ' if is_last_child else '/-- '}TOKEN: {child.getText()}")
            else:
                display_parse_tree(child, parser, next_indent, is_last_child)

    input_stream = InputStream(code)
    lexer = ScalorLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ScalorParser(stream)
    tree = parser.program()

    print("Parse Tree:")
    display_parse_tree(tree, parser)


if __name__ == "__main__":
    main()
