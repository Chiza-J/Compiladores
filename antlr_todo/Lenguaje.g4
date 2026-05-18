grammar Lenguaje;

//     PARSER
// Programa base
programa
    : PRINCIPAL PARENTESIS_ABIERTO PARENTESIS_CERRADO bloque EOF
    ;

// Bloque {....}
bloque
    : LLAVE_ABIERTA instrucciones LLAVE_CERRADA
    ;

// Lista de instrucciones
instrucciones
    : (instruccion)*
    ;

// Tipos de instrucciones
instruccion
    : declaracion
    | asignacion
    | impresion
    | condicion_if
    | ciclo_while
    | ciclo_fer_pendan
    | ciclo_pur
    | llamada_funcion_stmt
    | retorno
    | errorInstr
    ;

// Declaracion de variables
declaracion
    : ONTIE ID IGUAL expr_entera  PUNTOCOMA
    | FLOTE ID IGUAL expr_decimal PUNTOCOMA
    | DUBLE ID IGUAL expr_decimal PUNTOCOMA
    | SHEN  ID IGUAL expr_string  PUNTOCOMA
    ;

// Asignacion
asignacion
    : ID IGUAL expr PUNTOCOMA
    ;

// Print  amprimi(expr) puavir
impresion
    : AMPRIMI PARENTESIS_ABIERTO expr PARENTESIS_CERRADO PUNTOCOMA
    ;

// if / else
condicion_if
    : WI PARENTESIS_ABIERTO expr PARENTESIS_CERRADO bloque
      (OTRE bloque)?
    ;

// while  pendan(expr) { }
ciclo_while
    : PENDAN PARENTESIS_ABIERTO expr PARENTESIS_CERRADO bloque
    ;

// do-while  fer_pendan { } pendan(expr) puavir
ciclo_fer_pendan
    : FER_PENDAN bloque PENDAN PARENTESIS_ABIERTO expr PARENTESIS_CERRADO PUNTOCOMA
    ;

// for  pur(init puavir cond puavir step) { }
ciclo_pur
    : PUR PARENTESIS_ABIERTO
        pur_init PUNTOCOMA
        expr     PUNTOCOMA
        pur_step
      PARENTESIS_CERRADO bloque
    ;

// inicializacion del for sin puavir final
pur_init
    : ONTIE ID IGUAL expr_entera
    | FLOTE ID IGUAL expr_decimal
    | DUBLE ID IGUAL expr_decimal
    | SHEN  ID IGUAL expr_string
    | ID    IGUAL   expr
    ;

// incremento del for sin puavir final
pur_step
    : ID IGUAL expr
    ;

// return
retorno
    : RETUR expr? PUNTOCOMA
    ;

// Definicion de funcion
// funcion ontie suma pasuvert ontie a puavir ontie b pasferme cleuvert retur a plu b puavir cleferme
// funcion vacio saludar pasuvert pasferme cleuvert amprimi pasuvert "hola" pasferme puavir cleferme
funcion_def
    : FUNCION tipo_retorno ID
        PARENTESIS_ABIERTO parametros PARENTESIS_CERRADO
        bloque
    ;

tipo_retorno
    : ONTIE | FLOTE | DUBLE | SHEN | VACIO
    ;

// Parametros separados por puavir
parametros
    : (parametro (PUNTOCOMA parametro)*)?
    ;

parametro
    : ONTIE ID
    | FLOTE ID
    | DUBLE ID
    | SHEN  ID
    ;

// Llamada a funcion como expresion: suma pasuvert 1 puavir 2 pasferme
llamada_funcion
    : ID PARENTESIS_ABIERTO argumentos PARENTESIS_CERRADO
    ;

argumentos
    : (expr (PUNTOCOMA expr)*)?
    ;

// Llamada a funcion como instruccion (procedimiento)
llamada_funcion_stmt
    : llamada_funcion PUNTOCOMA
    ;

// Expresiones generales
expr
    : <assoc=left> expr OP expr
    | llamada_funcion
    | INT
    | FLOAT_LIT
    | STRING
    | ID
    ;

// Solo enteros
expr_entera
    : <assoc=left> expr_entera OP expr_entera
    | INT
    | ID
    ;

// Enteros o decimales
expr_decimal
    : <assoc=left> expr_decimal OP expr_decimal
    | FLOAT_LIT
    | INT
    | ID
    ;

// Solo strings
expr_string
    : STRING
    | ID
    ;

// Tipos
tipo : ONTIE | FLOTE | DUBLE | SHEN;

// Error sintactico
errorInstr : ERROR_CHAR+;


//       LEXER

PRINCIPAL  : 'principal';
WI         : 'wi';
OTRE       : 'otre';
PENDAN     : 'pendan';
FER_PENDAN : 'fer_pendan';
PUR        : 'pur';
RETUR      : 'retur';
FUNCION    : 'funcion';
VACIO      : 'vacio';

ONTIE : 'ontie';
FLOTE : 'flote';
DUBLE : 'duble';
SHEN  : 'shen';

AMPRIMI : 'amprimi';

IGUAL              : 'iyal';
PUNTOCOMA          : 'puavir';
PARENTESIS_ABIERTO : 'pasuvert';
PARENTESIS_CERRADO : 'pasferme';
LLAVE_ABIERTA      : 'cleuvert';
LLAVE_CERRADA      : 'cleferme';

OP : 'plu' | 'moan' | 'par' | 'bag' | 'minog' | 'aye' | 'compag';

ID        : [a-zA-Z_][a-zA-Z_0-9]*;
FLOAT_LIT : [0-9]+ '.' [0-9]+;
INT       : [0-9]+;
STRING    : '"' ~["\r\n]* '"';

WS           : [ \t\r\n]+                 -> skip;
COMMENT      : 'lementer' .*? 'blomenter' -> channel(HIDDEN);
LINE_COMMENT : 'comenter' ~[\r\n]*        -> channel(HIDDEN);

ERROR_CHAR : .;
