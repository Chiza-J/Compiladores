# Generated from Lenguaje.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,25,167,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,2,
        5,2,44,8,2,10,2,12,2,47,9,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,56,8,
        3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,82,8,4,1,5,1,5,1,5,1,5,1,5,
        1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,102,8,7,
        1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,3,9,112,8,9,1,9,1,9,1,10,1,10,1,
        10,1,10,1,10,3,10,121,8,10,1,10,1,10,1,10,5,10,126,8,10,10,10,12,
        10,129,9,10,1,11,1,11,1,11,3,11,134,8,11,1,11,1,11,1,11,5,11,139,
        8,11,10,11,12,11,142,9,11,1,12,1,12,1,12,1,12,3,12,148,8,12,1,12,
        1,12,1,12,5,12,153,8,12,10,12,12,12,156,9,12,1,13,1,13,1,14,1,14,
        1,15,4,15,163,8,15,11,15,12,15,164,1,15,0,3,20,22,24,16,0,2,4,6,
        8,10,12,14,16,18,20,22,24,26,28,30,0,2,2,0,18,18,21,21,1,0,6,9,172,
        0,32,1,0,0,0,2,38,1,0,0,0,4,45,1,0,0,0,6,55,1,0,0,0,8,81,1,0,0,0,
        10,83,1,0,0,0,12,88,1,0,0,0,14,94,1,0,0,0,16,103,1,0,0,0,18,109,
        1,0,0,0,20,120,1,0,0,0,22,133,1,0,0,0,24,147,1,0,0,0,26,157,1,0,
        0,0,28,159,1,0,0,0,30,162,1,0,0,0,32,33,5,1,0,0,33,34,5,13,0,0,34,
        35,5,14,0,0,35,36,3,2,1,0,36,37,5,0,0,1,37,1,1,0,0,0,38,39,5,15,
        0,0,39,40,3,4,2,0,40,41,5,16,0,0,41,3,1,0,0,0,42,44,3,6,3,0,43,42,
        1,0,0,0,44,47,1,0,0,0,45,43,1,0,0,0,45,46,1,0,0,0,46,5,1,0,0,0,47,
        45,1,0,0,0,48,56,3,8,4,0,49,56,3,10,5,0,50,56,3,12,6,0,51,56,3,14,
        7,0,52,56,3,16,8,0,53,56,3,18,9,0,54,56,3,30,15,0,55,48,1,0,0,0,
        55,49,1,0,0,0,55,50,1,0,0,0,55,51,1,0,0,0,55,52,1,0,0,0,55,53,1,
        0,0,0,55,54,1,0,0,0,56,7,1,0,0,0,57,58,5,6,0,0,58,59,5,18,0,0,59,
        60,5,11,0,0,60,61,3,22,11,0,61,62,5,12,0,0,62,82,1,0,0,0,63,64,5,
        7,0,0,64,65,5,18,0,0,65,66,5,11,0,0,66,67,3,24,12,0,67,68,5,12,0,
        0,68,82,1,0,0,0,69,70,5,8,0,0,70,71,5,18,0,0,71,72,5,11,0,0,72,73,
        3,24,12,0,73,74,5,12,0,0,74,82,1,0,0,0,75,76,5,9,0,0,76,77,5,18,
        0,0,77,78,5,11,0,0,78,79,3,26,13,0,79,80,5,12,0,0,80,82,1,0,0,0,
        81,57,1,0,0,0,81,63,1,0,0,0,81,69,1,0,0,0,81,75,1,0,0,0,82,9,1,0,
        0,0,83,84,5,18,0,0,84,85,5,11,0,0,85,86,3,20,10,0,86,87,5,12,0,0,
        87,11,1,0,0,0,88,89,5,10,0,0,89,90,5,13,0,0,90,91,3,20,10,0,91,92,
        5,14,0,0,92,93,5,12,0,0,93,13,1,0,0,0,94,95,5,2,0,0,95,96,5,13,0,
        0,96,97,3,20,10,0,97,98,5,14,0,0,98,101,3,2,1,0,99,100,5,3,0,0,100,
        102,3,2,1,0,101,99,1,0,0,0,101,102,1,0,0,0,102,15,1,0,0,0,103,104,
        5,4,0,0,104,105,5,13,0,0,105,106,3,20,10,0,106,107,5,14,0,0,107,
        108,3,2,1,0,108,17,1,0,0,0,109,111,5,5,0,0,110,112,3,20,10,0,111,
        110,1,0,0,0,111,112,1,0,0,0,112,113,1,0,0,0,113,114,5,12,0,0,114,
        19,1,0,0,0,115,116,6,10,-1,0,116,121,5,19,0,0,117,121,5,20,0,0,118,
        121,5,21,0,0,119,121,5,18,0,0,120,115,1,0,0,0,120,117,1,0,0,0,120,
        118,1,0,0,0,120,119,1,0,0,0,121,127,1,0,0,0,122,123,10,5,0,0,123,
        124,5,17,0,0,124,126,3,20,10,6,125,122,1,0,0,0,126,129,1,0,0,0,127,
        125,1,0,0,0,127,128,1,0,0,0,128,21,1,0,0,0,129,127,1,0,0,0,130,131,
        6,11,-1,0,131,134,5,19,0,0,132,134,5,18,0,0,133,130,1,0,0,0,133,
        132,1,0,0,0,134,140,1,0,0,0,135,136,10,3,0,0,136,137,5,17,0,0,137,
        139,3,22,11,4,138,135,1,0,0,0,139,142,1,0,0,0,140,138,1,0,0,0,140,
        141,1,0,0,0,141,23,1,0,0,0,142,140,1,0,0,0,143,144,6,12,-1,0,144,
        148,5,20,0,0,145,148,5,19,0,0,146,148,5,18,0,0,147,143,1,0,0,0,147,
        145,1,0,0,0,147,146,1,0,0,0,148,154,1,0,0,0,149,150,10,4,0,0,150,
        151,5,17,0,0,151,153,3,24,12,5,152,149,1,0,0,0,153,156,1,0,0,0,154,
        152,1,0,0,0,154,155,1,0,0,0,155,25,1,0,0,0,156,154,1,0,0,0,157,158,
        7,0,0,0,158,27,1,0,0,0,159,160,7,1,0,0,160,29,1,0,0,0,161,163,5,
        25,0,0,162,161,1,0,0,0,163,164,1,0,0,0,164,162,1,0,0,0,164,165,1,
        0,0,0,165,31,1,0,0,0,12,45,55,81,101,111,120,127,133,140,147,154,
        164
    ]

class LenguajeParser ( Parser ):

    grammarFileName = "Lenguaje.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'principal'", "'wi'", "'otre'", "'pendan'", 
                     "'retur'", "'ontie'", "'flote'", "'duble'", "'shen'", 
                     "'amprimi'", "'iyal'", "'puavir'", "'pasuvert'", "'pasferme'", 
                     "'cleuvert'", "'cleferme'" ]

    symbolicNames = [ "<INVALID>", "PRINCIPAL", "WI", "OTRE", "PENDAN", 
                      "RETUR", "ONTIE", "FLOTE", "DUBLE", "SHEN", "AMPRIMI", 
                      "IGUAL", "PUNTOCOMA", "PARENTESIS_ABIERTO", "PARENTESIS_CERRADO", 
                      "LLAVE_ABIERTA", "LLAVE_CERRADA", "OP", "ID", "INT", 
                      "FLOAT_LIT", "STRING", "WS", "COMMENT", "LINE_COMMENT", 
                      "ERROR_CHAR" ]

    RULE_programa = 0
    RULE_bloque = 1
    RULE_instrucciones = 2
    RULE_instruccion = 3
    RULE_declaracion = 4
    RULE_asignacion = 5
    RULE_impresion = 6
    RULE_condicion_if = 7
    RULE_ciclo_while = 8
    RULE_retorno = 9
    RULE_expr = 10
    RULE_expr_entera = 11
    RULE_expr_decimal = 12
    RULE_expr_string = 13
    RULE_tipo = 14
    RULE_errorInstr = 15

    ruleNames =  [ "programa", "bloque", "instrucciones", "instruccion", 
                   "declaracion", "asignacion", "impresion", "condicion_if", 
                   "ciclo_while", "retorno", "expr", "expr_entera", "expr_decimal", 
                   "expr_string", "tipo", "errorInstr" ]

    EOF = Token.EOF
    PRINCIPAL=1
    WI=2
    OTRE=3
    PENDAN=4
    RETUR=5
    ONTIE=6
    FLOTE=7
    DUBLE=8
    SHEN=9
    AMPRIMI=10
    IGUAL=11
    PUNTOCOMA=12
    PARENTESIS_ABIERTO=13
    PARENTESIS_CERRADO=14
    LLAVE_ABIERTA=15
    LLAVE_CERRADA=16
    OP=17
    ID=18
    INT=19
    FLOAT_LIT=20
    STRING=21
    WS=22
    COMMENT=23
    LINE_COMMENT=24
    ERROR_CHAR=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINCIPAL(self):
            return self.getToken(LenguajeParser.PRINCIPAL, 0)

        def PARENTESIS_ABIERTO(self):
            return self.getToken(LenguajeParser.PARENTESIS_ABIERTO, 0)

        def PARENTESIS_CERRADO(self):
            return self.getToken(LenguajeParser.PARENTESIS_CERRADO, 0)

        def bloque(self):
            return self.getTypedRuleContext(LenguajeParser.BloqueContext,0)


        def EOF(self):
            return self.getToken(LenguajeParser.EOF, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_programa

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrograma" ):
                listener.enterPrograma(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrograma" ):
                listener.exitPrograma(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrograma" ):
                return visitor.visitPrograma(self)
            else:
                return visitor.visitChildren(self)




    def programa(self):

        localctx = LenguajeParser.ProgramaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_programa)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(LenguajeParser.PRINCIPAL)
            self.state = 33
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 34
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 35
            self.bloque()
            self.state = 36
            self.match(LenguajeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BloqueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LLAVE_ABIERTA(self):
            return self.getToken(LenguajeParser.LLAVE_ABIERTA, 0)

        def instrucciones(self):
            return self.getTypedRuleContext(LenguajeParser.InstruccionesContext,0)


        def LLAVE_CERRADA(self):
            return self.getToken(LenguajeParser.LLAVE_CERRADA, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_bloque

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBloque" ):
                listener.enterBloque(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBloque" ):
                listener.exitBloque(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBloque" ):
                return visitor.visitBloque(self)
            else:
                return visitor.visitChildren(self)




    def bloque(self):

        localctx = LenguajeParser.BloqueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_bloque)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(LenguajeParser.LLAVE_ABIERTA)
            self.state = 39
            self.instrucciones()
            self.state = 40
            self.match(LenguajeParser.LLAVE_CERRADA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstruccionesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def instruccion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LenguajeParser.InstruccionContext)
            else:
                return self.getTypedRuleContext(LenguajeParser.InstruccionContext,i)


        def getRuleIndex(self):
            return LenguajeParser.RULE_instrucciones

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInstrucciones" ):
                listener.enterInstrucciones(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInstrucciones" ):
                listener.exitInstrucciones(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstrucciones" ):
                return visitor.visitInstrucciones(self)
            else:
                return visitor.visitChildren(self)




    def instrucciones(self):

        localctx = LenguajeParser.InstruccionesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_instrucciones)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 33818612) != 0):
                self.state = 42
                self.instruccion()
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstruccionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaracion(self):
            return self.getTypedRuleContext(LenguajeParser.DeclaracionContext,0)


        def asignacion(self):
            return self.getTypedRuleContext(LenguajeParser.AsignacionContext,0)


        def impresion(self):
            return self.getTypedRuleContext(LenguajeParser.ImpresionContext,0)


        def condicion_if(self):
            return self.getTypedRuleContext(LenguajeParser.Condicion_ifContext,0)


        def ciclo_while(self):
            return self.getTypedRuleContext(LenguajeParser.Ciclo_whileContext,0)


        def retorno(self):
            return self.getTypedRuleContext(LenguajeParser.RetornoContext,0)


        def errorInstr(self):
            return self.getTypedRuleContext(LenguajeParser.ErrorInstrContext,0)


        def getRuleIndex(self):
            return LenguajeParser.RULE_instruccion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInstruccion" ):
                listener.enterInstruccion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInstruccion" ):
                listener.exitInstruccion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstruccion" ):
                return visitor.visitInstruccion(self)
            else:
                return visitor.visitChildren(self)




    def instruccion(self):

        localctx = LenguajeParser.InstruccionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_instruccion)
        try:
            self.state = 55
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6, 7, 8, 9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 48
                self.declaracion()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 49
                self.asignacion()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 3)
                self.state = 50
                self.impresion()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 4)
                self.state = 51
                self.condicion_if()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 5)
                self.state = 52
                self.ciclo_while()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 6)
                self.state = 53
                self.retorno()
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 7)
                self.state = 54
                self.errorInstr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclaracionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ONTIE(self):
            return self.getToken(LenguajeParser.ONTIE, 0)

        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

        def IGUAL(self):
            return self.getToken(LenguajeParser.IGUAL, 0)

        def expr_entera(self):
            return self.getTypedRuleContext(LenguajeParser.Expr_enteraContext,0)


        def PUNTOCOMA(self):
            return self.getToken(LenguajeParser.PUNTOCOMA, 0)

        def FLOTE(self):
            return self.getToken(LenguajeParser.FLOTE, 0)

        def expr_decimal(self):
            return self.getTypedRuleContext(LenguajeParser.Expr_decimalContext,0)


        def DUBLE(self):
            return self.getToken(LenguajeParser.DUBLE, 0)

        def SHEN(self):
            return self.getToken(LenguajeParser.SHEN, 0)

        def expr_string(self):
            return self.getTypedRuleContext(LenguajeParser.Expr_stringContext,0)


        def getRuleIndex(self):
            return LenguajeParser.RULE_declaracion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaracion" ):
                listener.enterDeclaracion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaracion" ):
                listener.exitDeclaracion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaracion" ):
                return visitor.visitDeclaracion(self)
            else:
                return visitor.visitChildren(self)




    def declaracion(self):

        localctx = LenguajeParser.DeclaracionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_declaracion)
        try:
            self.state = 81
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(LenguajeParser.ONTIE)
                self.state = 58
                self.match(LenguajeParser.ID)
                self.state = 59
                self.match(LenguajeParser.IGUAL)
                self.state = 60
                self.expr_entera(0)
                self.state = 61
                self.match(LenguajeParser.PUNTOCOMA)
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                self.match(LenguajeParser.FLOTE)
                self.state = 64
                self.match(LenguajeParser.ID)
                self.state = 65
                self.match(LenguajeParser.IGUAL)
                self.state = 66
                self.expr_decimal(0)
                self.state = 67
                self.match(LenguajeParser.PUNTOCOMA)
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 3)
                self.state = 69
                self.match(LenguajeParser.DUBLE)
                self.state = 70
                self.match(LenguajeParser.ID)
                self.state = 71
                self.match(LenguajeParser.IGUAL)
                self.state = 72
                self.expr_decimal(0)
                self.state = 73
                self.match(LenguajeParser.PUNTOCOMA)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 4)
                self.state = 75
                self.match(LenguajeParser.SHEN)
                self.state = 76
                self.match(LenguajeParser.ID)
                self.state = 77
                self.match(LenguajeParser.IGUAL)
                self.state = 78
                self.expr_string()
                self.state = 79
                self.match(LenguajeParser.PUNTOCOMA)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AsignacionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

        def IGUAL(self):
            return self.getToken(LenguajeParser.IGUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(LenguajeParser.ExprContext,0)


        def PUNTOCOMA(self):
            return self.getToken(LenguajeParser.PUNTOCOMA, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_asignacion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAsignacion" ):
                listener.enterAsignacion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAsignacion" ):
                listener.exitAsignacion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAsignacion" ):
                return visitor.visitAsignacion(self)
            else:
                return visitor.visitChildren(self)




    def asignacion(self):

        localctx = LenguajeParser.AsignacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_asignacion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(LenguajeParser.ID)
            self.state = 84
            self.match(LenguajeParser.IGUAL)
            self.state = 85
            self.expr(0)
            self.state = 86
            self.match(LenguajeParser.PUNTOCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImpresionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AMPRIMI(self):
            return self.getToken(LenguajeParser.AMPRIMI, 0)

        def PARENTESIS_ABIERTO(self):
            return self.getToken(LenguajeParser.PARENTESIS_ABIERTO, 0)

        def expr(self):
            return self.getTypedRuleContext(LenguajeParser.ExprContext,0)


        def PARENTESIS_CERRADO(self):
            return self.getToken(LenguajeParser.PARENTESIS_CERRADO, 0)

        def PUNTOCOMA(self):
            return self.getToken(LenguajeParser.PUNTOCOMA, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_impresion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImpresion" ):
                listener.enterImpresion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImpresion" ):
                listener.exitImpresion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImpresion" ):
                return visitor.visitImpresion(self)
            else:
                return visitor.visitChildren(self)




    def impresion(self):

        localctx = LenguajeParser.ImpresionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_impresion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(LenguajeParser.AMPRIMI)
            self.state = 89
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 90
            self.expr(0)
            self.state = 91
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 92
            self.match(LenguajeParser.PUNTOCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Condicion_ifContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WI(self):
            return self.getToken(LenguajeParser.WI, 0)

        def PARENTESIS_ABIERTO(self):
            return self.getToken(LenguajeParser.PARENTESIS_ABIERTO, 0)

        def expr(self):
            return self.getTypedRuleContext(LenguajeParser.ExprContext,0)


        def PARENTESIS_CERRADO(self):
            return self.getToken(LenguajeParser.PARENTESIS_CERRADO, 0)

        def bloque(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LenguajeParser.BloqueContext)
            else:
                return self.getTypedRuleContext(LenguajeParser.BloqueContext,i)


        def OTRE(self):
            return self.getToken(LenguajeParser.OTRE, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_condicion_if

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondicion_if" ):
                listener.enterCondicion_if(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondicion_if" ):
                listener.exitCondicion_if(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondicion_if" ):
                return visitor.visitCondicion_if(self)
            else:
                return visitor.visitChildren(self)




    def condicion_if(self):

        localctx = LenguajeParser.Condicion_ifContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_condicion_if)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(LenguajeParser.WI)
            self.state = 95
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 96
            self.expr(0)
            self.state = 97
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 98
            self.bloque()
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 99
                self.match(LenguajeParser.OTRE)
                self.state = 100
                self.bloque()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ciclo_whileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PENDAN(self):
            return self.getToken(LenguajeParser.PENDAN, 0)

        def PARENTESIS_ABIERTO(self):
            return self.getToken(LenguajeParser.PARENTESIS_ABIERTO, 0)

        def expr(self):
            return self.getTypedRuleContext(LenguajeParser.ExprContext,0)


        def PARENTESIS_CERRADO(self):
            return self.getToken(LenguajeParser.PARENTESIS_CERRADO, 0)

        def bloque(self):
            return self.getTypedRuleContext(LenguajeParser.BloqueContext,0)


        def getRuleIndex(self):
            return LenguajeParser.RULE_ciclo_while

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCiclo_while" ):
                listener.enterCiclo_while(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCiclo_while" ):
                listener.exitCiclo_while(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCiclo_while" ):
                return visitor.visitCiclo_while(self)
            else:
                return visitor.visitChildren(self)




    def ciclo_while(self):

        localctx = LenguajeParser.Ciclo_whileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_ciclo_while)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.match(LenguajeParser.PENDAN)
            self.state = 104
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 105
            self.expr(0)
            self.state = 106
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 107
            self.bloque()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RetornoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETUR(self):
            return self.getToken(LenguajeParser.RETUR, 0)

        def PUNTOCOMA(self):
            return self.getToken(LenguajeParser.PUNTOCOMA, 0)

        def expr(self):
            return self.getTypedRuleContext(LenguajeParser.ExprContext,0)


        def getRuleIndex(self):
            return LenguajeParser.RULE_retorno

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRetorno" ):
                listener.enterRetorno(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRetorno" ):
                listener.exitRetorno(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRetorno" ):
                return visitor.visitRetorno(self)
            else:
                return visitor.visitChildren(self)




    def retorno(self):

        localctx = LenguajeParser.RetornoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_retorno)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            self.match(LenguajeParser.RETUR)
            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3932160) != 0):
                self.state = 110
                self.expr(0)


            self.state = 113
            self.match(LenguajeParser.PUNTOCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(LenguajeParser.INT, 0)

        def FLOAT_LIT(self):
            return self.getToken(LenguajeParser.FLOAT_LIT, 0)

        def STRING(self):
            return self.getToken(LenguajeParser.STRING, 0)

        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LenguajeParser.ExprContext)
            else:
                return self.getTypedRuleContext(LenguajeParser.ExprContext,i)


        def OP(self):
            return self.getToken(LenguajeParser.OP, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LenguajeParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [19]:
                self.state = 116
                self.match(LenguajeParser.INT)
                pass
            elif token in [20]:
                self.state = 117
                self.match(LenguajeParser.FLOAT_LIT)
                pass
            elif token in [21]:
                self.state = 118
                self.match(LenguajeParser.STRING)
                pass
            elif token in [18]:
                self.state = 119
                self.match(LenguajeParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 127
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LenguajeParser.ExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                    self.state = 122
                    if not self.precpred(self._ctx, 5):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                    self.state = 123
                    self.match(LenguajeParser.OP)
                    self.state = 124
                    self.expr(6) 
                self.state = 129
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Expr_enteraContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(LenguajeParser.INT, 0)

        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

        def expr_entera(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LenguajeParser.Expr_enteraContext)
            else:
                return self.getTypedRuleContext(LenguajeParser.Expr_enteraContext,i)


        def OP(self):
            return self.getToken(LenguajeParser.OP, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_expr_entera

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr_entera" ):
                listener.enterExpr_entera(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr_entera" ):
                listener.exitExpr_entera(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr_entera" ):
                return visitor.visitExpr_entera(self)
            else:
                return visitor.visitChildren(self)



    def expr_entera(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LenguajeParser.Expr_enteraContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_expr_entera, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [19]:
                self.state = 131
                self.match(LenguajeParser.INT)
                pass
            elif token in [18]:
                self.state = 132
                self.match(LenguajeParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 140
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LenguajeParser.Expr_enteraContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr_entera)
                    self.state = 135
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 136
                    self.match(LenguajeParser.OP)
                    self.state = 137
                    self.expr_entera(4) 
                self.state = 142
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Expr_decimalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOAT_LIT(self):
            return self.getToken(LenguajeParser.FLOAT_LIT, 0)

        def INT(self):
            return self.getToken(LenguajeParser.INT, 0)

        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

        def expr_decimal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LenguajeParser.Expr_decimalContext)
            else:
                return self.getTypedRuleContext(LenguajeParser.Expr_decimalContext,i)


        def OP(self):
            return self.getToken(LenguajeParser.OP, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_expr_decimal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr_decimal" ):
                listener.enterExpr_decimal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr_decimal" ):
                listener.exitExpr_decimal(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr_decimal" ):
                return visitor.visitExpr_decimal(self)
            else:
                return visitor.visitChildren(self)



    def expr_decimal(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LenguajeParser.Expr_decimalContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 24
        self.enterRecursionRule(localctx, 24, self.RULE_expr_decimal, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                self.state = 144
                self.match(LenguajeParser.FLOAT_LIT)
                pass
            elif token in [19]:
                self.state = 145
                self.match(LenguajeParser.INT)
                pass
            elif token in [18]:
                self.state = 146
                self.match(LenguajeParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 154
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LenguajeParser.Expr_decimalContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr_decimal)
                    self.state = 149
                    if not self.precpred(self._ctx, 4):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                    self.state = 150
                    self.match(LenguajeParser.OP)
                    self.state = 151
                    self.expr_decimal(5) 
                self.state = 156
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Expr_stringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(LenguajeParser.STRING, 0)

        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_expr_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr_string" ):
                listener.enterExpr_string(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr_string" ):
                listener.exitExpr_string(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr_string" ):
                return visitor.visitExpr_string(self)
            else:
                return visitor.visitChildren(self)




    def expr_string(self):

        localctx = LenguajeParser.Expr_stringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_expr_string)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 157
            _la = self._input.LA(1)
            if not(_la==18 or _la==21):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TipoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ONTIE(self):
            return self.getToken(LenguajeParser.ONTIE, 0)

        def FLOTE(self):
            return self.getToken(LenguajeParser.FLOTE, 0)

        def DUBLE(self):
            return self.getToken(LenguajeParser.DUBLE, 0)

        def SHEN(self):
            return self.getToken(LenguajeParser.SHEN, 0)

        def getRuleIndex(self):
            return LenguajeParser.RULE_tipo

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTipo" ):
                listener.enterTipo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTipo" ):
                listener.exitTipo(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTipo" ):
                return visitor.visitTipo(self)
            else:
                return visitor.visitChildren(self)




    def tipo(self):

        localctx = LenguajeParser.TipoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_tipo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 960) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ErrorInstrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ERROR_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(LenguajeParser.ERROR_CHAR)
            else:
                return self.getToken(LenguajeParser.ERROR_CHAR, i)

        def getRuleIndex(self):
            return LenguajeParser.RULE_errorInstr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterErrorInstr" ):
                listener.enterErrorInstr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitErrorInstr" ):
                listener.exitErrorInstr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitErrorInstr" ):
                return visitor.visitErrorInstr(self)
            else:
                return visitor.visitChildren(self)




    def errorInstr(self):

        localctx = LenguajeParser.ErrorInstrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_errorInstr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 161
                    self.match(LenguajeParser.ERROR_CHAR)

                else:
                    raise NoViableAltException(self)
                self.state = 164 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[10] = self.expr_sempred
        self._predicates[11] = self.expr_entera_sempred
        self._predicates[12] = self.expr_decimal_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 5)
         

    def expr_entera_sempred(self, localctx:Expr_enteraContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

    def expr_decimal_sempred(self, localctx:Expr_decimalContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         




