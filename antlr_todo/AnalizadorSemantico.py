from antlr4 import *
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class AnalizadorSemantico(LenguajeVisitor):

    def __init__(self):
        # Tabla de simbolos: nombre -> tipo  ('ontie', 'flote', 'duble')
        self.tabla_simbolos = {}
        self.errores = []

    # ------------------------------------------------------------------ #
    #  PROGRAMA
    # ------------------------------------------------------------------ #
    def visitPrograma(self, ctx: LenguajeParser.ProgramaContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  BLOQUE
    # ------------------------------------------------------------------ #
    def visitBloque(self, ctx: LenguajeParser.BloqueContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  INSTRUCCIONES
    # ------------------------------------------------------------------ #
    def visitInstrucciones(self, ctx: LenguajeParser.InstruccionesContext):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx: LenguajeParser.InstruccionContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  DECLARACION
    #  ontie x iyal 5 puavir
    #  flote x iyal 3.14 puavir
    #  duble x iyal 3.14 puavir
    # ------------------------------------------------------------------ #
    def visitDeclaracion(self, ctx: LenguajeParser.DeclaracionContext):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column

        # Determinar tipo por el token inicial
        if ctx.ONTIE():
            tipo = 'ontie'
        elif ctx.FLOTE():
            tipo = 'flote'
        else:
            tipo = 'duble'

        # Variable ya declarada
        if nombre in self.tabla_simbolos:
            self.errores.append({
                "linea":   linea,
                "columna": col,
                "mensaje": f"Variable '{nombre}' ya fue declarada anteriormente",
                "tipo":    "Semántico"
            })
        else:
            self.tabla_simbolos[nombre] = tipo

        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  ASIGNACION
    #  x iyal expr puavir
    # ------------------------------------------------------------------ #
    def visitAsignacion(self, ctx: LenguajeParser.AsignacionContext):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column

        if nombre not in self.tabla_simbolos:
            self.errores.append({
                "linea":   linea,
                "columna": col,
                "mensaje": f"Variable '{nombre}' usada sin declarar",
                "tipo":    "Semántico"
            })

        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  IMPRESION
    #  amprimi(expr) puavir
    # ------------------------------------------------------------------ #
    def visitImpresion(self, ctx: LenguajeParser.ImpresionContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  CONDICION IF
    # ------------------------------------------------------------------ #
    def visitCondicion_if(self, ctx: LenguajeParser.Condicion_ifContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  CICLO WHILE
    # ------------------------------------------------------------------ #
    def visitCiclo_while(self, ctx: LenguajeParser.Ciclo_whileContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  RETORNO
    # ------------------------------------------------------------------ #
    def visitRetorno(self, ctx: LenguajeParser.RetornoContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  EXPRESIONES — verifica que los IDs usados estén declarados
    # ------------------------------------------------------------------ #
    def visitExpr(self, ctx: LenguajeParser.ExprContext):
        if ctx.ID():
            nombre = ctx.ID().getText()
            linea  = ctx.ID().getSymbol().line
            col    = ctx.ID().getSymbol().column
            if nombre not in self.tabla_simbolos:
                self.errores.append({
                    "linea":   linea,
                    "columna": col,
                    "mensaje": f"Variable '{nombre}' usada sin declarar",
                    "tipo":    "Semántico"
                })
        return self.visitChildren(ctx)

    def visitExpr_entera(self, ctx: LenguajeParser.Expr_enteraContext):
        if ctx.ID():
            nombre = ctx.ID().getText()
            linea  = ctx.ID().getSymbol().line
            col    = ctx.ID().getSymbol().column
            if nombre not in self.tabla_simbolos:
                self.errores.append({
                    "linea":   linea,
                    "columna": col,
                    "mensaje": f"Variable '{nombre}' usada sin declarar",
                    "tipo":    "Semántico"
                })
            elif self.tabla_simbolos[nombre] not in ('ontie',):
                self.errores.append({
                    "linea":   linea,
                    "columna": col,
                    "mensaje": f"Variable '{nombre}' es de tipo '{self.tabla_simbolos[nombre]}' pero se esperaba 'ontie'",
                    "tipo":    "Semántico"
                })
        return self.visitChildren(ctx)

    def visitExpr_decimal(self, ctx: LenguajeParser.Expr_decimalContext):
        if ctx.ID():
            nombre = ctx.ID().getText()
            linea  = ctx.ID().getSymbol().line
            col    = ctx.ID().getSymbol().column
            if nombre not in self.tabla_simbolos:
                self.errores.append({
                    "linea":   linea,
                    "columna": col,
                    "mensaje": f"Variable '{nombre}' usada sin declarar",
                    "tipo":    "Semántico"
                })
            elif self.tabla_simbolos[nombre] not in ('flote', 'duble', 'ontie'):
                self.errores.append({
                    "linea":   linea,
                    "columna": col,
                    "mensaje": f"Variable '{nombre}' es de tipo '{self.tabla_simbolos[nombre]}' pero se esperaba tipo numérico",
                    "tipo":    "Semántico"
                })
        return self.visitChildren(ctx)

    def visitTipo(self, ctx: LenguajeParser.TipoContext):
        return self.visitChildren(ctx)

    def visitErrorInstr(self, ctx: LenguajeParser.ErrorInstrContext):
        return self.visitChildren(ctx)