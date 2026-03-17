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
        4,1,11,47,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,1,0,1,0,1,1,5,1,19,8,1,10,1,12,1,22,9,1,1,2,1,2,1,2,3,2,27,
        8,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,1,5,1,6,4,6,
        43,8,6,11,6,12,6,44,1,6,0,0,7,0,2,4,6,8,10,12,0,1,1,0,2,4,43,0,14,
        1,0,0,0,2,20,1,0,0,0,4,26,1,0,0,0,6,28,1,0,0,0,8,35,1,0,0,0,10,39,
        1,0,0,0,12,42,1,0,0,0,14,15,3,2,1,0,15,16,5,0,0,1,16,1,1,0,0,0,17,
        19,3,4,2,0,18,17,1,0,0,0,19,22,1,0,0,0,20,18,1,0,0,0,20,21,1,0,0,
        0,21,3,1,0,0,0,22,20,1,0,0,0,23,27,3,6,3,0,24,27,3,8,4,0,25,27,3,
        12,6,0,26,23,1,0,0,0,26,24,1,0,0,0,26,25,1,0,0,0,27,5,1,0,0,0,28,
        29,5,1,0,0,29,30,3,10,5,0,30,31,5,8,0,0,31,32,5,6,0,0,32,33,5,9,
        0,0,33,34,5,7,0,0,34,7,1,0,0,0,35,36,5,5,0,0,36,37,5,8,0,0,37,38,
        5,7,0,0,38,9,1,0,0,0,39,40,7,0,0,0,40,11,1,0,0,0,41,43,5,11,0,0,
        42,41,1,0,0,0,43,44,1,0,0,0,44,42,1,0,0,0,44,45,1,0,0,0,45,13,1,
        0,0,0,3,20,26,44
    ]

class LenguajeParser ( Parser ):

    grammarFileName = "Lenguaje.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'variabli'", "'ontie'", "'flote'", "'duble'", 
                     "'amprimi'", "'='", "';'" ]

    symbolicNames = [ "<INVALID>", "VARIABLI", "ONTIE", "FLOTE", "DUBLE", 
                      "AMPRIMI", "IGUAL", "PUNTOCOMA", "ID", "INT", "WS", 
                      "ERROR_CHAR" ]

    RULE_programa = 0
    RULE_instrucciones = 1
    RULE_instruccion = 2
    RULE_declaracion = 3
    RULE_impresion = 4
    RULE_tipo = 5
    RULE_errorInstr = 6

    ruleNames =  [ "programa", "instrucciones", "instruccion", "declaracion", 
                   "impresion", "tipo", "errorInstr" ]

    EOF = Token.EOF
    VARIABLI=1
    ONTIE=2
    FLOTE=3
    DUBLE=4
    AMPRIMI=5
    IGUAL=6
    PUNTOCOMA=7
    ID=8
    INT=9
    WS=10
    ERROR_CHAR=11

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

        def instrucciones(self):
            return self.getTypedRuleContext(LenguajeParser.InstruccionesContext,0)


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
            self.state = 14
            self.instrucciones()
            self.state = 15
            self.match(LenguajeParser.EOF)
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
        self.enterRule(localctx, 2, self.RULE_instrucciones)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2082) != 0):
                self.state = 17
                self.instruccion()
                self.state = 22
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


        def impresion(self):
            return self.getTypedRuleContext(LenguajeParser.ImpresionContext,0)


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
        self.enterRule(localctx, 4, self.RULE_instruccion)
        try:
            self.state = 26
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 23
                self.declaracion()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                self.impresion()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 25
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

        def VARIABLI(self):
            return self.getToken(LenguajeParser.VARIABLI, 0)

        def tipo(self):
            return self.getTypedRuleContext(LenguajeParser.TipoContext,0)


        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

        def IGUAL(self):
            return self.getToken(LenguajeParser.IGUAL, 0)

        def INT(self):
            return self.getToken(LenguajeParser.INT, 0)

        def PUNTOCOMA(self):
            return self.getToken(LenguajeParser.PUNTOCOMA, 0)

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
        self.enterRule(localctx, 6, self.RULE_declaracion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self.match(LenguajeParser.VARIABLI)
            self.state = 29
            self.tipo()
            self.state = 30
            self.match(LenguajeParser.ID)
            self.state = 31
            self.match(LenguajeParser.IGUAL)
            self.state = 32
            self.match(LenguajeParser.INT)
            self.state = 33
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

        def ID(self):
            return self.getToken(LenguajeParser.ID, 0)

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
        self.enterRule(localctx, 8, self.RULE_impresion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(LenguajeParser.AMPRIMI)
            self.state = 36
            self.match(LenguajeParser.ID)
            self.state = 37
            self.match(LenguajeParser.PUNTOCOMA)
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
        self.enterRule(localctx, 10, self.RULE_tipo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28) != 0)):
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
        self.enterRule(localctx, 12, self.RULE_errorInstr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 41
                    self.match(LenguajeParser.ERROR_CHAR)

                else:
                    raise NoViableAltException(self)
                self.state = 44 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





