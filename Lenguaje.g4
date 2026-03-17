grammar Lenguaje;

// ===== PARSER =====
programa : instrucciones EOF;

instrucciones : (instruccion)*;

instruccion
    : declaracion
    | impresion
    | ERROR_CHAR+   // manejo de errores
    ;

declaracion : VARIABLI tipo ID '=' INT ';';

impresion : AMPRIMI ID ';';

tipo : ONTIE | FLOTE | DUBLE;

// ===== LEXER =====

// Palabras reservadas (TU abecedario)
VARIABLI : 'variabli';
ONTIE    : 'ontie';
FLOTE    : 'flote';
DUBLE    : 'duble';
AMPRIMI  : 'amprimi';

// Tokens básicos
ID  : [a-zA-Z_][a-zA-Z_0-9]*;
INT : [0-9]+;

// Ignorar espacios
WS : [ \t\r\n]+ -> skip;

// Error léxico
ERROR_CHAR : . ;