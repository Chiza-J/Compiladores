from antlr4 import *
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class AnalizadorSemantico(LenguajeVisitor):

    def __init__(self):
        # Tabla de simbolos: nombre -> tipo
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
    # ------------------------------------------------------------------ #
    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()

        if nombre in self.tabla_simbolos:
            self.errores.append(f"Variable '{nombre}' ya declarada")
            return

        if ctx.ONTIE():
            tipo = 'ontie'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_entera())

        elif ctx.FLOTE():
            tipo = 'flote'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_decimal())

        elif ctx.DUBLE():
            tipo = 'duble'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_decimal())

        elif ctx.SHEN():
            tipo = 'shen'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_string())

        # Validación de tipos
        if tipo == 'ontie' and tipo_expr != 'ontie':
            self.errores.append(f"No se puede asignar {tipo_expr} a ontie")

        elif tipo == 'flote' and tipo_expr not in ['ontie', 'flote']:
            self.errores.append(f"No se puede asignar {tipo_expr} a flote")

        elif tipo == 'duble' and tipo_expr not in ['ontie', 'flote', 'duble']:
            self.errores.append(f"No se puede asignar {tipo_expr} a duble")

        elif tipo == 'shen' and tipo_expr != 'shen':
            self.errores.append(f"No se puede asignar {tipo_expr} a shen")

        self.tabla_simbolos[nombre] = tipo

    # ------------------------------------------------------------------ #
    #  ASIGNACION
    # ------------------------------------------------------------------ #
    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()

        if nombre not in self.tabla_simbolos:
            self.errores.append(f"Variable '{nombre}' no declarada")
            return

        tipo_var = self.tabla_simbolos[nombre]
        tipo_expr = self.obtener_tipo_expr(ctx.expr())

        if tipo_var == 'shen' and tipo_expr != 'shen':
            self.errores.append("Asignación inválida a string")

        elif tipo_var != 'shen' and tipo_expr == 'shen':
            self.errores.append("No se puede asignar string a tipo numérico")

        elif tipo_var == 'ontie' and tipo_expr != 'ontie':
            self.errores.append("ontie solo acepta enteros")

        elif tipo_var == 'flote' and tipo_expr not in ['ontie', 'flote']:
            self.errores.append("flote solo acepta números")

        elif tipo_var == 'duble' and tipo_expr not in ['ontie', 'flote', 'duble']:
            self.errores.append("duble solo acepta números")

    # ------------------------------------------------------------------ #
    #  IMPRESION
    # ------------------------------------------------------------------ #
    def visitImpresion(self, ctx: LenguajeParser.ImpresionContext):
        self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  CONDICION IF
    # ------------------------------------------------------------------ #
    def visitCondicion_if(self, ctx: LenguajeParser.Condicion_ifContext):
        self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  CICLO WHILE
    # ------------------------------------------------------------------ #
    def visitCiclo_while(self, ctx: LenguajeParser.Ciclo_whileContext):
        self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  RETORNO
    # ------------------------------------------------------------------ #
    def visitRetorno(self, ctx: LenguajeParser.RetornoContext):
        if ctx.expr():
            self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  EXPRESIONES
    # ------------------------------------------------------------------ #

    def visitExpr(self, ctx):
        self.obtener_tipo_expr(ctx)
        return self.visitChildren(ctx)

    def visitExpr_entera(self, ctx):
        self.obtener_tipo_expr(ctx)
        return self.visitChildren(ctx)

    def visitExpr_decimal(self, ctx):
        self.obtener_tipo_expr(ctx)
        return self.visitChildren(ctx)

    def visitExpr_string(self, ctx):
        self.obtener_tipo_expr(ctx)
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ #
    #  FUNCION CENTRAL DE TIPOS
    # ------------------------------------------------------------------ #
    def obtener_tipo_expr(self, ctx):

        # 🔹 expr general
        if isinstance(ctx, LenguajeParser.ExprContext):

            if ctx.INT():
                return 'ontie'

            if ctx.FLOAT_LIT():
                return 'flote'

            if ctx.STRING():
                return 'shen'

            if ctx.ID():
                nombre = ctx.ID().getText()
                if nombre not in self.tabla_simbolos:
                    self.errores.append(f"Variable '{nombre}' no declarada")
                    return 'error'
                return self.tabla_simbolos[nombre]

            if ctx.getChildCount() == 3:
                t1 = self.obtener_tipo_expr(ctx.expr(0))
                t2 = self.obtener_tipo_expr(ctx.expr(1))
                op = ctx.getChild(1).getText()

                # STRING
                if t1 == 'shen' or t2 == 'shen':
                    if op == 'plu' and t1 == 'shen' and t2 == 'shen':
                        return 'shen'
                    self.errores.append(f"No se puede usar '{op}' con strings")
                    return 'error'

                # NUMÉRICO
                if t1 == 'duble' or t2 == 'duble':
                    return 'duble'
                if t1 == 'flote' or t2 == 'flote':
                    return 'flote'
                return 'ontie'

        # 🔹 expr_entera
        elif isinstance(ctx, LenguajeParser.Expr_enteraContext):

            if ctx.INT():
                return 'ontie'

            if ctx.ID():
                nombre = ctx.ID().getText()
                if nombre not in self.tabla_simbolos:
                    self.errores.append(f"Variable '{nombre}' no declarada")
                    return 'error'
                return self.tabla_simbolos[nombre]

            if ctx.getChildCount() == 3:
                return 'ontie'

        # 🔹 expr_decimal
        elif isinstance(ctx, LenguajeParser.Expr_decimalContext):

            if ctx.FLOAT_LIT():
                return 'flote'

            if ctx.INT():
                return 'ontie'

            if ctx.ID():
                nombre = ctx.ID().getText()
                if nombre not in self.tabla_simbolos:
                    self.errores.append(f"Variable '{nombre}' no declarada")
                    return 'error'
                return self.tabla_simbolos[nombre]

            if ctx.getChildCount() == 3:
                return 'flote'

        # 🔹 expr_string
        elif isinstance(ctx, LenguajeParser.Expr_stringContext):

            if ctx.STRING():
                return 'shen'

            if ctx.ID():
                nombre = ctx.ID().getText()
                if nombre not in self.tabla_simbolos:
                    self.errores.append(f"Variable '{nombre}' no declarada")
                    return 'error'
                return self.tabla_simbolos[nombre]

            if ctx.getChildCount() == 3:
                return 'shen'

        return 'error'