grammar Expr;

prog:   stat+ ;

stat:   expr NEWLINE                # printExpr
    |   ID '=' expr NEWLINE        # assign
    |   NEWLINE                    # blank
    ;

expr:   expr op=('*'|'/') expr
    |   expr op=('+'|'-') expr
    |   INT
    |   ID
    |   '(' expr ')'
    ;

ID  : [a-zA-Z]+ ;
INT : [0-9]+ ;
NEWLINE : '\r'? '\n' ;
WS  : [ \t]+ -> skip ;