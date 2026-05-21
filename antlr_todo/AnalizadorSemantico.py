from antlr4 import *
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.LenguajeVisitor import LenguajeVisitor

class AnalizadorSemantico(LenguajeVisitor):

    def __init__(self):
        # Tabla de símbolos por función: { 'global': {var: tipo}, 'funcionX': {...} }
        self.tabla_por_funcion = {'global': {}}
        self.funcion_actual = 'global'

        # Tabla de funciones: { nombre: { 'retorno': tipo, 'params': [(tipo, nombre)] } }
        self.tabla_funciones = {}

        self.errores = []
        self._dentro_loop = 0
        self._dentro_switch = 0
        self.pila_scopes = [{}]      # pila de tablas locales durante el análisis
    @property
    def tabla_simbolos(self):
        """Retorna un diccionario plano con todas las variables de todas las funciones."""
        flat = {}
        for func_vars in self.tabla_por_funcion.values():
            flat.update(func_vars)
        return flat
    # ========== HELPERS ==========

    def abrir_scope(self):
        self.pila_scopes.append({})

    def cerrar_scope(self):
        if len(self.pila_scopes) > 1:
            self.pila_scopes.pop()

    def declarar_variable(self, nombre, tipo, ctx):
        scope_actual = self.pila_scopes[-1]
        if nombre in scope_actual:
            self._error(ctx, f"Variable '{nombre}' ya fue declarada")
            return False

        scope_actual[nombre] = tipo

        # Guardar en la tabla global por función
        self.tabla_por_funcion.setdefault(self.funcion_actual, {})[nombre] = tipo
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
            'vid': 'void (vid)'
        }.get(tipo, tipo)

    def _error(self, ctx, mensaje):
        try:
            token = ctx.start if hasattr(ctx, 'start') else ctx
            linea = token.line
            columna = token.column
        except:
            linea, columna = 0, 0
        self.errores.append({
            'linea': linea,
            'columna': columna,
            'mensaje': mensaje,
            'tipo': 'Semantico'
        })

    def _tipo_retorno(self, ctx):
        if ctx.ONTIE(): return 'ontie'
        if ctx.FLOTE(): return 'flote'
        if ctx.DUBLE(): return 'duble'
        if ctx.SHEN():  return 'shen'
        if ctx.VID():   return 'vid'
        return 'error'

    def es_compatible(self, destino, origen):
        if destino == origen: return True
        if destino == 'duble' and origen in ('ontie','flote','duble'): return True
        if destino == 'flote' and origen in ('ontie','flote'): return True
        return False

    def promocion(self, t1, t2):
        if 'duble' in (t1, t2): return 'duble'
        if 'flote' in (t1, t2): return 'flote'
        return 'ontie'

    def obtener_tipo_expr(self, ctx):
        """Retorna el tipo (ontie, flote, duble, shen) de una expresión."""
        if ctx is None:
            return 'error'

        # 1. Llamada a función
        if hasattr(ctx, 'llamada_funcion') and ctx.llamada_funcion():
            return self.visit(ctx.llamada_funcion())

        # 2. Literales numéricos y strings (terminales)
        if hasattr(ctx, 'INT') and ctx.INT():
            return 'ontie'
        if hasattr(ctx, 'FLOAT_LIT') and ctx.FLOAT_LIT():
            return 'duble'
        if hasattr(ctx, 'STRING') and ctx.STRING():
            return 'shen'

        # 3. Identificador (variable)
        if hasattr(ctx, 'ID') and ctx.ID():
            nombre = ctx.ID().getText()
            tipo = self.buscar_variable(nombre)
            if tipo is None:
                self._error(ctx, f"Variable '{nombre}' usada sin declarar")
                return 'error'
            return tipo

        # 4. Operación binaria (tiene exactamente 3 hijos)
        if ctx.getChildCount() == 3:
            izq = self.obtener_tipo_expr(ctx.getChild(0))
            der = self.obtener_tipo_expr(ctx.getChild(2))
            op = ctx.getChild(1).getText()

            if izq == 'error' or der == 'error':
                return 'error'

            # Concatenación de strings solo con '+'
            if izq == 'shen' or der == 'shen':
                if op == 'plu' and izq == 'shen' and der == 'shen':
                    return 'shen'
                self._error(ctx, "Operación inválida con string")
                return 'error'

            # Operaciones aritméticas y relacionales
            if izq in ('ontie', 'flote', 'duble') and der in ('ontie', 'flote', 'duble'):
                if op in ('plu', 'moan', 'par', 'bag'):   # + - * /
                    return self.promocion(izq, der)
                if op in ('minog', 'aye', 'compag'):      # < > ==
                    return 'ontie'

        # 5. Si es una expresión entre paréntesis u otro caso, explorar el único hijo
        if ctx.getChildCount() == 1:
            return self.obtener_tipo_expr(ctx.getChild(0))

        return 'error'

    # ========== VISITORS ==========

    def visitPrograma(self, ctx):
        for child in ctx.getChildren():
            self.visit(child)
        return None

    def visitBloque(self, ctx):
        self.abrir_scope()
        self.visitChildren(ctx)
        self.cerrar_scope()
        return None

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
        else:
            tipo = 'shen'
            tipo_expr = self.obtener_tipo_expr(ctx.expr_string())
        if not self.declarar_variable(nombre, tipo, ctx):
            return None
        if not self.es_compatible(tipo, tipo_expr):
            self._error(ctx, f"No se puede asignar {self._tipo_legible(tipo_expr)} a {self._tipo_legible(tipo)}")
        return None

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()
        tipo_var = self.buscar_variable(nombre)
        if tipo_var is None:
            self._error(ctx, f"Variable '{nombre}' usada sin declarar")
            return None
        tipo_expr = self.obtener_tipo_expr(ctx.expr())
        if not self.es_compatible(tipo_var, tipo_expr):
            self._error(ctx, f"No se puede asignar {self._tipo_legible(tipo_expr)} a {self._tipo_legible(tipo_var)}")
        return None

    def visitImpresion(self, ctx):
        self.obtener_tipo_expr(ctx.expr())
        return None

    def visitEntrada(self, ctx):
        nombre = ctx.ID().getText()
        if self.buscar_variable(nombre) is None:
            self._error(ctx, f"Variable '{nombre}' usada sin declarar")
        return None

    def visitCondicion_if(self, ctx):
        if self.obtener_tipo_expr(ctx.expr()) == 'shen':
            self._error(ctx, "La condición del wi no puede ser string")
        return self.visitChildren(ctx)

    def visitCiclo_while(self, ctx):
        if self.obtener_tipo_expr(ctx.expr()) == 'shen':
            self._error(ctx, "La condición del pendan no puede ser string")
        self._dentro_loop += 1
        self.visit(ctx.bloque())
        self._dentro_loop -= 1
        return None

    def visitCiclo_fer_pendan(self, ctx):
        self._dentro_loop += 1
        self.visit(ctx.bloque())
        self._dentro_loop -= 1
        if self.obtener_tipo_expr(ctx.expr()) == 'shen':
            self._error(ctx, "La condición del fer_pendan no puede ser string")
        return None

    def visitCiclo_pur(self, ctx):
        self.abrir_scope()
        self.visit(ctx.pur_init())
        if self.obtener_tipo_expr(ctx.expr()) == 'shen':
            self._error(ctx, "La condición del pur no puede ser string")
        self._dentro_loop += 1
        self.visit(ctx.pur_step())
        self.visit(ctx.bloque())
        self._dentro_loop -= 1
        self.cerrar_scope()
        return None

    def visitPur_init(self, ctx):
        nombre = ctx.ID().getText()
        if ctx.ONTIE() or ctx.FLOTE() or ctx.DUBLE() or ctx.SHEN():
            tipo = 'ontie' if ctx.ONTIE() else 'flote' if ctx.FLOTE() else 'duble' if ctx.DUBLE() else 'shen'
            self.declarar_variable(nombre, tipo, ctx)
        else:
            if self.buscar_variable(nombre) is None:
                self._error(ctx, f"Variable '{nombre}' usada sin declarar")
        return None

    def visitPur_step(self, ctx):
        nombre = ctx.ID().getText()
        if self.buscar_variable(nombre) is None:
            self._error(ctx, f"Variable '{nombre}' usada sin declarar")
        return None

    def visitCondicion_switch(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo != 'ontie' and tipo != 'error':
            self._error(ctx, "El shangshe solo acepta ontie")
        self._dentro_switch += 1
        self.visitChildren(ctx)
        self._dentro_switch -= 1
        return None

    def visitSentencia_pos(self, ctx):
        if self._dentro_loop == 0 and self._dentro_switch == 0:
            self._error(ctx, "pos solo puede usarse dentro de loop o switch")
        return None

    def visitSentencia_contine(self, ctx):
        if self._dentro_loop == 0:
            self._error(ctx, "contine solo puede usarse dentro de loop")
        return None

    def visitSentencia_su(self, ctx):
        return None

    def visitRetorno(self, ctx):
        if self.funcion_actual == 'global':
            return None
        tipo_esperado = self.tabla_funciones.get(self.funcion_actual, {}).get('retorno')
        if ctx.expr():
            tipo_expr = self.obtener_tipo_expr(ctx.expr())
            if not self.es_compatible(tipo_esperado, tipo_expr):
                self._error(ctx, f"La función debe retornar {self._tipo_legible(tipo_esperado)}")
        else:
            if tipo_esperado != 'vid':
                self._error(ctx, f"La función debe retornar {self._tipo_legible(tipo_esperado)}")
        return None

    def visitFuncion_def(self, ctx):
        nombre = ctx.ID().getText()
        tipo_ret = self._tipo_retorno(ctx.tipo_retorno())
        if nombre in self.tabla_funciones:
            self._error(ctx, f"Función '{nombre}' ya declarada")
            return None

        parametros = []
        if ctx.parametros():
            for p in ctx.parametros().parametro():
                if p.ONTIE(): tipo = 'ontie'
                elif p.FLOTE(): tipo = 'flote'
                elif p.DUBLE(): tipo = 'duble'
                else: tipo = 'shen'
                parametros.append((tipo, p.ID().getText()))

        self.tabla_funciones[nombre] = {'retorno': tipo_ret, 'params': parametros}

        # Cambiar a la nueva función
        funcion_anterior = self.funcion_actual
        self.funcion_actual = nombre
        self.tabla_por_funcion[nombre] = {}

        self.abrir_scope()
        for tipo, pnombre in parametros:
            self.declarar_variable(pnombre, tipo, ctx)
        self.visit(ctx.bloque())
        self.cerrar_scope()

        self.funcion_actual = funcion_anterior
        return None

    def visitLlamada_funcion(self, ctx):
        nombre = ctx.ID().getText()
        if nombre not in self.tabla_funciones:
            self._error(ctx, f"Función '{nombre}' no declarada")
            return 'error'
        info = self.tabla_funciones[nombre]
        params = info['params']
        args = ctx.argumentos().expr() if ctx.argumentos() else []
        if len(args) != len(params):
            self._error(ctx, f"Función '{nombre}' esperaba {len(params)} argumentos")
        else:
            for (tipo_param, _), arg in zip(params, args):
                tipo_arg = self.obtener_tipo_expr(arg)
                if not self.es_compatible(tipo_param, tipo_arg):
                    self._error(ctx, f"Argumento incompatible en llamada a '{nombre}'")
        return info['retorno']

    def visitLlamada_funcion_stmt(self, ctx):
        self.visit(ctx.llamada_funcion())
        return None

    # Los siguientes métodos ya están cubiertos por visitExpr y la herencia
    def visitExpr(self, ctx): return self.visitChildren(ctx)
    def visitExpr_entera(self, ctx): return self.visitChildren(ctx)
    def visitExpr_decimal(self, ctx): return self.visitChildren(ctx)
    def visitExpr_string(self, ctx): return self.visitChildren(ctx)