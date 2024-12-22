grammar Scalor;

program          : declSection doSection EOF ;
declSection      : declarList ;
declarList       : declaration (',' declaration)* ;
declaration      : varDecl | valDecl ;
varDecl          : 'var' IDENT ':' type '=' expression ;
valDecl          : 'val' IDENT ':' type '=' expression ;
type             : 'Int' | 'Float' | 'Boolean' | 'String' ;
doSection        : statementList ;
statementList    : statement+ ;
statement        : assign
                 | ifStatement
                 | whileStatement
                 | printStatement
                 | inputStatement ;
assign           : IDENT '=' expression ;
ifStatement      : 'if' '(' expression ')' doBlock ('else' doBlock)? ;
whileStatement   : 'while' '(' expression ')' doBlock ;
printStatement   : 'print' '(' expression ')' ;
inputStatement   : 'input' '(' IDENT ')' ;
expression       : arithmExpression
                 | boolExpr
                 | concatExpression ;
boolExpr         : arithmExpression relOp arithmExpression
                 | 'true'
                 | 'false'
                 | '(' boolExpr ')' ;
arithmExpression : power (( '+' | '-' ) power)* ;
power            : term ('^' term)* ;
term             : factor (( '*' | '/' ) factor)* ;
factor           : IDENT
                 | constant
                 | '(' arithmExpression ')' ;
concatExpression : STRING_CONST '+' (STRING_CONST | IDENT) ;
doBlock          : statement | '{' statementList '}' ;
constant         : INT_NUMB | FLOAT_NUMB | BOOL_CONST | STRING_CONST ;

relOp            : '==' | '!=' | '<' | '>' | '<=' | '>=' ;
IDENT            : LETTER (LETTER | DIGIT)* ;
INT_NUMB         : '-'? DIGIT+ ;
FLOAT_NUMB       : '-'? DIGIT+ '.' DIGIT+ ;
BOOL_CONST       : 'true' | 'false' ;
STRING_CONST     : '"' (~["])* '"' ;
LETTER           : [a-zA-Z] ;
DIGIT            : [0-9] ;
SYMBOL           : [!@#$%^&*()\-:/“”,.] ;

WS               : [ \t\r\n]+ -> skip ;
COMMENT          : '//' ~[\r\n]* -> skip ;
