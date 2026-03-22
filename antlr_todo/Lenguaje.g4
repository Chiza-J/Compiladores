grammar Lenguaje;

//     PARSER
// Programa base que genera toda la lista de instrucciones 
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

//       LEXER 

// PALABRAS RESERVADAS (PRIMERO)

// marcar inicio del programa
PRINCIPAL : 'principal';


VARIABLI : 'variabli'; // variables
ONTIE    : 'ontie'; // enteros
FLOTE    : 'flote'; //flotantes
DUBLE    : 'duble'; //decimales
AMPRIMI  : 'amprimi'; //print

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