from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor
from antlr_todo.LenguajeParser import LenguajeParser   # ← Importación necesaria

class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo              = []
        self.temp_count          = 0
        self.label_count         = 0
        self.tabla               = dict(tabla_simbolos)
        self._break_label_stack  = []
        self._cont_label_stack   = []
        self._scope_stack        = [{}]   # nivel 0 = main
        self._locals_por_funcion = {}     # { func: { var: tipo } }
        self._funcion_actual     = None

    # HELPERS
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, line):
        self.codigo.append(line)

    def _push_scope(self):
        self._scope_stack.append({})

    def _pop_scope(self):
        if len(self._scope_stack) > 1:
            self._scope_stack.pop()

    def _declarar_local(self, nombre, tipo):
        self._scope_stack[-1][nombre] = tipo
        self.tabla[nombre] = tipo
        if self._funcion_actual is not None:
            self._locals_por_funcion.setdefault(self._funcion_actual, {})[nombre] = tipo
        else:
            self._locals_por_funcion.setdefault('__main__', {})[nombre] = tipo

    def _buscar_variable(self, nombre):
        for scope in reversed(self._scope_stack):
            if nombre in scope:
                return scope[nombre]
        return self.tabla.get(nombre)

    # PROGRAMA Y BLOQUES
    def visitPrograma(self, ctx):
        for f in ctx.funcion_def():
            self.visit(f)
        self.visit(ctx.bloque())
        return None

    def visitBloque(self, ctx):
        self._push_scope()
        self.visitChildren(ctx)
        self._pop_scope()
        return None

    def visitInstrucciones(self, ctx):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx):
        return self.visitChildren(ctx)

    # DECLARACION
    def visitDeclaracion(self, ctx):
        var = ctx.ID().getText()
        tipo = None
        if ctx.ONTIE(): tipo = 'ontie'
        elif ctx.FLOTE(): tipo = 'flote'
        elif ctx.DUBLE(): tipo = 'duble'
        elif ctx.SHEN(): tipo = 'shen'

        if tipo:
            self._declarar_local(var, tipo)

        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        elif ctx.expr_decimal():
            value = self.visit(ctx.expr_decimal())
        elif ctx.expr_string():
            value = self.visit(ctx.expr_string())
        else:
            value = '0'

        self.emit(f"{var} = {value}")
        return None

    # ASIGNACION
    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()
        if self._buscar_variable(var) is None:
            return
        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    # IMPRESION / ENTRADA
    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")

    def visitEntrada(self, ctx):
        var = ctx.ID().getText()
        self.emit(f"read {var}")

    # IF / ELSE
    def visitCondicion_if(self, ctx):
        cond = self.visit(ctx.expr())
        label_true = self.new_label()
        label_false = self.new_label()
        self.emit(f"if {cond} goto {label_true}")
        self.emit(f"goto {label_false}")
        self.emit(f"{label_true}:")
        self.visit(ctx.bloque(0))
        if ctx.OTRE():
            label_end = self.new_label()
            self.emit(f"goto {label_end}")
            self.emit(f"{label_false}:")
            self.visit(ctx.bloque(1))
            self.emit(f"{label_end}:")
        else:
            self.emit(f"{label_false}:")

    # WHILE
    def visitCiclo_while(self, ctx):
        label_start = self.new_label()
        label_body = self.new_label()
        label_end = self.new_label()
        self._break_label_stack.append(label_end)
        self._cont_label_stack.append(label_start)
        self.emit(f"{label_start}:")
        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {label_body}")
        self.emit(f"goto {label_end}")
        self.emit(f"{label_body}:")
        self.visit(ctx.bloque())
        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")
        self._break_label_stack.pop()
        self._cont_label_stack.pop()

    # DO-WHILE
    def visitCiclo_fer_pendan(self, ctx):
        label_start = self.new_label()
        label_cond = self.new_label()
        label_end = self.new_label()
        self._break_label_stack.append(label_end)
        self._cont_label_stack.append(label_cond)
        self.emit(f"{label_start}:")
        self.visit(ctx.bloque())
        self.emit(f"{label_cond}:")
        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {label_start}")
        self.emit(f"{label_end}:")
        self._break_label_stack.pop()
        self._cont_label_stack.pop()

    # FOR
    def visitCiclo_pur(self, ctx):
        self._push_scope()
        self.visit(ctx.pur_init())
        label_start = self.new_label()
        label_body = self.new_label()
        label_step = self.new_label()
        label_end = self.new_label()
        self._break_label_stack.append(label_end)
        self._cont_label_stack.append(label_step)
        self.emit(f"{label_start}:")
        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {label_body}")
        self.emit(f"goto {label_end}")
        self.emit(f"{label_body}:")
        self.visit(ctx.bloque())
        self.emit(f"{label_step}:")
        self.visit(ctx.pur_step())
        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")
        self._break_label_stack.pop()
        self._cont_label_stack.pop()
        self._pop_scope()

    def visitPur_init(self, ctx):
        var = ctx.ID().getText()
        tipo = None
        if ctx.ONTIE(): tipo = 'ontie'
        elif ctx.FLOTE(): tipo = 'flote'
        elif ctx.DUBLE(): tipo = 'duble'
        elif ctx.SHEN(): tipo = 'shen'
        if tipo:
            self._declarar_local(var, tipo)
        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        elif ctx.expr_decimal():
            value = self.visit(ctx.expr_decimal())
        elif ctx.expr_string():
            value = self.visit(ctx.expr_string())
        elif ctx.expr():
            value = self.visit(ctx.expr())
        else:
            value = '0'
        self.emit(f"{var} = {value}")

    def visitPur_step(self, ctx):
        var = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    # SWITCH
    def visitCondicion_switch(self, ctx):
        expr_val = self.visit(ctx.expr())
        label_end = self.new_label()
        casos = ctx.caso_switch()
        labels = [self.new_label() for _ in casos]
        label_default = self.new_label() if ctx.caso_default() else label_end
        self._break_label_stack.append(label_end)
        for i, caso in enumerate(casos):
            val = caso.INT().getText()
            temp = self.new_temp()
            self.emit(f"{temp} = {expr_val} compag {val}")
            self.emit(f"if {temp} goto {labels[i]}")
        self.emit(f"goto {label_default}")
        for i, caso in enumerate(casos):
            self.emit(f"{labels[i]}:")
            self.visit(caso.instrucciones())
        if ctx.caso_default():
            self.emit(f"{label_default}:")
            self.visit(ctx.caso_default().instrucciones())
        self.emit(f"{label_end}:")
        self._break_label_stack.pop()

    def visitCaso_switch(self, ctx):
        return self.visitChildren(ctx)

    def visitCaso_default(self, ctx):
        return self.visitChildren(ctx)

    # BREAK / CONTINUE / GOTO
    def visitSentencia_pos(self, ctx):
        if self._break_label_stack:
            self.emit(f"goto {self._break_label_stack[-1]}")

    def visitSentencia_contine(self, ctx):
        if self._cont_label_stack:
            self.emit(f"goto {self._cont_label_stack[-1]}")

    def visitSentencia_su(self, ctx):
        self.emit(f"goto {ctx.ID().getText()}")

    # RETURN
    def visitRetorno(self, ctx):
        if ctx.expr():
            value = self.visit(ctx.expr())
            self.emit(f"return {value}")
        else:
            self.emit("return")

    # FUNCIONES
    def visitFuncion_def(self, ctx):
        nombre = ctx.ID().getText()
        self._funcion_actual = nombre
        self._locals_por_funcion[nombre] = {}
        tabla_anterior = dict(self.tabla)
        self._push_scope()
        for p in ctx.parametros().parametro():
            pid = p.ID().getText()
            if p.ONTIE(): tipo = 'ontie'
            elif p.FLOTE(): tipo = 'flote'
            elif p.DUBLE(): tipo = 'duble'
            elif p.SHEN(): tipo = 'shen'
            else: tipo = 'ontie'
            self._declarar_local(pid, tipo)
        self.emit(f"func_begin {nombre}")
        for p in ctx.parametros().parametro():
            self.emit(f"param_decl {p.ID().getText()}")
        self.visit(ctx.bloque())
        self.emit(f"func_end {nombre}")
        self._pop_scope()
        self.tabla = tabla_anterior
        self._funcion_actual = None

    def visitParametros(self, ctx): return None
    def visitParametro(self, ctx): return None
    def visitTipo_retorno(self, ctx): return None

    # LLAMADAS A FUNCION - CORREGIDO (usando ctx.argumentos().expr())
    def visitLlamada_funcion(self, ctx):
        nombre = ctx.ID().getText()
        # Procesar cada argumento usando la lista de expresiones
        if ctx.argumentos():
            for expr_ctx in ctx.argumentos().expr():
                val = self.visit(expr_ctx)
                self.emit(f"arg {val}")
        temp = self.new_temp()
        self.emit(f"{temp} = call {nombre}")
        return temp

    def visitLlamada_funcion_stmt(self, ctx):
        llamada = ctx.llamada_funcion()
        nombre = llamada.ID().getText()
        if llamada.argumentos():
            for expr_ctx in llamada.argumentos().expr():
                val = self.visit(expr_ctx)
                self.emit(f"arg {val}")
        self.emit(f"call {nombre}")

    def visitArgumentos(self, ctx):
        return None   # Ya se procesaron en las llamadas

    # EXPRESIONES
    def visitExpr(self, ctx):
        if ctx.llamada_funcion():
            return self.visit(ctx.llamada_funcion())
        if ctx.getChildCount() == 1:
            return ctx.getText()
        left = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))
        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_entera(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()
        left = self.visit(ctx.expr_entera(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_entera(1))
        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_decimal(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()
        left = self.visit(ctx.expr_decimal(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_decimal(1))
        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_string(self, ctx):
        return ctx.getText()

    def visitErrorInstr(self, ctx): pass
    def visitTipo(self, ctx): return None

    def get_codigo(self):
        return "\n".join(self.codigo)


# ══════════════════════════════════════════════════════════════
#  TRADUCTOR C3D → C++
# ══════════════════════════════════════════════════════════════

class C3DAC_Traductor:

    OP_MAP = {
        'plu':    '+',
        'moan':   '-',
        'par':    '*',
        'bag':    '/',
        'minog':  '<',
        'mayog':  '>',
        'compag': '==',
        'difer':  '!=',
    }

    TIPO_C = {
        'ontie': 'int',
        'flote': 'float',
        'duble': 'double',
        'shen':  'const char*',
        'vid':   'void',
    }

    def __init__(self, codigo_c3d, tabla_simbolos,
                 tabla_funciones=None, locals_por_funcion=None):
        self.lineas             = codigo_c3d
        self.tabla              = tabla_simbolos
        self.tabla_funciones    = tabla_funciones or {}
        self.locals_por_funcion = locals_por_funcion or {}

    def _tc(self, tipo):
        return self.TIPO_C.get(tipo, 'double')

    def _es_temp(self, s):
        return s.startswith('t') and s[1:].isdigit()

    def _expr(self, e):
        import re
        for op_l, op_c in self.OP_MAP.items():
            e = re.sub(r'\b' + re.escape(op_l) + r'\b', op_c, e)
        return e

    def _es_shen(self, val):
        return val.startswith('"') or self.tabla.get(val, '') == 'shen'

    def _separar(self):
        funciones = {}
        main = []
        actual = None
        for linea in self.lineas:
            l = linea.strip()
            if l.startswith('func_begin '):
                actual = l[11:].strip()
                funciones[actual] = []
            elif l.startswith('func_end '):
                actual = None
            elif actual is not None:
                funciones[actual].append(linea)
            else:
                main.append(linea)
        return funciones, main

    def _decl_locales(self, nombre_funcion, excluir=None):
        locales = self.locals_por_funcion.get(nombre_funcion, {})
        excluir = excluir or set()
        lines = []
        for nombre, tipo in locales.items():
            if nombre in excluir:
                continue
            if tipo == 'shen':
                lines.append(f'    const char* {nombre} = "";')
            elif tipo in ('flote', 'duble'):
                lines.append(f'    {self._tc(tipo)} {nombre} = 0.0;')
            else:
                lines.append(f'    {self._tc(tipo)} {nombre} = 0;')
        return lines

    def _decl_temps(self, lineas):
        import re
        temps = set()
        for l in lineas:
            ls = l.strip()
            if '=' in ls and not ls.endswith(':') and not ls.startswith('func_') and not ls.startswith('param_decl') and not ls.startswith('arg ') and not ls.startswith('call '):
                dest = ls.split('=')[0].strip()
                if self._es_temp(dest):
                    temps.add(dest)
        return [f'    double {t};' for t in sorted(temps, key=lambda x: int(x[1:]))]

    def _traducir_bloque(self, lineas, indent='    '):
        resultado = []
        args_buf = []
        for linea in lineas:
            l = linea.strip()
            if not l:
                continue
            if l.endswith(':') and ' ' not in l:
                resultado.append(f'{indent}{l}')
                continue
            if l.startswith('arg '):
                args_buf.append(self._expr(l[4:].strip()))
                continue
            if l.startswith('param_decl '):
                continue
            if '= call ' in l:
                dest = l.split('=')[0].strip()
                after_call = l.split('call ')[1].strip()
                nombre = after_call.split()[0]
                args = ', '.join(args_buf)
                args_buf = []
                resultado.append(f'{indent}{dest} = {nombre}({args});')
                continue
            if l.startswith('call '):
                after_call = l[5:].strip()
                nombre = after_call.split()[0]
                args = ', '.join(args_buf)
                args_buf = []
                resultado.append(f'{indent}{nombre}({args});')
                continue
            if l.startswith('print '):
                val = self._expr(l[6:].strip())
                if self._es_shen(val):
                    resultado.append(f'{indent}printf("%s\\\\n", {val});')
                else:
                    resultado.append(f'{indent}printf("%g\\\\n", (double)({val}));')
                continue
            if l.startswith('read '):
                var = l[5:].strip()
                tipo = self.tabla.get(var, 'ontie')
                fmt = {'ontie': '%d', 'flote': '%f', 'duble': '%lf', 'shen': '%s'}.get(tipo, '%d')
                resultado.append(f'{indent}scanf("{fmt}", &{var});')
                continue
            if l.startswith('return'):
                resto = l[6:].strip()
                if resto:
                    resultado.append(f'{indent}return {self._expr(resto)};')
                else:
                    resultado.append(f'{indent}return;')
                continue
            if l.startswith('if '):
                parts = l.split()
                goto_idx = parts.index('goto')
                cond = ' '.join(parts[1:goto_idx])
                label = parts[-1]
                resultado.append(f'{indent}if ({self._expr(cond)}) goto {label};')
                continue
            if l.startswith('goto '):
                resultado.append(f'{indent}goto {l.split()[1]};')
                continue
            if '=' in l:
                dest, resto = l.split('=', 1)
                resultado.append(f'{indent}{dest.strip()} = {self._expr(resto.strip())};')
                continue
            resultado.append(f'{indent}// {l}')
        return resultado

    def generar_cpp(self):
        funciones, main_lineas = self._separar()
        cpp = ['#include <stdio.h>', '#include <stdlib.h>', '']

        # forward declarations
        for nombre, info in self.tabla_funciones.items():
            tipo_r = self._tc(info.get('retorno', 'vid'))
            params = info.get('params', [])
            param_str = ', '.join(f"{self._tc(t)} {n}" for t, n in params)
            cpp.append(f'{tipo_r} {nombre}({param_str});')
        if self.tabla_funciones:
            cpp.append('')

        # definiciones de funciones
        for nombre, lineas_func in funciones.items():
            info = self.tabla_funciones.get(nombre, {})
            tipo_r = self._tc(info.get('retorno', 'vid'))
            params = info.get('params', [])
            param_str = ', '.join(f"{self._tc(t)} {n}" for t, n in params)
            param_set = {n for _, n in params}
            cpp.append(f'{tipo_r} {nombre}({param_str}) {{')
            decl_loc = self._decl_locales(nombre, excluir=param_set)
            decl_tmp = self._decl_temps(lineas_func)
            for d in decl_loc: cpp.append(d)
            for d in decl_tmp: cpp.append(d)
            if decl_loc or decl_tmp:
                cpp.append('')
            cpp += self._traducir_bloque(lineas_func)
            cpp.append('}')
            cpp.append('')

        # main
        cpp.append('int main() {')
        decl_main = self._decl_locales('__main__')
        decl_tmp = self._decl_temps(main_lineas)
        for d in decl_main: cpp.append(d)
        for d in decl_tmp: cpp.append(d)
        if decl_main or decl_tmp:
            cpp.append('')
        cpp += self._traducir_bloque(main_lineas)
        ultimas = [l.strip() for l in self._traducir_bloque(main_lineas) if l.strip()]
        if not (ultimas and ultimas[-1].startswith('return')):
            cpp.append('')
            cpp.append('    return 0;')
        cpp.append('}')
        return '\n'.join(cpp)

    def guardar(self, ruta='salida.cpp'):
        contenido = self.generar_cpp()
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return contenido