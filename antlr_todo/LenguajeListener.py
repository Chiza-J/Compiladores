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


    # Enter a parse tree produced by LenguajeParser#bloque.
    def enterBloque(self, ctx:LenguajeParser.BloqueContext):
        pass

    # Exit a parse tree produced by LenguajeParser#bloque.
    def exitBloque(self, ctx:LenguajeParser.BloqueContext):
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


    # Enter a parse tree produced by LenguajeParser#asignacion.
    def enterAsignacion(self, ctx:LenguajeParser.AsignacionContext):
        pass

    # Exit a parse tree produced by LenguajeParser#asignacion.
    def exitAsignacion(self, ctx:LenguajeParser.AsignacionContext):
        pass


    # Enter a parse tree produced by LenguajeParser#impresion.
    def enterImpresion(self, ctx:LenguajeParser.ImpresionContext):
        pass

    # Exit a parse tree produced by LenguajeParser#impresion.
    def exitImpresion(self, ctx:LenguajeParser.ImpresionContext):
        pass


    # Enter a parse tree produced by LenguajeParser#condicion_if.
    def enterCondicion_if(self, ctx:LenguajeParser.Condicion_ifContext):
        pass

    # Exit a parse tree produced by LenguajeParser#condicion_if.
    def exitCondicion_if(self, ctx:LenguajeParser.Condicion_ifContext):
        pass


    # Enter a parse tree produced by LenguajeParser#ciclo_while.
    def enterCiclo_while(self, ctx:LenguajeParser.Ciclo_whileContext):
        pass

    # Exit a parse tree produced by LenguajeParser#ciclo_while.
    def exitCiclo_while(self, ctx:LenguajeParser.Ciclo_whileContext):
        pass


    # Enter a parse tree produced by LenguajeParser#ciclo_fer_pendan.
    def enterCiclo_fer_pendan(self, ctx:LenguajeParser.Ciclo_fer_pendanContext):
        pass

    # Exit a parse tree produced by LenguajeParser#ciclo_fer_pendan.
    def exitCiclo_fer_pendan(self, ctx:LenguajeParser.Ciclo_fer_pendanContext):
        pass


    # Enter a parse tree produced by LenguajeParser#ciclo_pur.
    def enterCiclo_pur(self, ctx:LenguajeParser.Ciclo_purContext):
        pass

    # Exit a parse tree produced by LenguajeParser#ciclo_pur.
    def exitCiclo_pur(self, ctx:LenguajeParser.Ciclo_purContext):
        pass


    # Enter a parse tree produced by LenguajeParser#pur_init.
    def enterPur_init(self, ctx:LenguajeParser.Pur_initContext):
        pass

    # Exit a parse tree produced by LenguajeParser#pur_init.
    def exitPur_init(self, ctx:LenguajeParser.Pur_initContext):
        pass


    # Enter a parse tree produced by LenguajeParser#pur_step.
    def enterPur_step(self, ctx:LenguajeParser.Pur_stepContext):
        pass

    # Exit a parse tree produced by LenguajeParser#pur_step.
    def exitPur_step(self, ctx:LenguajeParser.Pur_stepContext):
        pass


    # Enter a parse tree produced by LenguajeParser#retorno.
    def enterRetorno(self, ctx:LenguajeParser.RetornoContext):
        pass

    # Exit a parse tree produced by LenguajeParser#retorno.
    def exitRetorno(self, ctx:LenguajeParser.RetornoContext):
        pass


    # Enter a parse tree produced by LenguajeParser#funcion_def.
    def enterFuncion_def(self, ctx:LenguajeParser.Funcion_defContext):
        pass

    # Exit a parse tree produced by LenguajeParser#funcion_def.
    def exitFuncion_def(self, ctx:LenguajeParser.Funcion_defContext):
        pass


    # Enter a parse tree produced by LenguajeParser#tipo_retorno.
    def enterTipo_retorno(self, ctx:LenguajeParser.Tipo_retornoContext):
        pass

    # Exit a parse tree produced by LenguajeParser#tipo_retorno.
    def exitTipo_retorno(self, ctx:LenguajeParser.Tipo_retornoContext):
        pass


    # Enter a parse tree produced by LenguajeParser#parametros.
    def enterParametros(self, ctx:LenguajeParser.ParametrosContext):
        pass

    # Exit a parse tree produced by LenguajeParser#parametros.
    def exitParametros(self, ctx:LenguajeParser.ParametrosContext):
        pass


    # Enter a parse tree produced by LenguajeParser#parametro.
    def enterParametro(self, ctx:LenguajeParser.ParametroContext):
        pass

    # Exit a parse tree produced by LenguajeParser#parametro.
    def exitParametro(self, ctx:LenguajeParser.ParametroContext):
        pass


    # Enter a parse tree produced by LenguajeParser#llamada_funcion.
    def enterLlamada_funcion(self, ctx:LenguajeParser.Llamada_funcionContext):
        pass

    # Exit a parse tree produced by LenguajeParser#llamada_funcion.
    def exitLlamada_funcion(self, ctx:LenguajeParser.Llamada_funcionContext):
        pass


    # Enter a parse tree produced by LenguajeParser#argumentos.
    def enterArgumentos(self, ctx:LenguajeParser.ArgumentosContext):
        pass

    # Exit a parse tree produced by LenguajeParser#argumentos.
    def exitArgumentos(self, ctx:LenguajeParser.ArgumentosContext):
        pass


    # Enter a parse tree produced by LenguajeParser#llamada_funcion_stmt.
    def enterLlamada_funcion_stmt(self, ctx:LenguajeParser.Llamada_funcion_stmtContext):
        pass

    # Exit a parse tree produced by LenguajeParser#llamada_funcion_stmt.
    def exitLlamada_funcion_stmt(self, ctx:LenguajeParser.Llamada_funcion_stmtContext):
        pass


    # Enter a parse tree produced by LenguajeParser#expr.
    def enterExpr(self, ctx:LenguajeParser.ExprContext):
        pass

    # Exit a parse tree produced by LenguajeParser#expr.
    def exitExpr(self, ctx:LenguajeParser.ExprContext):
        pass


    # Enter a parse tree produced by LenguajeParser#expr_entera.
    def enterExpr_entera(self, ctx:LenguajeParser.Expr_enteraContext):
        pass

    # Exit a parse tree produced by LenguajeParser#expr_entera.
    def exitExpr_entera(self, ctx:LenguajeParser.Expr_enteraContext):
        pass


    # Enter a parse tree produced by LenguajeParser#expr_decimal.
    def enterExpr_decimal(self, ctx:LenguajeParser.Expr_decimalContext):
        pass

    # Exit a parse tree produced by LenguajeParser#expr_decimal.
    def exitExpr_decimal(self, ctx:LenguajeParser.Expr_decimalContext):
        pass


    # Enter a parse tree produced by LenguajeParser#expr_string.
    def enterExpr_string(self, ctx:LenguajeParser.Expr_stringContext):
        pass

    # Exit a parse tree produced by LenguajeParser#expr_string.
    def exitExpr_string(self, ctx:LenguajeParser.Expr_stringContext):
        pass


    # Enter a parse tree produced by LenguajeParser#tipo.
    def enterTipo(self, ctx:LenguajeParser.TipoContext):
        pass

    # Exit a parse tree produced by LenguajeParser#tipo.
    def exitTipo(self, ctx:LenguajeParser.TipoContext):
        pass


    # Enter a parse tree produced by LenguajeParser#errorInstr.
    def enterErrorInstr(self, ctx:LenguajeParser.ErrorInstrContext):
        pass

    # Exit a parse tree produced by LenguajeParser#errorInstr.
    def exitErrorInstr(self, ctx:LenguajeParser.ErrorInstrContext):
        pass



del LenguajeParser