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


    # Visit a parse tree produced by LenguajeParser#entrada.
    def visitEntrada(self, ctx:LenguajeParser.EntradaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#condicion_if.
    def visitCondicion_if(self, ctx:LenguajeParser.Condicion_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#ciclo_while.
    def visitCiclo_while(self, ctx:LenguajeParser.Ciclo_whileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#ciclo_fer_pendan.
    def visitCiclo_fer_pendan(self, ctx:LenguajeParser.Ciclo_fer_pendanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#ciclo_pur.
    def visitCiclo_pur(self, ctx:LenguajeParser.Ciclo_purContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#pur_init.
    def visitPur_init(self, ctx:LenguajeParser.Pur_initContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#pur_step.
    def visitPur_step(self, ctx:LenguajeParser.Pur_stepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#condicion_switch.
    def visitCondicion_switch(self, ctx:LenguajeParser.Condicion_switchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#caso_switch.
    def visitCaso_switch(self, ctx:LenguajeParser.Caso_switchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#caso_default.
    def visitCaso_default(self, ctx:LenguajeParser.Caso_defaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#sentencia_pos.
    def visitSentencia_pos(self, ctx:LenguajeParser.Sentencia_posContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#sentencia_contine.
    def visitSentencia_contine(self, ctx:LenguajeParser.Sentencia_contineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#sentencia_su.
    def visitSentencia_su(self, ctx:LenguajeParser.Sentencia_suContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#retorno.
    def visitRetorno(self, ctx:LenguajeParser.RetornoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#funcion_def.
    def visitFuncion_def(self, ctx:LenguajeParser.Funcion_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#tipo_retorno.
    def visitTipo_retorno(self, ctx:LenguajeParser.Tipo_retornoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#parametros.
    def visitParametros(self, ctx:LenguajeParser.ParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#parametro.
    def visitParametro(self, ctx:LenguajeParser.ParametroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#llamada_funcion.
    def visitLlamada_funcion(self, ctx:LenguajeParser.Llamada_funcionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#argumentos.
    def visitArgumentos(self, ctx:LenguajeParser.ArgumentosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#llamada_funcion_stmt.
    def visitLlamada_funcion_stmt(self, ctx:LenguajeParser.Llamada_funcion_stmtContext):
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


    # Visit a parse tree produced by LenguajeParser#expr_string.
    def visitExpr_string(self, ctx:LenguajeParser.Expr_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#tipo.
    def visitTipo(self, ctx:LenguajeParser.TipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LenguajeParser#errorInstr.
    def visitErrorInstr(self, ctx:LenguajeParser.ErrorInstrContext):
        return self.visitChildren(ctx)



del LenguajeParser