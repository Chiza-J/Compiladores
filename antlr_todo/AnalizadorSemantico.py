from antlr4 import *
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class AnalizadorSemantico(LenguajeVisitor):

    # CONSTRUCTOR

    def __init__(self):

        # TABLA GLOBAL DE VARIABLES
        self.tabla_simbolos = {}

        # TABLA DE FUNCIONES
        self.tabla_funciones = {}

        # LISTA DE ERRORES
        self.errores = []

        # FUNCION ACTUAL
        self._scope_funcion = None

        # CONTROL DE LOOPS
        self._dentro_loop = 0

        # CONTROL DE SWITCH
        self._dentro_switch = 0

        # SCOPES
        self.pila_scopes = [{}]

    # ==========================================================
    # HELPERS
    # ==========================================================

    def abrir_scope(self):
        self.pila_scopes.append({})

    def cerrar_scope(self):
        if len(self.pila_scopes) > 1:
            self.pila_scopes.pop()

    def declarar_variable(self, nombre, tipo, ctx):

        scope_actual = self.pila_scopes[-1]

        if nombre in scope_actual:
            self._error(
                ctx,
                f"Variable '{nombre}' ya fue declarada"
            )
            return False

        scope_actual[nombre] = tipo
        return True

    def buscar_variable(self, nombre):

        for scope in reversed(self.pila_scopes):

            if nombre in scope:
                return scope[nombre]

        return None

    def _tipo_legible(self, tipo):

        return {
            'ontie': 'int (ontie)',
            'flote': 'float (flote)',
            'duble': 'double (duble)',
            'shen': 'varchar (shen)',
            'vid': 'void (vid)',
            'error': 'desconocido'
        }.get(tipo, tipo)

    def _error(self, ctx, mensaje):

        try:
            token = ctx.start if hasattr(ctx, 'start') else ctx

            linea = token.line
            columna = token.column

        except Exception:

            linea = 0
            columna = 0

        self.errores.append({
            'linea': linea,
            'columna': columna,
            'mensaje': mensaje,
            'tipo': 'Semantico'
        })

    def _tipo_retorno(self, ctx):

        if ctx.ONTIE():
            return 'ontie'

        if ctx.FLOTE():
            return 'flote'

        if ctx.DUBLE():
            return 'duble'

        if ctx.SHEN():
            return 'shen'

        if ctx.VID():
            return 'vid'

        return 'error'

    # PROGRAMA

    def visitPrograma(self, ctx: LenguajeParser.ProgramaContext):

        for child in ctx.getChildren():
            self.visit(child)

        return None

    # BLOQUES

    def visitBloque(self, ctx: LenguajeParser.BloqueContext):

        self.abrir_scope()

        self.visitChildren(ctx)

        self.cerrar_scope()

        return None

    def visitInstrucciones(self, ctx):

        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx):

        return self.visitChildren(ctx)

    # DECLARACION

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
            return None

        if not self.declarar_variable(nombre, tipo, ctx):
            return None

        if not self.es_compatible(tipo, tipo_expr):

            self._error(
                ctx,
                f"No se puede asignar "
                f"{self._tipo_legible(tipo_expr)} "
                f"a "
                f"{self._tipo_legible(tipo)}"
            )

        return None

    # ASIGNACION

    def visitAsignacion(self, ctx):

        nombre = ctx.ID().getText()

        tipo_variable = self.buscar_variable(nombre)

        if tipo_variable is None:

            self._error(
                ctx,
                f"Variable '{nombre}' usada sin declarar"
            )

            return None

        tipo_expr = self.obtener_tipo_expr(ctx.expr())

        if not self.es_compatible(tipo_variable, tipo_expr):

            self._error(
                ctx,
                f"No se puede asignar "
                f"{self._tipo_legible(tipo_expr)} "
                f"a "
                f"{self._tipo_legible(tipo_variable)}"
            )

        return None

    # IMPRESION

    def visitImpresion(self, ctx):

        self.obtener_tipo_expr(ctx.expr())

        return None

    # ENTRADA

    def visitEntrada(self, ctx):

        nombre = ctx.ID().getText()

        tipo = self.buscar_variable(nombre)

        if tipo is None:

            self._error(
                ctx,
                f"Variable '{nombre}' usada sin declarar"
            )

        return None

    # IF

    def visitCondicion_if(self, ctx):

        tipo = self.obtener_tipo_expr(ctx.expr())

        if tipo == 'shen':

            self._error(
                ctx,
                "La condicion del wi no puede ser string"
            )

        return self.visitChildren(ctx)

    # WHILE

    def visitCiclo_while(self, ctx):

        tipo = self.obtener_tipo_expr(ctx.expr())

        if tipo == 'shen':

            self._error(
                ctx,
                "La condicion del pendan no puede ser string"
            )

        self._dentro_loop += 1

        self.visit(ctx.bloque())

        self._dentro_loop -= 1

        return None

    # DO WHILE

    def visitCiclo_fer_pendan(self, ctx):

        self._dentro_loop += 1

        self.visit(ctx.bloque())

        self._dentro_loop -= 1

        tipo = self.obtener_tipo_expr(ctx.expr())

        if tipo == 'shen':

            self._error(
                ctx,
                "La condicion del fer_pendan no puede ser string"
            )

        return None

    # FOR

    def visitCiclo_pur(self, ctx):

        self.abrir_scope()

        self.visit(ctx.pur_init())

        tipo = self.obtener_tipo_expr(ctx.expr())

        if tipo == 'shen':

            self._error(
                ctx,
                "La condicion del pur no puede ser string"
            )

        self._dentro_loop += 1

        self.visit(ctx.pur_step())

        self.visit(ctx.bloque())

        self._dentro_loop -= 1

        self.cerrar_scope()

        return None

    def visitPur_init(self, ctx):

        nombre = ctx.ID().getText()

        if ctx.ONTIE():

            tipo = 'ontie'
            self.declarar_variable(nombre, tipo, ctx)

        elif ctx.FLOTE():

            tipo = 'flote'
            self.declarar_variable(nombre, tipo, ctx)

        elif ctx.DUBLE():

            tipo = 'duble'
            self.declarar_variable(nombre, tipo, ctx)

        elif ctx.SHEN():

            tipo = 'shen'
            self.declarar_variable(nombre, tipo, ctx)

        else:

            tipo = self.buscar_variable(nombre)

            if tipo is None:

                self._error(
                    ctx,
                    f"Variable '{nombre}' usada sin declarar"
                )

        return None

    def visitPur_step(self, ctx):

        nombre = ctx.ID().getText()

        tipo = self.buscar_variable(nombre)

        if tipo is None:

            self._error(
                ctx,
                f"Variable '{nombre}' usada sin declarar"
            )

        return None

    # SWITCH

    def visitCondicion_switch(self, ctx):

        tipo = self.obtener_tipo_expr(ctx.expr())

        if tipo != 'ontie' and tipo != 'error':

            self._error(
                ctx,
                "El shangshe solo acepta ontie"
            )

        self._dentro_switch += 1

        self.visitChildren(ctx)

        self._dentro_switch -= 1

        return None

    # BREAK

    def visitSentencia_pos(self, ctx):

        if self._dentro_loop == 0 and self._dentro_switch == 0:

            self._error(
                ctx,
                "pos solo puede usarse dentro de loop o switch"
            )

        return None

    # CONTINUE

    def visitSentencia_contine(self, ctx):

        if self._dentro_loop == 0:

            self._error(
                ctx,
                "contine solo puede usarse dentro de loop"
            )

        return None

    # GOTO

    def visitSentencia_su(self, ctx):

        return None

    # RETURN

    def visitRetorno(self, ctx):

        if self._scope_funcion is None:
            return None

        if ctx.expr():

            tipo_expr = self.obtener_tipo_expr(ctx.expr())

            if not self.es_compatible(
                self._scope_funcion,
                tipo_expr
            ):

                self._error(
                    ctx,
                    f"La funcion debe retornar "
                    f"{self._tipo_legible(self._scope_funcion)}"
                )

        return None

    # FUNCIONES

    def visitFuncion_def(self, ctx):

        nombre = ctx.ID().getText()

        tipo_retorno = self._tipo_retorno(
            ctx.tipo_retorno()
        )

        if nombre in self.tabla_funciones:

            self._error(
                ctx,
                f"Funcion '{nombre}' ya declarada"
            )

            return None

        parametros = []

        if ctx.parametros():

            for p in ctx.parametros().parametro():

                if p.ONTIE():
                    tipo = 'ontie'

                elif p.FLOTE():
                    tipo = 'flote'

                elif p.DUBLE():
                    tipo = 'duble'

                elif p.SHEN():
                    tipo = 'shen'

                else:
                    tipo = 'error'

                parametros.append(
                    (tipo, p.ID().getText())
                )

        self.tabla_funciones[nombre] = {
            'retorno': tipo_retorno,
            'params': parametros
        }

        scope_anterior = self._scope_funcion

        self._scope_funcion = tipo_retorno

        self.abrir_scope()

        for tipo, nombre_param in parametros:

            self.declarar_variable(
                nombre_param,
                tipo,
                ctx
            )

        self.visit(ctx.bloque())

        self.cerrar_scope()

        self._scope_funcion = scope_anterior

        return None

    # LLAMADAS A FUNCION

    def visitLlamada_funcion(self, ctx):

        nombre = ctx.ID().getText()

        if nombre not in self.tabla_funciones:

            self._error(
                ctx,
                f"Funcion '{nombre}' no declarada"
            )

            return 'error'

        info = self.tabla_funciones[nombre]

        params = info['params']

        argumentos = []

        if ctx.argumentos():
            argumentos = ctx.argumentos().expr()

        if len(argumentos) != len(params):

            self._error(
                ctx,
                f"Funcion '{nombre}' esperaba "
                f"{len(params)} argumentos"
            )

        else:

            for (tipo_param, nombre_param), arg in zip(params, argumentos):

                tipo_arg = self.obtener_tipo_expr(arg)

                if not self.es_compatible(tipo_param, tipo_arg):

                    self._error(
                        ctx,
                        f"Argumento '{nombre_param}' incompatible"
                    )

        return info['retorno']

    def visitLlamada_funcion_stmt(self, ctx):

        self.visit(ctx.llamada_funcion())

        return None

    # EXPRESIONES

    def obtener_tipo_expr(self, ctx):

        if ctx is None:
            return 'error'

        if hasattr(ctx, 'llamada_funcion') and ctx.llamada_funcion():

            return self.visit(ctx.llamada_funcion())

        if hasattr(ctx, 'STRING') and ctx.STRING():
            return 'shen'

        if hasattr(ctx, 'INT') and ctx.INT():
            return 'ontie'

        if hasattr(ctx, 'FLOAT_LIT') and ctx.FLOAT_LIT():
            return 'duble'

        if hasattr(ctx, 'ID') and ctx.ID():

            nombre = ctx.ID().getText()

            tipo = self.buscar_variable(nombre)

            if tipo is None:

                self._error(
                    ctx,
                    f"Variable '{nombre}' usada sin declarar"
                )

                return 'error'

            return tipo

        if ctx.getChildCount() == 3:

            tipo_izq = self.obtener_tipo_expr(
                ctx.getChild(0)
            )

            tipo_der = self.obtener_tipo_expr(
                ctx.getChild(2)
            )

            op = ctx.getChild(1).getText()

            if tipo_izq == 'error' or tipo_der == 'error':
                return 'error'

            if tipo_izq == 'shen' or tipo_der == 'shen':

                if op == 'plu':

                    if tipo_izq == 'shen' and tipo_der == 'shen':
                        return 'shen'

                self._error(
                    ctx,
                    "Operacion invalida con string"
                )

                return 'error'

            if tipo_izq in ['ontie', 'flote', 'duble'] and \
               tipo_der in ['ontie', 'flote', 'duble']:

                if op in ['plu', 'moan', 'par', 'bag']:

                    return self.promocion(
                        tipo_izq,
                        tipo_der
                    )

                if op in ['minog', 'aye', 'compag']:

                    return 'ontie'

        if ctx.getChildCount() == 1:

            return self.obtener_tipo_expr(
                ctx.getChild(0)
            )

        return 'error'

    # PROMOCION

    def promocion(self, t1, t2):

        if 'duble' in [t1, t2]:
            return 'duble'

        if 'flote' in [t1, t2]:
            return 'flote'

        return 'ontie'

    # COMPATIBILIDAD

    def es_compatible(self, destino, origen):

        if destino == origen:
            return True

        if destino == 'duble':

            if origen in ['ontie', 'flote', 'duble']:
                return True

        if destino == 'flote':

            if origen in ['ontie', 'flote']:
                return True

        return False

    # VISITORS RESTANTES

    def visitExpr(self, ctx):

        return self.visitChildren(ctx)

    def visitExpr_entera(self, ctx):

        return self.visitChildren(ctx)

    def visitExpr_decimal(self, ctx):

        return self.visitChildren(ctx)

    def visitExpr_string(self, ctx):

        return self.visitChildren(ctx)

    def visitTipo(self, ctx):

        return self.visitChildren(ctx)

    def visitErrorInstr(self, ctx):

        return self.visitChildren(ctx)