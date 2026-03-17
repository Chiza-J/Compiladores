# Generated from Lenguaje.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .LenguajeParser import LenguajeParser
else:
    from LenguajeParser import LenguajeParser

# This class defines a complete listener for a parse tree produced by LenguajeParser.
class LenguajeListener(ParseTreeListener):

    # Enter a parse tree produced by LenguajeParser#programa.
    def enterPrograma(self, ctx:LenguajeParser.ProgramaContext):
        pass

    # Exit a parse tree produced by LenguajeParser#programa.
    def exitPrograma(self, ctx:LenguajeParser.ProgramaContext):
        pass


    # Enter a parse tree produced by LenguajeParser#instrucciones.
    def enterInstrucciones(self, ctx:LenguajeParser.InstruccionesContext):
        pass

    # Exit a parse tree produced by LenguajeParser#instrucciones.
    def exitInstrucciones(self, ctx:LenguajeParser.InstruccionesContext):
        pass


    # Enter a parse tree produced by LenguajeParser#instruccion.
    def enterInstruccion(self, ctx:LenguajeParser.InstruccionContext):
        pass

    # Exit a parse tree produced by LenguajeParser#instruccion.
    def exitInstruccion(self, ctx:LenguajeParser.InstruccionContext):
        pass


    # Enter a parse tree produced by LenguajeParser#declaracion.
    def enterDeclaracion(self, ctx:LenguajeParser.DeclaracionContext):
        pass

    # Exit a parse tree produced by LenguajeParser#declaracion.
    def exitDeclaracion(self, ctx:LenguajeParser.DeclaracionContext):
        pass


    # Enter a parse tree produced by LenguajeParser#impresion.
    def enterImpresion(self, ctx:LenguajeParser.ImpresionContext):
        pass

    # Exit a parse tree produced by LenguajeParser#impresion.
    def exitImpresion(self, ctx:LenguajeParser.ImpresionContext):
        pass


    # Enter a parse tree produced by LenguajeParser#tipo.
    def enterTipo(self, ctx:LenguajeParser.TipoContext):
        pass

    # Exit a parse tree produced by LenguajeParser#tipo.
    def exitTipo(self, ctx:LenguajeParser.TipoContext):
        pass



del LenguajeParser