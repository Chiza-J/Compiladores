from antlr4 import *
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class AnalizadorSemantico(LenguajeVisitor):

    def __init__(self):
        self.tabla_simbolos = {}
        self.errores = []   # siempre dicts: {linea, columna, mensaje, tipo}

    #  helper para agregar error con ubicación 
    def _error(self, ctx, mensaje):
        try:
            token = ctx.start if hasattr(ctx, 'start') else ctx
            linea = token.line
            col   = token.column
        except Exception:
            linea, col = 0, 0
        self.errores.append({
            'linea':   linea,
            'columna': col,
            'mensaje': mensaje,
            'tipo':    'Semántico',
        })

    #  helper: obtiene el ctx de la expresión de valor en shen
    def _get_expr_cadena(self, ctx):
        """
        Busca el hijo de DeclaracionContext que corresponde a expr_cadena.
        Funciona aunque el parser no haya sido regenerado con el método
        expr_cadena() — recorre los hijos buscando uno que tenga STRING.
        """
        # Si el parser ya tiene el método, úsalo
        if hasattr(ctx, 'expr_cadena') and callable(ctx.expr_cadena):
            try:
                result = ctx.expr_cadena()
                if result is not None:
                    return result
            except Exception:
                pass

        # Fallback: buscar entre los hijos el que tenga STRING o ID
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if hasattr(child, 'STRING') and child.STRING():
                return child
            if hasattr(child, 'ID') and child.ID():
                # solo si no es el ID de la declaración (el 2do token)
                if i > 1:
                    return child
        return None

    #  PROGRAMA / BLOQUES 

    def visitPrograma(self, ctx: LenguajeParser.ProgramaContext):
        return self.visitChildren(ctx)

    def visitBloque(self, ctx: LenguajeParser.BloqueContext):
        return self.visitChildren(ctx)

    def visitInstrucciones(self, ctx: LenguajeParser.InstruccionesContext):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx: LenguajeParser.InstruccionContext):
        return self.visitChildren(ctx)

    #  DECLARACIÓN 

    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()

        if ctx.ONTIE():
            tipo      = 'ontie'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_entera())
        elif ctx.FLOTE():
            tipo      = 'flote'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_decimal())
        elif ctx.DUBLE():
            tipo      = 'duble'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_decimal())
        elif ctx.SHEN():
            tipo      = 'shen'
            # compatible tanto con parser nuevo (expr_cadena) como viejo
            expr_cad  = self._get_expr_cadena(ctx)
            tipo_expr = self.obtener_tipo_expr(expr_cad)
        else:
            return

        if not self.es_compatible(tipo, tipo_expr):
            self._error(ctx, f"No se puede asignar '{tipo_expr}' a '{tipo}' en '{nombre}'")

        self.tabla_simbolos[nombre] = tipo

    #  ASIGNACIÓN 

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()

        if nombre not in self.tabla_simbolos:
            self._error(ctx, f"Variable '{nombre}' no declarada")
            return

        tipo_var  = self.tabla_simbolos[nombre]
        tipo_expr = self.obtener_tipo_expr(ctx.expr())

        if not self.es_compatible(tipo_var, tipo_expr):
            self._error(ctx, f"No se puede asignar '{tipo_expr}' a '{tipo_var}' en '{nombre}'")

    #  IMPRESIÓN 

    def visitImpresion(self, ctx):
        self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    #  CONTROL DE FLUJO 

    def visitCondicion_if(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo == 'shen':
            self._error(ctx, "La condición no puede ser de tipo 'shen'")
        return self.visitChildren(ctx)

    def visitCiclo_while(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo == 'shen':
            self._error(ctx, "La condición no puede ser de tipo 'shen'")
        return self.visitChildren(ctx)

    def visitRetorno(self, ctx):
        if ctx.expr():
            self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    #  VALIDACIÓN DE EXPRESIONES 

    def obtener_tipo_expr(self, ctx):
        if ctx is None:
            return 'error'

        if hasattr(ctx, 'STRING') and ctx.STRING():
            return 'shen'

        if hasattr(ctx, 'INT') and ctx.INT():
            return 'ontie'

        if hasattr(ctx, 'FLOAT_LIT') and ctx.FLOAT_LIT():
            return 'duble'

        if hasattr(ctx, 'ID') and ctx.ID():
            nombre = ctx.ID().getText()
            if nombre not in self.tabla_simbolos:
                self._error(ctx, f"Variable '{nombre}' no declarada")
                return 'error'
            return self.tabla_simbolos[nombre]

        if ctx.getChildCount() == 3:
            tipo_izq = self.obtener_tipo_expr(ctx.getChild(0))
            tipo_der = self.obtener_tipo_expr(ctx.getChild(2))
            op       = ctx.getChild(1).getText()

            if tipo_izq == 'error' or tipo_der == 'error':
                return 'error'

            if tipo_izq == 'shen' or tipo_der == 'shen':
                if op == 'plu' and tipo_izq == 'shen' and tipo_der == 'shen':
                    return 'shen'
                self._error(ctx, f"No se puede usar '{op}' entre '{tipo_izq}' y '{tipo_der}'")
                return 'error'

            if tipo_izq in ['ontie', 'flote', 'duble'] and tipo_der in ['ontie', 'flote', 'duble']:
                if op in ['plu', 'moan', 'par', 'bag']:
                    return self.promocion(tipo_izq, tipo_der)
                if op in ['minog', 'aye', 'compag']:
                    return 'ontie'

            self._error(ctx, f"Operación inválida: '{tipo_izq}' {op} '{tipo_der}'")
            return 'error'

        return 'error'

    #  PROMOCIÓN DE TIPOS 

    def promocion(self, t1, t2):
        if 'duble' in (t1, t2):
            return 'duble'
        if 'flote' in (t1, t2):
            return 'flote'
        return 'ontie'

    #  COMPATIBILIDAD 

    def es_compatible(self, destino, origen):
        if destino == origen:
            return True
        if destino in ['duble', 'flote'] and origen in ['ontie', 'flote', 'duble']:
            return True
        if destino == 'shen' and origen != 'shen':
            return False
        if destino != 'shen' and origen == 'shen':
            return False
        if destino == 'ontie' and origen in ['flote', 'duble']:
            return False
        return False