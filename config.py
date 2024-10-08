letters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
    "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
    "S", "T", "U", "V", "W", "X", "Y", "Z"
]

digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

signs = [
    ".", ";", "=", "*", "+", "-", "/", "^", "(", ")", "<", ">", "{", "}", ":", " ", "\n"
]

lexer_config = {
    "token_table": {
        "true": "Boolean", "false": "Boolean",
        "var": "keyword", "val": "keyword", "if": "keyword", "else": "keyword", "while": "keyword",
        "print": "keyword", "Int": "type", "Float": "type", "Boolean": "type", "String": "type",
        "=": "assign_op", "+": "add_op", "-": "add_op", "*": "mult_op", "/": "mult_op", "^": "power_op",
        ">": "rel_op", "<": "rel_op", ">=": "rel_op", "<=": "rel_op", "==": "rel_op", "!=": "rel_op",
        "(": "brackets_op", ")": "brackets_op", "{": "brackets_op", "}": "brackets_op",
        ".": "punct", ";": "punct",
        ":": "colon_op",
        " ": "ws", "\n": "eol"
    },
    "tok_state_table": {
        2: "id",
        4: "int",
        6: "float",
        12: "assign_op",
        8: "rel_op",
        11: "rel_op",
        16: "rel_op",
        24: "colon_op",
        14: "endofline",
        23: "string"
    },
    "stf": {
        (0, "ws"): 0,
        (1, "ws"): 2,
        (1, "Letter"): 1,  # продолжаем читать идентификаторы
        (1, "Digit"): 1,
        (1, ":"): 24,
        (0, "Letter"): 1, (1, "Letter"): 1, (1, "Digit"): 1, (1, "OtherChar"): 2,
        (0, "Digit"): 3, (3, "Digit"): 3, (3, "OtherChar"): 4, (3, "Dot"): 5, (5, "Digit"): 5, (5, "OtherChar"): 6,
        (0, ">"): 7, (0, "<"): 7, (7, "="): 8, (7, "OtherChar"): 9,
        (0, "="): 10, (10, "="): 11, (10, "OtherChar"): 12,
        (0, "+"): 13, (0, "-"): 13, (0, "*"): 13, (0, "/"): 13,
        (0, "!"): 15, (15, "="): 16, (15, "OtherChar"): 102,
        (0, "EndOfLine"): 14,
        (0, "/"): 17, (17, "/"): 18, (18, "OtherChar"): 18, (18, "EndOfLine"): 19, (17, "OtherChar"): 20,
        (0, '"'): 21, (21, "Letter"): 21, (21, "Digit"): 21, (21, "Symbol"): 21, (21, '"'): 23,
        (0, "OtherChar"): 100
    },
    "initial_state": 0,
    "F": [2, 4, 6, 8, 9, 11, 12, 13, 14, 19, 20, 23, 100, 101, 102],
    "F_star": [2, 4, 6, 19, 20],
    "F_error": [100, 101, 102],
    "F_ignore": [14, 19]
}
