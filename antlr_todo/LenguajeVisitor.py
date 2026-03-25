# Generated from Lenguaje.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .LenguajeParser import LenguajeParser
else:
    from LenguajeParser import LenguajeParser

# This class defines a complete generic visitor for a parse tree produced by LenguajeParser.

class LenguajeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LenguajeParser#programa.
    def visitPrograma(self, ctx:LenguajeParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#bloque.
    def visitBloque(self, ctx:LenguajeParser.BloqueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#instrucciones.
    def visitInstrucciones(self, ctx:LenguajeParser.InstruccionesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#instruccion.
    def visitInstruccion(self, ctx:LenguajeParser.InstruccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#declaracion.
    def visitDeclaracion(self, ctx:LenguajeParser.DeclaracionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#asignacion.
    def visitAsignacion(self, ctx:LenguajeParser.AsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#impresion.
    def visitImpresion(self, ctx:LenguajeParser.ImpresionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#condicion_if.
    def visitCondicion_if(self, ctx:LenguajeParser.Condicion_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#ciclo_while.
    def visitCiclo_while(self, ctx:LenguajeParser.Ciclo_whileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#retorno.
    def visitRetorno(self, ctx:LenguajeParser.RetornoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#expr.
    def visitExpr(self, ctx:LenguajeParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#expr_entera.
    def visitExpr_entera(self, ctx:LenguajeParser.Expr_enteraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#expr_decimal.
    def visitExpr_decimal(self, ctx:LenguajeParser.Expr_decimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#tipo.
    def visitTipo(self, ctx:LenguajeParser.TipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#errorInstr.
    def visitErrorInstr(self, ctx:LenguajeParser.ErrorInstrContext):
        return self.visitChildren(ctx)



del LenguajeParser