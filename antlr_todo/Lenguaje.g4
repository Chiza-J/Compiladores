grammar Lenguaje;

//     PARSER
// Programa base que genera toda la lista de instrucciones 
programa 
    : PRINCIPAL PARENTESIS_ABIERTO PARENTESIS_CERRADO bloque EOF
    ;

//  Bloque {....}
bloque
    : LLAVE_ABIERTA instrucciones LLAVE_CERRADA
    ;

// Lista de instrucciones
instrucciones 
    : (instruccion)*
    ;

//  Tipos de instrucciones
instruccion
    : declaracion
    | asignacion
    | impresion
    | condicion_if
    | ciclo_while
    | retorno
    | errorInstr
    ;


//  Declaracion de variables 
//  int x = 10;
declaracion 
    : VARIABLI tipo ID IGUAL INT PUNTOCOMA
    ;

impresion : AMPRIMI ID PUNTOCOMA;

tipo : ONTIE | FLOTE | DUBLE;

// Manejo de error
errorInstr : ERROR_CHAR+;

//       LEXER 

// PALABRAS RESERVADAS (PRIMERO)

// marcar inicio del programa
PRINCIPAL : 'principal';

//  if
WI : 'wi';

//  else
OTRE : 'otre';

//  while
PENDAN : 'pendan';

//  return
RETUR : 'retur';

//          Tipos
ONTIE    : 'ontie'; // enteros
FLOTE    : 'flote'; //flotantes
DUBLE    : 'duble'; //decimales

//      Funiones
AMPRIMI  : 'amprimi'; //print

// SÍMBOLOS (IMPORTANTE)
IGUAL      : '=';
PUNTOCOMA  : ';';
PARENTESIS_ABIERTO : '(';
PARENTESIS_CERRADO : ')';
LLAVE_ABIERTA : '{';
LLAVE_CERRADA : '}';

// TOKENS
//  Operadores
OP : '+' | '-' | '*' | '/' | '<' | '>' | '==' ;

//  Identificadores
ID  : [a-zA-Z_][a-zA-Z_0-9]*;

//  Numeros
INT : [0-9]+;

// IGNORAR ESPACIOS
WS : [ \t\r\n]+ -> skip;

// ERROR (SIEMPRE AL FINAL)
ERROR_CHAR : . ;