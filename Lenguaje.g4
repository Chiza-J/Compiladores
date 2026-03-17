grammar Lenguaje;

// ===== PARSER =====
programa : instrucciones EOF;

instrucciones : (instruccion)*;

instruccion
    : declaracion
    | impresion
    | errorInstr
    ;

declaracion : VARIABLI tipo ID IGUAL INT PUNTOCOMA;

impresion : AMPRIMI ID PUNTOCOMA;

tipo : ONTIE | FLOTE | DUBLE;

// Manejo de error
errorInstr : ERROR_CHAR+;

// ===== LEXER =====

// PALABRAS RESERVADAS (PRIMERO)
VARIABLI : 'variabli';
ONTIE    : 'ontie';
FLOTE    : 'flote';
DUBLE    : 'duble';
AMPRIMI  : 'amprimi';

// SÍMBOLOS (IMPORTANTE)
IGUAL      : '=';
PUNTOCOMA  : ';';

// TOKENS
ID  : [a-zA-Z_][a-zA-Z_0-9]*;
INT : [0-9]+;

// IGNORAR ESPACIOS
WS : [ \t\r\n]+ -> skip;

// ERROR (SIEMPRE AL FINAL)
ERROR_CHAR : . ;