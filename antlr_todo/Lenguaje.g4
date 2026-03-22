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
    : tipo ID IGUAL expr PUNTOCOMA
    ;

//  Asignacion x = 5;
asignacion
    : ID IGUAL expr PUNTOCOMA
    ;

//  Print y en C es printf(x);
impresion
    : AMPRIMI PARENTESIS_ABIERTO expr PARENTESIS_CERRADO PUNTOCOMA
    ;

//  if
// if (cond) {} else {}
condicion_if
    : WI PARENTESIS_ABIERTO expr PARENTESIS_CERRADO bloque 
     (OTRE bloque)?
    ;

//  while 
//  while (cond) { }
ciclo_while
    : PENDAN PARENTESIS_ABIERTO expr PARENTESIS_CERRADO bloque
    ;

// return
// return x;
retorno
    : RETUR expr? PUNTOCOMA
    ;


// Expresiones básicas
expr
    : expr OP expr
    | INT
    | ID
    ;


tipo : ONTIE | FLOTE | DUBLE;

// Manejo de error sintactico
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