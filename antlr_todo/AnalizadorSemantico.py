from antlr4 import *
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class AnalizadorSemantico(LenguajeVisitor):

    def __init__(self):
        self.tabla_simbolos  = {}   # nombre -> tipo  global
        self.tabla_funciones = {}   # nombre -> { retorno, params: [(tipo, nombre)] }
        self.errores         = []
        self._scope_funcion  = None # tipo de retorno de la funcion actual
        self._dentro_loop    = 0    # contador de loops anidados
        self._dentro_switch  = 0    # contador de switch anidados

    #helper: tipo legibl    
    def _tipo_legible(self, tipo):
        return {
            'ontie': 'int (ontie)',
            'flote': 'float (flote)',
            'duble': 'double (duble)',
            'shen':  'varchar (shen)',
            'vid':   'void (vid)',
            'error': 'desconocido',
        }.get(tipo, tipo)

    #helper: agregar erro
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
            'tipo':    'Semantico',
        })

    #helper: tipo de retorno legibl    
    def _tipo_retorno(self, ctx):
        if ctx.ONTIE(): return 'ontie'
        if ctx.FLOTE(): return 'flote'
        if ctx.DUBLE(): return 'duble'
        if ctx.SHEN():  return 'shen'
        if ctx.VID():   return 'vid'
        return 'error'

    #helper: obtiene expr_string de declaracion she    
    def _get_expr_string(self, ctx):
        if hasattr(ctx, 'expr_string') and callable(ctx.expr_string):
            try:
                r = ctx.expr_string()
                if r is not None:
                    return r
            except Exception:
                pass
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if hasattr(child, 'STRING') and child.STRING():
                return child
        return None

    
    #  PROGRAMA
    

    def visitPrograma(self, ctx: LenguajeParser.ProgramaContext):
        # visitar primero todas las definiciones de funciones
        for child in ctx.getChildren():
            self.visit(child)
        return None

    
    #  BLOQUE / INSTRUCCIONES
    

    def visitBloque(self, ctx: LenguajeParser.BloqueContext):
        return self.visitChildren(ctx)

    def visitInstrucciones(self, ctx: LenguajeParser.InstruccionesContext):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx: LenguajeParser.InstruccionContext):
        return self.visitChildren(ctx)

    
    #  DECLARACION
    

    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()

        if nombre in self.tabla_simbolos:
            self._error(ctx,
                f"Variable '{nombre}' ya fue declarada como "
                f"{self._tipo_legible(self.tabla_simbolos[nombre])}")
            return

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
            tipo_expr = self.obtener_tipo_expr(self._get_expr_string(ctx))
        else:
            return

        if not self.es_compatible(tipo, tipo_expr):
            self._error(ctx,
                f"No se puede asignar {self._tipo_legible(tipo_expr)} "
                f"a {self._tipo_legible(tipo)} en '{nombre}'")
            return

        self.tabla_simbolos[nombre] = tipo

    
    #  ASIGNACION
    

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()

        if nombre not in self.tabla_simbolos:
            self._error(ctx, f"Variable '{nombre}' usada sin declarar")
            return

        tipo_var  = self.tabla_simbolos[nombre]
        tipo_expr = self.obtener_tipo_expr(ctx.expr())

        if not self.es_compatible(tipo_var, tipo_expr):
            self._error(ctx,
                f"No se puede asignar {self._tipo_legible(tipo_expr)} "
                f"a {self._tipo_legible(tipo_var)} en '{nombre}'")

    
    #  IMPRESION
    

    def visitImpresion(self, ctx):
        self.obtener_tipo_expr(ctx.expr())
        return self.visitChildren(ctx)

    
    #  ENTRADA  lirf(x) puavir
    

    def visitEntrada(self, ctx):
        nombre = ctx.ID().getText()
        if nombre not in self.tabla_simbolos:
            self._error(ctx,
                f"Variable '{nombre}' usada en lirf sin declarar")

    
    #  IF / ELSE
    

    def visitCondicion_if(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo == 'shen':
            self._error(ctx,
                "La condicion del wi no puede ser de tipo varchar (shen)")
        return self.visitChildren(ctx)

    
    #  WHILE
    

    def visitCiclo_while(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo == 'shen':
            self._error(ctx,
                "La condicion del pendan no puede ser de tipo varchar (shen)")
        self._dentro_loop += 1
        self.visit(ctx.bloque())
        self._dentro_loop -= 1
        return None

    
    #  DO-WHILE
    

    def visitCiclo_fer_pendan(self, ctx):
        self._dentro_loop += 1
        self.visit(ctx.bloque())
        self._dentro_loop -= 1
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo == 'shen':
            self._error(ctx,
                "La condicion del fer_pendan no puede ser de tipo varchar (shen)")
        return None

    
    #  FOR
    

    def visitCiclo_pur(self, ctx):
        # visitar init (puede declarar variable nueva)
        self.visit(ctx.pur_init())
        # validar condicion
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo == 'shen':
            self._error(ctx,
                "La condicion del pur no puede ser de tipo varchar (shen)")
        # visitar step y bloque dentro del loop
        self._dentro_loop += 1
        self.visit(ctx.pur_step())
        self.visit(ctx.bloque())
        self._dentro_loop -= 1
        return None

    def visitPur_init(self, ctx):
        # si declara variable nueva, agregarla a la tabla
        if ctx.ID() and ctx.IGUAL():
            nombre = ctx.ID().getText()
            if ctx.ONTIE():
                tipo = 'ontie'
            elif ctx.FLOTE():
                tipo = 'flote'
            elif ctx.DUBLE():
                tipo = 'duble'
            elif ctx.SHEN():
                tipo = 'shen'
            else:
                # asignacion simple sin tipo
                if nombre not in self.tabla_simbolos:
                    self._error(ctx,
                        f"Variable '{nombre}' usada en pur sin declarar")
                return
            # declaracion nueva dentro del for
            if nombre not in self.tabla_simbolos:
                self.tabla_simbolos[nombre] = tipo
        return self.visitChildren(ctx)

    def visitPur_step(self, ctx):
        nombre = ctx.ID().getText()
        if nombre not in self.tabla_simbolos:
            self._error(ctx,
                f"Variable '{nombre}' usada en incremento de pur sin declarar")
        return self.visitChildren(ctx)

    
    #  SWITCH / CASE / DEFAULT
    

    def visitCondicion_switch(self, ctx):
        tipo = self.obtener_tipo_expr(ctx.expr())
        if tipo != 'ontie' and tipo != 'error':
            self._error(ctx,
                f"El shangshe solo acepta int (ontie), "
                f"se recibio {self._tipo_legible(tipo)}")
        self._dentro_switch += 1
        self.visitChildren(ctx)
        self._dentro_switch -= 1
        return None

    def visitCaso_switch(self, ctx):
        return self.visitChildren(ctx)

    def visitCaso_default(self, ctx):
        return self.visitChildren(ctx)

    
    #  BREAK / CONTINUE
    

    def visitSentencia_pos(self, ctx):
        if self._dentro_loop == 0 and self._dentro_switch == 0:
            self._error(ctx,
                "pos (break) solo puede usarse dentro de un loop o shangshe")

    def visitSentencia_contine(self, ctx):
        if self._dentro_loop == 0:
            self._error(ctx,
                "contine (continue) solo puede usarse dentro de un loop")

    
    #  GOTO
    

    def visitSentencia_su(self, ctx):
        # goto no requiere validacion semantica adicional
        pass

    
    #  RETURN
    

    def visitRetorno(self, ctx):
        if ctx.expr():
            tipo_expr = self.obtener_tipo_expr(ctx.expr())
            if self._scope_funcion and self._scope_funcion != 'vid':
                if not self.es_compatible(self._scope_funcion, tipo_expr):
                    self._error(ctx,
                        f"La funcion retorna {self._tipo_legible(self._scope_funcion)} "
                        f"pero se encontro {self._tipo_legible(tipo_expr)}")
        elif self._scope_funcion and self._scope_funcion != 'vid':
            self._error(ctx,
                f"La funcion debe retornar {self._tipo_legible(self._scope_funcion)}")
        return None

    
    #  FUNCIONES
    

    def visitFuncion_def(self, ctx):
        nombre       = ctx.ID().getText()
        tipo_ret     = self._tipo_retorno(ctx.tipo_retorno())

        # recoger parametros
        params = []
        for p in ctx.parametros().parametro():
            if p.ONTIE():   t = 'ontie'
            elif p.FLOTE(): t = 'flote'
            elif p.DUBLE(): t = 'duble'
            elif p.SHEN():  t = 'shen'
            else:           t = 'error'
            params.append((t, p.ID().getText()))

        if nombre in self.tabla_funciones:
            self._error(ctx,
                f"Funcion '{nombre}' ya fue declarada anteriormente")
            return

        self.tabla_funciones[nombre] = {
            'retorno': tipo_ret,
            'params':  params,
        }

        # guardar scope anterior y abrir scope de funcion
        scope_anterior   = self._scope_funcion
        tabla_anterior   = dict(self.tabla_simbolos)

        self._scope_funcion = tipo_ret

        # agregar parametros al scope local
        for t, n in params:
            self.tabla_simbolos[n] = t

        self.visit(ctx.bloque())

        # restaurar scope anterior
        self._scope_funcion  = scope_anterior
        self.tabla_simbolos  = tabla_anterior

        return None

    def visitTipo_retorno(self, ctx):
        return self.visitChildren(ctx)

    def visitParametros(self, ctx):
        return self.visitChildren(ctx)

    def visitParametro(self, ctx):
        return self.visitChildren(ctx)

    
    #  LLAMADA A FUNCION
    

    def visitLlamada_funcion(self, ctx):
        nombre = ctx.ID().getText()

        if nombre not in self.tabla_funciones:
            self._error(ctx,
                f"Funcion '{nombre}' no declarada")
            return 'error'

        info   = self.tabla_funciones[nombre]
        params = info['params']
        args   = ctx.argumentos().expr() if ctx.argumentos() else []

        if len(args) != len(params):
            self._error(ctx,
                f"Funcion '{nombre}' espera {len(params)} "
                f"argumento(s) pero recibio {len(args)}")
        else:
            for (tipo_p, nombre_p), arg in zip(params, args):
                tipo_a = self.obtener_tipo_expr(arg)
                if not self.es_compatible(tipo_p, tipo_a):
                    self._error(ctx,
                        f"Argumento '{nombre_p}' de '{nombre}': "
                        f"se esperaba {self._tipo_legible(tipo_p)} "
                        f"pero se recibio {self._tipo_legible(tipo_a)}")

        return info['retorno']

    def visitArgumentos(self, ctx):
        return self.visitChildren(ctx)

    def visitLlamada_funcion_stmt(self, ctx):
        self.visit(ctx.llamada_funcion())

    
    #  VALIDACION DE EXPRESIONES
    

    def obtener_tipo_expr(self, ctx):
        if ctx is None:
            return 'error'

        # llamada a funcion dentro de expr
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
            if nombre not in self.tabla_simbolos:
                self._error(ctx,
                    f"Variable '{nombre}' usada sin declarar")
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
                self._error(ctx,
                    f"No se puede operar '{op}' entre "
                    f"{self._tipo_legible(tipo_izq)} y "
                    f"{self._tipo_legible(tipo_der)}")
                return 'error'

            if tipo_izq in ['ontie','flote','duble'] and \
               tipo_der in ['ontie','flote','duble']:
                if op in ['plu','moan','par','bag']:
                    return self.promocion(tipo_izq, tipo_der)
                if op in ['minog','aye','compag']:
                    return 'ontie'

            self._error(ctx,
                f"Operacion invalida: "
                f"{self._tipo_legible(tipo_izq)} {op} "
                f"{self._tipo_legible(tipo_der)}")
            return 'error'

        # nodo con un solo hijo — delegar
        if ctx.getChildCount() == 1:
            return self.obtener_tipo_expr(ctx.getChild(0))

        return 'error'

    
    #  PROMOCION Y COMPATIBILIDAD
    

    def promocion(self, t1, t2):
        if 'duble' in (t1, t2): return 'duble'
        if 'flote' in (t1, t2): return 'flote'
        return 'ontie'

    def es_compatible(self, destino, origen):
        if destino == origen:
            return True
        if destino in ['duble','flote'] and origen in ['ontie','flote','duble']:
            return True
        if destino == 'shen' and origen != 'shen':
            return False
        if destino != 'shen' and origen == 'shen':
            return False
        if destino == 'ontie' and origen in ['flote','duble']:
            return False
        return False

    
    #  VISITORS RESTANTES
    

    def visitExpr(self, ctx: LenguajeParser.ExprContext):
        return self.visitChildren(ctx)

    def visitExpr_entera(self, ctx: LenguajeParser.Expr_enteraContext):
        return self.visitChildren(ctx)

    def visitExpr_decimal(self, ctx: LenguajeParser.Expr_decimalContext):
        return self.visitChildren(ctx)

    def visitExpr_string(self, ctx):
        return self.visitChildren(ctx)

    def visitTipo(self, ctx: LenguajeParser.TipoContext):
        return self.visitChildren(ctx)

    def visitErrorInstr(self, ctx: LenguajeParser.ErrorInstrContext):
        return self.visitChildren(ctx)