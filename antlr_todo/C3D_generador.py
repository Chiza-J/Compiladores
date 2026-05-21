from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor
from antlr_todo.LenguajeParser import LenguajeParser

class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0
        self.tabla = dict(tabla_simbolos)                     # ← usado en generar_c3d.py
        self._break_label_stack = []                          # ← nombre esperado (opcional)
        self._cont_label_stack = []                           # ← nombre esperado
        self._scope_stack = [{}]                              # ← scopes locales
        self._locals_por_funcion = {}                         # ← ¡nombre clave!
        self._funcion_actual = None

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
            val = self.visit(ctx.expr_entera())
        elif ctx.expr_decimal():
            val = self.visit(ctx.expr_decimal())
        elif ctx.expr_string():
            val = self.visit(ctx.expr_string())
        else:
            val = '0'
        self.emit(f"{var} = {val}")
        return None

    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()
        if self._buscar_variable(var) is None:
            return
        val = self.visit(ctx.expr())
        self.emit(f"{var} = {val}")

    def visitImpresion(self, ctx):
        val = self.visit(ctx.expr())
        self.emit(f"print {val}")

    def visitEntrada(self, ctx):
        var = ctx.ID().getText()
        self.emit(f"read {var}")

    # IF / ELSE
    def visitCondicion_if(self, ctx):
        cond = self.visit(ctx.expr())
        l_true = self.new_label()
        l_false = self.new_label()
        self.emit(f"if {cond} goto {l_true}")
        self.emit(f"goto {l_false}")
        self.emit(f"{l_true}:")
        self.visit(ctx.bloque(0))
        if ctx.OTRE():
            l_end = self.new_label()
            self.emit(f"goto {l_end}")
            self.emit(f"{l_false}:")
            self.visit(ctx.bloque(1))
            self.emit(f"{l_end}:")
        else:
            self.emit(f"{l_false}:")

    # WHILE
    def visitCiclo_while(self, ctx):
        l_start = self.new_label()
        l_body = self.new_label()
        l_end = self.new_label()
        self._break_label_stack.append(l_end)
        self._cont_label_stack.append(l_start)
        self.emit(f"{l_start}:")
        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {l_body}")
        self.emit(f"goto {l_end}")
        self.emit(f"{l_body}:")
        self.visit(ctx.bloque())
        self.emit(f"goto {l_start}")
        self.emit(f"{l_end}:")
        self._break_label_stack.pop()
        self._cont_label_stack.pop()

    # DO-WHILE
    def visitCiclo_fer_pendan(self, ctx):
        l_start = self.new_label()
        l_cond = self.new_label()
        l_end = self.new_label()
        self._break_label_stack.append(l_end)
        self._cont_label_stack.append(l_cond)
        self.emit(f"{l_start}:")
        self.visit(ctx.bloque())
        self.emit(f"{l_cond}:")
        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {l_start}")
        self.emit(f"{l_end}:")
        self._break_label_stack.pop()
        self._cont_label_stack.pop()

    # FOR
    def visitCiclo_pur(self, ctx):
        self._push_scope()
        self.visit(ctx.pur_init())
        l_start = self.new_label()
        l_body = self.new_label()
        l_step = self.new_label()
        l_end = self.new_label()
        self._break_label_stack.append(l_end)
        self._cont_label_stack.append(l_step)
        self.emit(f"{l_start}:")
        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {l_body}")
        self.emit(f"goto {l_end}")
        self.emit(f"{l_body}:")
        self.visit(ctx.bloque())
        self.emit(f"{l_step}:")
        self.visit(ctx.pur_step())
        self.emit(f"goto {l_start}")
        self.emit(f"{l_end}:")
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
            val = self.visit(ctx.expr_entera())
        elif ctx.expr_decimal():
            val = self.visit(ctx.expr_decimal())
        elif ctx.expr_string():
            val = self.visit(ctx.expr_string())
        elif ctx.expr():
            val = self.visit(ctx.expr())
        else:
            val = '0'
        self.emit(f"{var} = {val}")

    def visitPur_step(self, ctx):
        var = ctx.ID().getText()
        val = self.visit(ctx.expr())
        self.emit(f"{var} = {val}")

    # SWITCH
    def visitCondicion_switch(self, ctx):
        expr_val = self.visit(ctx.expr())
        l_end = self.new_label()
        casos = ctx.caso_switch()
        labels = [self.new_label() for _ in casos]
        l_default = self.new_label() if ctx.caso_default() else l_end
        self._break_label_stack.append(l_end)
        for i, c in enumerate(casos):
            const = c.INT().getText()
            t = self.new_temp()
            self.emit(f"{t} = {expr_val} compag {const}")
            self.emit(f"if {t} goto {labels[i]}")
        self.emit(f"goto {l_default}")
        for i, c in enumerate(casos):
            self.emit(f"{labels[i]}:")
            self.visit(c.instrucciones())
        if ctx.caso_default():
            self.emit(f"{l_default}:")
            self.visit(ctx.caso_default().instrucciones())
        self.emit(f"{l_end}:")
        self._break_label_stack.pop()

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
            val = self.visit(ctx.expr())
            self.emit(f"return {val}")
        else:
            self.emit("return")

    # FUNCIONES
    def visitFuncion_def(self, ctx):
        name = ctx.ID().getText()
        self._funcion_actual = name
        self._locals_por_funcion[name] = {}
        old_tabla = dict(self.tabla)
        self._push_scope()
        for p in ctx.parametros().parametro():
            pname = p.ID().getText()
            if p.ONTIE(): tipo = 'ontie'
            elif p.FLOTE(): tipo = 'flote'
            elif p.DUBLE(): tipo = 'duble'
            elif p.SHEN(): tipo = 'shen'
            else: tipo = 'ontie'
            self._declarar_local(pname, tipo)
        self.emit(f"func_begin {name}")
        for p in ctx.parametros().parametro():
            self.emit(f"param_decl {p.ID().getText()}")
        self.visit(ctx.bloque())
        self.emit(f"func_end {name}")
        self._pop_scope()
        self.tabla = old_tabla
        self._funcion_actual = None

    # LLAMADAS A FUNCION
    def visitLlamada_funcion(self, ctx):
        name = ctx.ID().getText()
        if ctx.argumentos():
            for arg_expr in ctx.argumentos().expr():
                val = self.visit(arg_expr)
                self.emit(f"arg {val}")
        temp = self.new_temp()
        self.emit(f"{temp} = call {name}")
        return temp

    def visitLlamada_funcion_stmt(self, ctx):
        call = ctx.llamada_funcion()
        name = call.ID().getText()
        if call.argumentos():
            for arg_expr in call.argumentos().expr():
                val = self.visit(arg_expr)
                self.emit(f"arg {val}")
        self.emit(f"call {name}")

    def visitArgumentos(self, ctx):
        return None

    # EXPRESIONES (CORREGIDAS)
    def visitExpr(self, ctx):
        if ctx.llamada_funcion():
            return self.visit(ctx.llamada_funcion())
        if ctx.getChildCount() == 1:
            return ctx.getText()
        left = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))
        t = self.new_temp()
        self.emit(f"{t} = {left} {op} {right}")
        return t

    def visitExpr_entera(self, ctx):
        if ctx.llamada_funcion():
            return self.visit(ctx.llamada_funcion())
        if ctx.getChildCount() == 1:
            return ctx.getText()
        left = self.visit(ctx.expr_entera(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_entera(1))
        t = self.new_temp()
        self.emit(f"{t} = {left} {op} {right}")
        return t

    def visitExpr_decimal(self, ctx):
        if ctx.llamada_funcion():
            return self.visit(ctx.llamada_funcion())
        if ctx.getChildCount() == 1:
            return ctx.getText()
        left = self.visit(ctx.expr_decimal(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_decimal(1))
        t = self.new_temp()
        self.emit(f"{t} = {left} {op} {right}")
        return t

    def visitExpr_string(self, ctx):
        return ctx.getText()

    # IGNORADOS
    def visitParametros(self, ctx): return None
    def visitParametro(self, ctx): return None
    def visitTipo_retorno(self, ctx): return None
    def visitCaso_switch(self, ctx): return self.visitChildren(ctx)
    def visitCaso_default(self, ctx): return self.visitChildren(ctx)
    def visitErrorInstr(self, ctx): pass
    def visitTipo(self, ctx): return None

    def get_codigo(self):
        return "\n".join(self.codigo)


# ============================================================
# TRADUCTOR C3D → C++ (con \\n)
# ============================================================

class C3DAC_Traductor:

    OP_MAP = {
        'plu': '+', 'moan': '-', 'par': '*', 'bag': '/',
        'minog': '<', 'mayog': '>', 'compag': '==', 'difer': '!='
    }
    TIPO_C = {
        'ontie': 'int', 'flote': 'float', 'duble': 'double',
        'shen': 'const char*', 'vid': 'void'
    }

    def __init__(self, codigo_c3d, tabla_simbolos,
                 tabla_funciones=None, locals_por_funcion=None):
        self.lineas = codigo_c3d
        self.tabla = tabla_simbolos
        self.tabla_funciones = tabla_funciones or {}
        self.locals_por_funcion = locals_por_funcion or {}

    def _tc(self, t):
        return self.TIPO_C.get(t, 'double')

    def _es_temp(self, s):
        return s.startswith('t') and s[1:].isdigit()

    def _expr(self, e):
        import re
        for a, b in self.OP_MAP.items():
            e = re.sub(r'\b' + re.escape(a) + r'\b', b, e)
        return e

    def _es_shen(self, val):
        return val.startswith('"') or self.tabla.get(val, '') == 'shen'

    def _separar(self):
        funcs = {}
        main = []
        cur = None
        for l in self.lineas:
            ls = l.strip()
            if ls.startswith('func_begin '):
                cur = ls[11:].strip()
                funcs[cur] = []
            elif ls.startswith('func_end '):
                cur = None
            elif cur:
                funcs[cur].append(ls)
            else:
                main.append(ls)
        return funcs, main

    def _decl_locales(self, func, excl=None):
        excl = excl or set()
        lines = []
        for var, tip in self.locals_por_funcion.get(func, {}).items():
            if var in excl: continue
            if tip == 'shen':
                lines.append(f'    const char* {var} = "";')
            elif tip in ('flote', 'duble'):
                lines.append(f'    {self._tc(tip)} {var} = 0.0;')
            else:
                lines.append(f'    {self._tc(tip)} {var} = 0;')
        return lines

    def _decl_temps(self, lines):
        import re
        temps = set()
        for l in lines:
            if '=' in l and not l.endswith(':') and not l.startswith('func_') and not l.startswith('param_decl') and not l.startswith('arg ') and not l.startswith('call '):
                dst = l.split('=')[0].strip()
                if self._es_temp(dst):
                    temps.add(dst)
        return [f'    double {t};' for t in sorted(temps, key=lambda x: int(x[1:]))]

    def _traducir_bloque(self, lines, indent='    '):
        res = []
        args = []
        for l in lines:
            ls = l.strip()
            if not ls:
                continue
            if ls.endswith(':') and ' ' not in ls:
                res.append(f'{indent}{ls}')
                continue
            if ls.startswith('arg '):
                args.append(self._expr(ls[4:].strip()))
                continue
            if ls.startswith('param_decl '):
                continue
            if '= call ' in ls:
                dst = ls.split('=')[0].strip()
                after = ls.split('call ')[1].strip()
                name = after.split()[0]
                res.append(f'{indent}{dst} = {name}({", ".join(args)});')
                args = []
                continue
            if ls.startswith('call '):
                after = ls[5:].strip()
                name = after.split()[0]
                res.append(f'{indent}{name}({", ".join(args)});')
                args = []
                continue
            if ls.startswith('print '):
                val = self._expr(ls[6:].strip())
                if self._es_shen(val):
                    res.append(f'{indent}printf("%s\\\\n", {val});')
                else:
                    res.append(f'{indent}printf("%g\\\\n", (double)({val}));')
                continue
            if ls.startswith('read '):
                var = ls[5:].strip()
                typ = self.tabla.get(var, 'ontie')
                fmt = {'ontie':'%d','flote':'%f','duble':'%lf','shen':'%s'}.get(typ,'%d')
                res.append(f'{indent}scanf("{fmt}", &{var});')
                continue
            if ls.startswith('return'):
                resto = ls[6:].strip()
                if resto:
                    res.append(f'{indent}return {self._expr(resto)};')
                else:
                    res.append(f'{indent}return;')
                continue
            if ls.startswith('if '):
                parts = ls.split()
                gi = parts.index('goto')
                cond = ' '.join(parts[1:gi])
                label = parts[-1]
                res.append(f'{indent}if ({self._expr(cond)}) goto {label};')
                continue
            if ls.startswith('goto '):
                res.append(f'{indent}goto {ls.split()[1]};')
                continue
            if '=' in ls:
                dst, resto = ls.split('=', 1)
                res.append(f'{indent}{dst.strip()} = {self._expr(resto.strip())};')
                continue
            res.append(f'{indent}// {ls}')
        return res

    def generar_cpp(self):
        funcs, main_lines = self._separar()
        cpp = ['#include <stdio.h>', '#include <stdlib.h>', '']
        # forward declarations
        for name, info in self.tabla_funciones.items():
            ret = self._tc(info.get('retorno', 'vid'))
            params = info.get('params', [])
            param_str = ', '.join(f"{self._tc(t)} {n}" for t, n in params)
            cpp.append(f'{ret} {name}({param_str});')
        if self.tabla_funciones:
            cpp.append('')
        # funciones
        for name, lines in funcs.items():
            info = self.tabla_funciones.get(name, {})
            ret = self._tc(info.get('retorno', 'vid'))
            params = info.get('params', [])
            param_str = ', '.join(f"{self._tc(t)} {n}" for t, n in params)
            param_set = {n for _, n in params}
            cpp.append(f'{ret} {name}({param_str}) {{')
            for d in self._decl_locales(name, excl=param_set):
                cpp.append(d)
            for d in self._decl_temps(lines):
                cpp.append(d)
            if self._decl_locales(name, excl=param_set) or self._decl_temps(lines):
                cpp.append('')
            cpp += self._traducir_bloque(lines)
            cpp.append('}')
            cpp.append('')
        # main
        cpp.append('int main() {')
        for d in self._decl_locales('__main__'):
            cpp.append(d)
        for d in self._decl_temps(main_lines):
            cpp.append(d)
        if self._decl_locales('__main__') or self._decl_temps(main_lines):
            cpp.append('')
        cpp += self._traducir_bloque(main_lines)
        cpp.append('    return 0;')
        cpp.append('}')
        return '\n'.join(cpp)