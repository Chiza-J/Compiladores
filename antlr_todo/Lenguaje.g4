grammar Lenguaje;

//     PARSER
// Programa base
programa
    : funcion_def* PRINCIPAL PARENTESIS_ABIERTO PARENTESIS_CERRADO bloque EOF
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
    | entrada
    | condicion_if
    | ciclo_while
    | ciclo_fer_pendan
    | ciclo_pur
    | condicion_switch
    | sentencia_pos
    | sentencia_contine
    | sentencia_su
    | llamada_funcion_stmt
    | retorno
    | errorInstr
    ;

// ── DECLARACION ──────────────────────────────────────────────
// ontie x iyal 10 puavir
declaracion
    : ONTIE ID IGUAL expr_entera  PUNTOCOMA
    | FLOTE ID IGUAL expr_decimal PUNTOCOMA
    | DUBLE ID IGUAL expr_decimal PUNTOCOMA
    | SHEN  ID IGUAL expr_string  PUNTOCOMA
    ;

// ── ASIGNACION ───────────────────────────────────────────────
// x iyal expr puavir
asignacion
    : ID IGUAL expr PUNTOCOMA
    ;

// ── IMPRESION ────────────────────────────────────────────────
// amprimi(expr) puavir
impresion
    : AMPRIMI PARENTESIS_ABIERTO expr PARENTESIS_CERRADO PUNTOCOMA
    ;

// ── ENTRADA DE DATOS ─────────────────────────────────────────
// lirf(x) puavir
entrada
    : LIRF PARENTESIS_ABIERTO ID PARENTESIS_CERRADO PUNTOCOMA
    ;

// ── IF / ELSE ────────────────────────────────────────────────
condicion_if
    : WI PARENTESIS_ABIERTO expr PARENTESIS_CERRADO bloque
      (OTRE bloque)?
    ;

// ── WHILE ────────────────────────────────────────────────────
// pendan(expr) { }
ciclo_while
    : PENDAN PARENTESIS_ABIERTO expr PARENTESIS_CERRADO bloque
    ;

// ── DO-WHILE ─────────────────────────────────────────────────
// fer_pendan { } pendan(expr) puavir
ciclo_fer_pendan
    : FER_PENDAN bloque PENDAN PARENTESIS_ABIERTO expr PARENTESIS_CERRADO PUNTOCOMA
    ;

// ── FOR ──────────────────────────────────────────────────────
// pur(init puavir cond puavir step) { }
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

// ── SWITCH ───────────────────────────────────────────────────
// shangshe(expr) { ca 1 { } ca 2 { } difu { } }
condicion_switch
    : SHANGSHE PARENTESIS_ABIERTO expr PARENTESIS_CERRADO
      LLAVE_ABIERTA
        caso_switch*
        caso_default?
      LLAVE_CERRADA
    ;

caso_switch
    : CA INT LLAVE_ABIERTA instrucciones LLAVE_CERRADA
    ;

caso_default
    : DIFU LLAVE_ABIERTA instrucciones LLAVE_CERRADA
    ;

// ── BREAK ────────────────────────────────────────────────────
sentencia_pos
    : POS PUNTOCOMA
    ;

// ── CONTINUE ─────────────────────────────────────────────────
sentencia_contine
    : CONTINE PUNTOCOMA
    ;

// ── GOTO ─────────────────────────────────────────────────────
sentencia_su
    : SU ID PUNTOCOMA
    ;

// ── RETURN ───────────────────────────────────────────────────
retorno
    : RETUR expr? PUNTOCOMA
    ;

// ── FUNCIONES ────────────────────────────────────────────────
// funcion ontie suma pasuvert ontie a puavir ontie b pasferme { retur a plu b puavir }
// funcion vid saludar pasuvert pasferme { amprimi("hola") puavir }
funcion_def
    : FUNCION tipo_retorno ID
        PARENTESIS_ABIERTO parametros PARENTESIS_CERRADO
        bloque
    ;

tipo_retorno
    : ONTIE | FLOTE | DUBLE | SHEN | VID
    ;

// parametros separados por puavir
parametros
    : (parametro (PUNTOCOMA parametro)*)?
    ;

parametro
    : ONTIE ID
    | FLOTE ID
    | DUBLE ID
    | SHEN  ID
    ;

// llamada a funcion como expresion: suma pasuvert 1 puavir 2 pasferme
llamada_funcion
    : ID PARENTESIS_ABIERTO argumentos PARENTESIS_CERRADO
    ;

argumentos
    : (expr (PUNTOCOMA expr)*)?
    ;

// llamada a funcion como instruccion (procedimiento)
llamada_funcion_stmt
    : llamada_funcion PUNTOCOMA
    ;

// ── EXPRESIONES ──────────────────────────────────────────────
expr
    : <assoc=left> expr OP expr
    | llamada_funcion
    | INT
    | FLOAT_LIT
    | STRING
    | ID
    ;

// solo enteros
expr_entera
    : <assoc=left> expr_entera OP expr_entera
    | INT
    | ID
    ;

// enteros o decimales
expr_decimal
    : <assoc=left> expr_decimal OP expr_decimal
    | FLOAT_LIT
    | INT
    | ID
    ;

// solo strings
expr_string
    : STRING
    | ID
    ;

// tipos
tipo : ONTIE | FLOTE | DUBLE | SHEN;

// error sintactico
errorInstr : ERROR_CHAR+;


//       LEXER

// palabras reservadas primero
PRINCIPAL   : 'principal';
WI          : 'wi';
OTRE        : 'otre';
PENDAN      : 'pendan';
FER_PENDAN  : 'fer_pendan';
PUR         : 'pur';
SHANGSHE    : 'shangshe';
CA          : 'ca';
DIFU        : 'difu';
POS         : 'pos';
CONTINE     : 'contine';
SU          : 'su';
RETUR       : 'retur';
FUNCION     : 'funcion';
VID         : 'vid';
LIRF        : 'lirf';

// tipos
ONTIE : 'ontie';
FLOTE : 'flote';
DUBLE : 'duble';
SHEN  : 'shen';

// funciones built-in
AMPRIMI : 'amprimi';

// simbolos
IGUAL              : 'iyal';
PUNTOCOMA          : 'puavir';
PARENTESIS_ABIERTO : 'pasuvert';
PARENTESIS_CERRADO : 'pasferme';
LLAVE_ABIERTA      : 'cleuvert';
LLAVE_CERRADA      : 'cleferme';

// operadores
OP : 'plu' | 'moan' | 'par' | 'bag' | 'minog' | 'aye' | 'compag';

// literales
ID        : [a-zA-Z_][a-zA-Z_0-9]*;
FLOAT_LIT : [0-9]+ '.' [0-9]+;
INT       : [0-9]+;
STRING    : '"' ~["\r\n]* '"';

// ignorar espacios
WS           : [ \t\r\n]+                 -> skip;
COMMENT      : 'lementer' .*? 'blomenter' -> channel(HIDDEN);
LINE_COMMENT : 'comenter' ~[\r\n]*        -> channel(HIDDEN);

// siempre al final
ERROR_CHAR : .;
