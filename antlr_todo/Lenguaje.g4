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
//  cada tipo usa su propia expresión para validar que el valor corresponde al tipo declarado
declaracion 
    : ONTIE ID IGUAL expr_entera PUNTOCOMA   // ontie solo acepta enteros
    | FLOTE ID IGUAL expr_decimal PUNTOCOMA  // flote acepta enteros o decimales
    | DUBLE ID IGUAL expr_decimal PUNTOCOMA  // duble acepta enteros o decimales
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
    : <assoc=left> expr OP expr
    | INT
    | FLOAT_LIT
    | ID
    ;

// No permite FLOAT_LIT — si se intenta asignar un decimal a ontie, será un error sintáctico
expr_entera
    : <assoc=left> expr_entera OP expr_entera
    | INT
    | ID
    ;

// Permite tanto INT como FLOAT_LIT
expr_decimal
    : <assoc=left> expr_decimal OP expr_decimal
    | FLOAT_LIT
    | INT
    | ID
    ;

// Tipos de datos del lenguaje
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
IGUAL      : 'iyal';
PUNTOCOMA  : 'puavir';
PARENTESIS_ABIERTO : 'pasuvert';
PARENTESIS_CERRADO : 'pasferme';
LLAVE_ABIERTA : 'cleuvert';
LLAVE_CERRADA : 'cleferme';

// TOKENS
//  Operadores
OP : 'plu' | 'moan' | 'par' | 'bag' | 'minog' | 'aye' | 'compag' ;
//      +     -        *       /       <         >       ==   
//  Identificadores
ID  : [a-zA-Z_][a-zA-Z_0-9]*;

//  Numeros enteros
INT : [0-9]+;

// token para números decimales/flotantes (ej: 3.14, 0.5, 2.0)
// Se define ANTES de INT para que ANTLR lo reconozca con mayor prioridad cuando hay punto decimal
FLOAT_LIT : [0-9]+ '.' [0-9]+;

// IGNORAR ESPACIOS
WS : [ \t\r\n]+ -> skip;

//Comentario de bloque
COMMENT: 'lementer' .*? 'blomenter' -> channel(HIDDEN) ;

//Comentario de linea
LINE_COMMENT: 'comenter' ~[\r\n]* -> channel(HIDDEN) ;

// ERROR (SIEMPRE AL FINAL)
ERROR_CHAR : . ;
