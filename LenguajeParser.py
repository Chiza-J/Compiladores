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
        4,1,11,44,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,
        0,1,0,1,1,5,1,17,8,1,10,1,12,1,20,9,1,1,2,1,2,1,2,4,2,25,8,2,11,
        2,12,2,26,3,2,29,8,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,
        1,5,1,5,1,5,0,0,6,0,2,4,6,8,10,0,1,1,0,4,6,41,0,12,1,0,0,0,2,18,
        1,0,0,0,4,28,1,0,0,0,6,30,1,0,0,0,8,37,1,0,0,0,10,41,1,0,0,0,12,
        13,3,2,1,0,13,14,5,0,0,1,14,1,1,0,0,0,15,17,3,4,2,0,16,15,1,0,0,
        0,17,20,1,0,0,0,18,16,1,0,0,0,18,19,1,0,0,0,19,3,1,0,0,0,20,18,1,
        0,0,0,21,29,3,6,3,0,22,29,3,8,4,0,23,25,5,11,0,0,24,23,1,0,0,0,25,
        26,1,0,0,0,26,24,1,0,0,0,26,27,1,0,0,0,27,29,1,0,0,0,28,21,1,0,0,
        0,28,22,1,0,0,0,28,24,1,0,0,0,29,5,1,0,0,0,30,31,5,3,0,0,31,32,3,
        10,5,0,32,33,5,8,0,0,33,34,5,1,0,0,34,35,5,9,0,0,35,36,5,2,0,0,36,
        7,1,0,0,0,37,38,5,7,0,0,38,39,5,8,0,0,39,40,5,2,0,0,40,9,1,0,0,0,
        41,42,7,0,0,0,42,11,1,0,0,0,3,18,26,28
    ]

class LenguajeParser ( Parser ):

    grammarFileName = "Lenguaje.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "';'", "'variabli'", "'ontie'", 
                     "'flote'", "'duble'", "'amprimi'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "VARIABLI", 
                      "ONTIE", "FLOTE", "DUBLE", "AMPRIMI", "ID", "INT", 
                      "WS", "ERROR_CHAR" ]

    RULE_programa = 0
    RULE_instrucciones = 1
    RULE_instruccion = 2
    RULE_declaracion = 3
    RULE_impresion = 4
    RULE_tipo = 5

    ruleNames =  [ "programa", "instrucciones", "instruccion", "declaracion", 
                   "impresion", "tipo" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    VARIABLI=3
    ONTIE=4
    FLOTE=5
    DUBLE=6
    AMPRIMI=7
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
            self.state = 12
            self.instrucciones()
            self.state = 13
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
            self.state = 18
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2184) != 0):
                self.state = 15
                self.instruccion()
                self.state = 20
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


        def ERROR_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(LenguajeParser.ERROR_CHAR)
            else:
                return self.getToken(LenguajeParser.ERROR_CHAR, i)

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
            self.state = 28
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 21
                self.declaracion()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 22
                self.impresion()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 24 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 23
                        self.match(LenguajeParser.ERROR_CHAR)

                    else:
                        raise NoViableAltException(self)
                    self.state = 26 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

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

        def INT(self):
            return self.getToken(LenguajeParser.INT, 0)

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
            self.state = 30
            self.match(LenguajeParser.VARIABLI)
            self.state = 31
            self.tipo()
            self.state = 32
            self.match(LenguajeParser.ID)
            self.state = 33
            self.match(LenguajeParser.T__0)
            self.state = 34
            self.match(LenguajeParser.INT)
            self.state = 35
            self.match(LenguajeParser.T__1)
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
            self.state = 37
            self.match(LenguajeParser.AMPRIMI)
            self.state = 38
            self.match(LenguajeParser.ID)
            self.state = 39
            self.match(LenguajeParser.T__1)
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
            self.state = 41
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 112) != 0)):
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





