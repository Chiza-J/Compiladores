from antlr4 import *
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class AnalizadorSemantico(LenguajeVisitor):

    def __init__(self):
        self.tabla_simbolos = {}
        self.errores = []

    # PROGRAMA / BLOQUES

    def visitPrograma(self, ctx: LenguajeParser.ProgramaContext):
        return self.visitChildren(ctx)

    def visitBloque(self, ctx: LenguajeParser.BloqueContext):
        return self.visitChildren(ctx)

    def visitInstrucciones(self, ctx: LenguajeParser.InstruccionesContext):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx: LenguajeParser.InstruccionContext):
        return self.visitChildren(ctx)

    # DECLARACIÓN

    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()

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
        else:
            return

        # VALIDACIÓN DE ASIGNACIÓN
        if not self.es_compatible(tipo, tipo_expr):
            self.errores.append(
                f"Error: no se puede asignar {tipo_expr} a {tipo} en '{nombre}'"
            )

        self.tabla_simbolos[nombre] = tipo

    # ASIGNACIÓN

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()

        if nombre not in self.tabla_simbolos:
            self.errores.append(f"Variable '{nombre}' no declarada")
            return

        tipo_var = self.tabla_simbolos[nombre]
        tipo_expr = self.obtener_tipo_expr(ctx.expr())

        if not self.es_compatible(tipo_var, tipo_expr):
            self.errores.append(
                f"Error: no se puede asignar {tipo_expr} a {tipo_var} en '{nombre}'"
            )

    # IMPRESIÓN

    def visitImpresion(self, ctx):
        self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    # CONTROL DE FLUJO

    def visitCondicion_if(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())

        if tipo == 'shen':
            self.errores.append("Error: condición no puede ser string")

        return self.visitChildren(ctx)

    def visitCiclo_while(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())

        if tipo == 'shen':
            self.errores.append("Error: condición no puede ser string")

        return self.visitChildren(ctx)

    def visitRetorno(self, ctx):
        if ctx.expr():
            self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    # VALIDACIÓN DE EXPRESIONES

    def obtener_tipo_expr(self, ctx):

        if ctx is None:
            return 'error'

        # STRING
        if hasattr(ctx, "STRING") and ctx.STRING():
            return 'shen'

        # ENTERO
        if hasattr(ctx, "INT") and ctx.INT():
            return 'ontie'

        # DECIMAL
        if hasattr(ctx, "FLOAT_LIT") and ctx.FLOAT_LIT():
            return 'duble'

        # VARIABLE
        if hasattr(ctx, "ID") and ctx.ID():
            nombre = ctx.ID().getText()

            if nombre not in self.tabla_simbolos:
                self.errores.append(f"Variable '{nombre}' no declarada")
                return 'error'

            return self.tabla_simbolos[nombre]

        # EXPRESIÓN BINARIA
        if ctx.getChildCount() == 3:
            tipo_izq = self.obtener_tipo_expr(ctx.getChild(0))
            tipo_der = self.obtener_tipo_expr(ctx.getChild(2))
            op = ctx.getChild(1).getText()

            # ERROR PREVIO
            if tipo_izq == 'error' or tipo_der == 'error':
                return 'error'

            #  STRINGS 
            if tipo_izq == 'shen' or tipo_der == 'shen':
                if op == 'plu' and tipo_izq == 'shen' and tipo_der == 'shen':
                    return 'shen'
                else:
                    self.errores.append(
                        f"Error: no se puede usar '{op}' entre {tipo_izq} y {tipo_der}"
                    )
                    return 'error'

            #  NUMÉRICOS 
            if tipo_izq in ['ontie', 'flote', 'duble'] and tipo_der in ['ontie', 'flote', 'duble']:

                if op in ['plu', 'moan', 'par', 'bag']:
                    return self.promocion(tipo_izq, tipo_der)

                if op in ['minog', 'aye', 'compag']:
                    return 'ontie'  # boolean simulado como int

            self.errores.append(
                f"Operación inválida: {tipo_izq} {op} {tipo_der}"
            )
            return 'error'

        return 'error'

    # PROMOCIÓN DE TIPOS

    def promocion(self, t1, t2):
        if 'duble' in (t1, t2):
            return 'duble'
        if 'flote' in (t1, t2):
            return 'flote'
        return 'ontie'

    # COMPATIBILIDAD DE ASIGNACIÓN

    def es_compatible(self, destino, origen):

        if destino == origen:
            return True

        # NUMÉRICOS (permite promoción hacia arriba)
        if destino in ['duble', 'flote']:
            if origen in ['ontie', 'flote', 'duble']:
                return True

        #  PROHIBIDO: string con números
        if destino == 'shen' and origen != 'shen':
            return False

        if destino != 'shen' and origen == 'shen':
            return False

        #  evitar pérdida (double → int)
        if destino == 'ontie' and origen in ['flote', 'duble']:
            return False

        return False