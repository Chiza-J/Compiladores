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
        4,1,23,156,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,2,5,2,42,8,2,
        10,2,12,2,45,9,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,54,8,3,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        3,4,74,8,4,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,
        7,1,7,1,7,1,7,1,7,3,7,94,8,7,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,3,9,
        104,8,9,1,9,1,9,1,10,1,10,1,10,1,10,3,10,112,8,10,1,10,1,10,1,10,
        5,10,117,8,10,10,10,12,10,120,9,10,1,11,1,11,1,11,3,11,125,8,11,
        1,11,1,11,1,11,5,11,130,8,11,10,11,12,11,133,9,11,1,12,1,12,1,12,
        1,12,3,12,139,8,12,1,12,1,12,1,12,5,12,144,8,12,10,12,12,12,147,
        9,12,1,13,1,13,1,14,4,14,152,8,14,11,14,12,14,153,1,14,0,3,20,22,
        24,15,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,0,1,1,0,6,8,160,0,
        30,1,0,0,0,2,36,1,0,0,0,4,43,1,0,0,0,6,53,1,0,0,0,8,73,1,0,0,0,10,
        75,1,0,0,0,12,80,1,0,0,0,14,86,1,0,0,0,16,95,1,0,0,0,18,101,1,0,
        0,0,20,111,1,0,0,0,22,124,1,0,0,0,24,138,1,0,0,0,26,148,1,0,0,0,
        28,151,1,0,0,0,30,31,5,1,0,0,31,32,5,12,0,0,32,33,5,13,0,0,33,34,
        3,2,1,0,34,35,5,0,0,1,35,1,1,0,0,0,36,37,5,14,0,0,37,38,3,4,2,0,
        38,39,5,15,0,0,39,3,1,0,0,0,40,42,3,6,3,0,41,40,1,0,0,0,42,45,1,
        0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,44,5,1,0,0,0,45,43,1,0,0,0,46,
        54,3,8,4,0,47,54,3,10,5,0,48,54,3,12,6,0,49,54,3,14,7,0,50,54,3,
        16,8,0,51,54,3,18,9,0,52,54,3,28,14,0,53,46,1,0,0,0,53,47,1,0,0,
        0,53,48,1,0,0,0,53,49,1,0,0,0,53,50,1,0,0,0,53,51,1,0,0,0,53,52,
        1,0,0,0,54,7,1,0,0,0,55,56,5,6,0,0,56,57,5,17,0,0,57,58,5,10,0,0,
        58,59,3,22,11,0,59,60,5,11,0,0,60,74,1,0,0,0,61,62,5,7,0,0,62,63,
        5,17,0,0,63,64,5,10,0,0,64,65,3,24,12,0,65,66,5,11,0,0,66,74,1,0,
        0,0,67,68,5,8,0,0,68,69,5,17,0,0,69,70,5,10,0,0,70,71,3,24,12,0,
        71,72,5,11,0,0,72,74,1,0,0,0,73,55,1,0,0,0,73,61,1,0,0,0,73,67,1,
        0,0,0,74,9,1,0,0,0,75,76,5,17,0,0,76,77,5,10,0,0,77,78,3,20,10,0,
        78,79,5,11,0,0,79,11,1,0,0,0,80,81,5,9,0,0,81,82,5,12,0,0,82,83,
        3,20,10,0,83,84,5,13,0,0,84,85,5,11,0,0,85,13,1,0,0,0,86,87,5,2,
        0,0,87,88,5,12,0,0,88,89,3,20,10,0,89,90,5,13,0,0,90,93,3,2,1,0,
        91,92,5,3,0,0,92,94,3,2,1,0,93,91,1,0,0,0,93,94,1,0,0,0,94,15,1,
        0,0,0,95,96,5,4,0,0,96,97,5,12,0,0,97,98,3,20,10,0,98,99,5,13,0,
        0,99,100,3,2,1,0,100,17,1,0,0,0,101,103,5,5,0,0,102,104,3,20,10,
        0,103,102,1,0,0,0,103,104,1,0,0,0,104,105,1,0,0,0,105,106,5,11,0,
        0,106,19,1,0,0,0,107,108,6,10,-1,0,108,112,5,18,0,0,109,112,5,19,
        0,0,110,112,5,17,0,0,111,107,1,0,0,0,111,109,1,0,0,0,111,110,1,0,
        0,0,112,118,1,0,0,0,113,114,10,4,0,0,114,115,5,16,0,0,115,117,3,
        20,10,5,116,113,1,0,0,0,117,120,1,0,0,0,118,116,1,0,0,0,118,119,
        1,0,0,0,119,21,1,0,0,0,120,118,1,0,0,0,121,122,6,11,-1,0,122,125,
        5,18,0,0,123,125,5,17,0,0,124,121,1,0,0,0,124,123,1,0,0,0,125,131,
        1,0,0,0,126,127,10,3,0,0,127,128,5,16,0,0,128,130,3,22,11,4,129,
        126,1,0,0,0,130,133,1,0,0,0,131,129,1,0,0,0,131,132,1,0,0,0,132,
        23,1,0,0,0,133,131,1,0,0,0,134,135,6,12,-1,0,135,139,5,19,0,0,136,
        139,5,18,0,0,137,139,5,17,0,0,138,134,1,0,0,0,138,136,1,0,0,0,138,
        137,1,0,0,0,139,145,1,0,0,0,140,141,10,4,0,0,141,142,5,16,0,0,142,
        144,3,24,12,5,143,140,1,0,0,0,144,147,1,0,0,0,145,143,1,0,0,0,145,
        146,1,0,0,0,146,25,1,0,0,0,147,145,1,0,0,0,148,149,7,0,0,0,149,27,
        1,0,0,0,150,152,5,23,0,0,151,150,1,0,0,0,152,153,1,0,0,0,153,151,
        1,0,0,0,153,154,1,0,0,0,154,29,1,0,0,0,12,43,53,73,93,103,111,118,
        124,131,138,145,153
    ]

class LenguajeParser ( Parser ):

    grammarFileName = "Lenguaje.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'principal'", "'wi'", "'otre'", "'pendan'", 
                     "'retur'", "'ontie'", "'flote'", "'duble'", "'amprimi'", 
                     "'='", "';'", "'('", "')'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "PRINCIPAL", "WI", "OTRE", "PENDAN", 
                      "RETUR", "ONTIE", "FLOTE", "DUBLE", "AMPRIMI", "IGUAL", 
                      "PUNTOCOMA", "PARENTESIS_ABIERTO", "PARENTESIS_CERRADO", 
                      "LLAVE_ABIERTA", "LLAVE_CERRADA", "OP", "ID", "INT", 
                      "FLOAT_LIT", "WS", "COMMENT", "LINE_COMMENT", "ERROR_CHAR" ]

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
    RULE_tipo = 13
    RULE_errorInstr = 14

    ruleNames =  [ "programa", "bloque", "instrucciones", "instruccion", 
                   "declaracion", "asignacion", "impresion", "condicion_if", 
                   "ciclo_while", "retorno", "expr", "expr_entera", "expr_decimal", 
                   "tipo", "errorInstr" ]

    EOF = Token.EOF
    PRINCIPAL=1
    WI=2
    OTRE=3
    PENDAN=4
    RETUR=5
    ONTIE=6
    FLOTE=7
    DUBLE=8
    AMPRIMI=9
    IGUAL=10
    PUNTOCOMA=11
    PARENTESIS_ABIERTO=12
    PARENTESIS_CERRADO=13
    LLAVE_ABIERTA=14
    LLAVE_CERRADA=15
    OP=16
    ID=17
    INT=18
    FLOAT_LIT=19
    WS=20
    COMMENT=21
    LINE_COMMENT=22
    ERROR_CHAR=23

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




    def programa(self):

        localctx = LenguajeParser.ProgramaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_programa)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(LenguajeParser.PRINCIPAL)
            self.state = 31
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 32
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 33
            self.bloque()
            self.state = 34
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




    def bloque(self):

        localctx = LenguajeParser.BloqueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_bloque)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(LenguajeParser.LLAVE_ABIERTA)
            self.state = 37
            self.instrucciones()
            self.state = 38
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




    def instrucciones(self):

        localctx = LenguajeParser.InstruccionesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_instrucciones)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8520692) != 0):
                self.state = 40
                self.instruccion()
                self.state = 45
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




    def instruccion(self):

        localctx = LenguajeParser.InstruccionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_instruccion)
        try:
            self.state = 53
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6, 7, 8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 46
                self.declaracion()
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 2)
                self.state = 47
                self.asignacion()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 48
                self.impresion()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 4)
                self.state = 49
                self.condicion_if()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 5)
                self.state = 50
                self.ciclo_while()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 6)
                self.state = 51
                self.retorno()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 7)
                self.state = 52
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

        def getRuleIndex(self):
            return LenguajeParser.RULE_declaracion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaracion" ):
                listener.enterDeclaracion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaracion" ):
                listener.exitDeclaracion(self)




    def declaracion(self):

        localctx = LenguajeParser.DeclaracionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_declaracion)
        try:
            self.state = 73
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 55
                self.match(LenguajeParser.ONTIE)
                self.state = 56
                self.match(LenguajeParser.ID)
                self.state = 57
                self.match(LenguajeParser.IGUAL)
                self.state = 58
                self.expr_entera(0)
                self.state = 59
                self.match(LenguajeParser.PUNTOCOMA)
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 61
                self.match(LenguajeParser.FLOTE)
                self.state = 62
                self.match(LenguajeParser.ID)
                self.state = 63
                self.match(LenguajeParser.IGUAL)
                self.state = 64
                self.expr_decimal(0)
                self.state = 65
                self.match(LenguajeParser.PUNTOCOMA)
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 3)
                self.state = 67
                self.match(LenguajeParser.DUBLE)
                self.state = 68
                self.match(LenguajeParser.ID)
                self.state = 69
                self.match(LenguajeParser.IGUAL)
                self.state = 70
                self.expr_decimal(0)
                self.state = 71
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




    def asignacion(self):

        localctx = LenguajeParser.AsignacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_asignacion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(LenguajeParser.ID)
            self.state = 76
            self.match(LenguajeParser.IGUAL)
            self.state = 77
            self.expr(0)
            self.state = 78
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




    def impresion(self):

        localctx = LenguajeParser.ImpresionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_impresion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(LenguajeParser.AMPRIMI)
            self.state = 81
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 82
            self.expr(0)
            self.state = 83
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 84
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




    def condicion_if(self):

        localctx = LenguajeParser.Condicion_ifContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_condicion_if)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(LenguajeParser.WI)
            self.state = 87
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 88
            self.expr(0)
            self.state = 89
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 90
            self.bloque()
            self.state = 93
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 91
                self.match(LenguajeParser.OTRE)
                self.state = 92
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




    def ciclo_while(self):

        localctx = LenguajeParser.Ciclo_whileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_ciclo_while)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.match(LenguajeParser.PENDAN)
            self.state = 96
            self.match(LenguajeParser.PARENTESIS_ABIERTO)
            self.state = 97
            self.expr(0)
            self.state = 98
            self.match(LenguajeParser.PARENTESIS_CERRADO)
            self.state = 99
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




    def retorno(self):

        localctx = LenguajeParser.RetornoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_retorno)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self.match(LenguajeParser.RETUR)
            self.state = 103
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 917504) != 0):
                self.state = 102
                self.expr(0)


            self.state = 105
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



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LenguajeParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.state = 108
                self.match(LenguajeParser.INT)
                pass
            elif token in [19]:
                self.state = 109
                self.match(LenguajeParser.FLOAT_LIT)
                pass
            elif token in [17]:
                self.state = 110
                self.match(LenguajeParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 118
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LenguajeParser.ExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                    self.state = 113
                    if not self.precpred(self._ctx, 4):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                    self.state = 114
                    self.match(LenguajeParser.OP)
                    self.state = 115
                    self.expr(5) 
                self.state = 120
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



    def expr_entera(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LenguajeParser.Expr_enteraContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_expr_entera, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.state = 122
                self.match(LenguajeParser.INT)
                pass
            elif token in [17]:
                self.state = 123
                self.match(LenguajeParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 131
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LenguajeParser.Expr_enteraContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr_entera)
                    self.state = 126
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 127
                    self.match(LenguajeParser.OP)
                    self.state = 128
                    self.expr_entera(4) 
                self.state = 133
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



    def expr_decimal(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LenguajeParser.Expr_decimalContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 24
        self.enterRecursionRule(localctx, 24, self.RULE_expr_decimal, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [19]:
                self.state = 135
                self.match(LenguajeParser.FLOAT_LIT)
                pass
            elif token in [18]:
                self.state = 136
                self.match(LenguajeParser.INT)
                pass
            elif token in [17]:
                self.state = 137
                self.match(LenguajeParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 145
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LenguajeParser.Expr_decimalContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr_decimal)
                    self.state = 140
                    if not self.precpred(self._ctx, 4):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                    self.state = 141
                    self.match(LenguajeParser.OP)
                    self.state = 142
                    self.expr_decimal(5) 
                self.state = 147
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
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

        def getRuleIndex(self):
            return LenguajeParser.RULE_tipo

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTipo" ):
                listener.enterTipo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTipo" ):
                listener.exitTipo(self)




    def tipo(self):

        localctx = LenguajeParser.TipoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_tipo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0)):
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




    def errorInstr(self):

        localctx = LenguajeParser.ErrorInstrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_errorInstr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 150
                    self.match(LenguajeParser.ERROR_CHAR)

                else:
                    raise NoViableAltException(self)
                self.state = 153 
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
                return self.precpred(self._ctx, 4)
         

    def expr_entera_sempred(self, localctx:Expr_enteraContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

    def expr_decimal_sempred(self, localctx:Expr_decimalContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         




