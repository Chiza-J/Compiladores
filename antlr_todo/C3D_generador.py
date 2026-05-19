from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo             = []
        self.temp_count         = 0
        self.label_count        = 0
        self.tabla              = tabla_simbolos  # { nombre: tipo }
        self._break_label_stack = []
        self._cont_label_stack  = []

    #  helpers ─

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, line):
        self.codigo.append(line)

    #  programa y bloques 

    def visitPrograma(self, ctx):
        # primero definiciones de funciones, luego bloque principal
        for f in ctx.funcion_def():
            self.visit(f)
        self.visit(ctx.bloque())
        return None

    def visitBloque(self, ctx):
        return self.visitChildren(ctx)

    def visitInstrucciones(self, ctx):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx):
        return self.visitChildren(ctx)

    #  declaracion ─

    def visitDeclaracion(self, ctx):
        var = ctx.ID().getText()
        if var not in self.tabla:
            return

        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        elif ctx.expr_decimal():
            value = self.visit(ctx.expr_decimal())
        elif ctx.expr_string():
            value = self.visit(ctx.expr_string())
        else:
            value = '0'

        self.emit(f"{var} = {value}")

    #  asignacion 

    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()
        if var not in self.tabla:
            return
        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    #  impresion ─

    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")

    #  entrada (lirf) 

    def visitEntrada(self, ctx):
        var = ctx.ID().getText()
        self.emit(f"read {var}")

    #  if / else ─

    def visitCondicion_if(self, ctx):
        cond        = self.visit(ctx.expr())
        label_true  = self.new_label()
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

    #  while ─

    def visitCiclo_while(self, ctx):
        label_start = self.new_label()
        label_body  = self.new_label()
        label_end   = self.new_label()

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

    #  do-while (fer_pendan) ─

    def visitCiclo_fer_pendan(self, ctx):
        label_start = self.new_label()
        label_cond  = self.new_label()
        label_end   = self.new_label()

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

    #  for (pur) ─

    def visitCiclo_pur(self, ctx):
        self.visit(ctx.pur_init())

        label_start = self.new_label()
        label_body  = self.new_label()
        label_step  = self.new_label()
        label_end   = self.new_label()

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

    def visitPur_init(self, ctx):
        var = ctx.ID().getText()
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
        # agregar a tabla si es declaracion nueva
        if var not in self.tabla:
            if ctx.ONTIE():        self.tabla[var] = 'ontie'
            elif ctx.FLOTE():      self.tabla[var] = 'flote'
            elif ctx.DUBLE():      self.tabla[var] = 'duble'
            elif ctx.SHEN():       self.tabla[var] = 'shen'
        self.emit(f"{var} = {value}")

    def visitPur_step(self, ctx):
        var   = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    #  switch (shangshe) ─

    def visitCondicion_switch(self, ctx):
        expr_val      = self.visit(ctx.expr())
        label_end     = self.new_label()
        casos         = ctx.caso_switch()
        labels        = [self.new_label() for _ in casos]
        label_default = self.new_label() if ctx.caso_default() else label_end

        self._break_label_stack.append(label_end)

        # comparaciones
        for i, caso in enumerate(casos):
            val  = caso.INT().getText()
            temp = self.new_temp()
            self.emit(f"{temp} = {expr_val} compag {val}")
            self.emit(f"if {temp} goto {labels[i]}")
        self.emit(f"goto {label_default}")

        # cuerpos
        for i, caso in enumerate(casos):
            self.emit(f"{labels[i]}:")
            self.visit(caso.instrucciones())

        # default
        if ctx.caso_default():
            self.emit(f"{label_default}:")
            self.visit(ctx.caso_default().instrucciones())

        self.emit(f"{label_end}:")
        self._break_label_stack.pop()

    def visitCaso_switch(self, ctx):
        return self.visitChildren(ctx)

    def visitCaso_default(self, ctx):
        return self.visitChildren(ctx)

    #  break / continue / goto ─

    def visitSentencia_pos(self, ctx):
        if self._break_label_stack:
            self.emit(f"goto {self._break_label_stack[-1]}")

    def visitSentencia_contine(self, ctx):
        if self._cont_label_stack:
            self.emit(f"goto {self._cont_label_stack[-1]}")

    def visitSentencia_su(self, ctx):
        self.emit(f"goto {ctx.ID().getText()}")

    #  return 

    def visitRetorno(self, ctx):
        if ctx.expr():
            value = self.visit(ctx.expr())
            self.emit(f"return {value}")
        else:
            self.emit("return")

    #  funciones ─
    # Formato C3D:
    #   func_begin nombre
    #   param_decl a
    #   param_decl b
    #   ... cuerpo ...
    #   func_end nombre

    def visitFuncion_def(self, ctx):
        nombre = ctx.ID().getText()

        # guardar tabla y agregar params al scope local
        tabla_anterior = dict(self.tabla)
        for p in ctx.parametros().parametro():
            pid = p.ID().getText()
            if p.ONTIE():        self.tabla[pid] = 'ontie'
            elif p.FLOTE():      self.tabla[pid] = 'flote'
            elif p.DUBLE():      self.tabla[pid] = 'duble'
            elif p.SHEN():       self.tabla[pid] = 'shen'

        self.emit(f"func_begin {nombre}")
        for p in ctx.parametros().parametro():
            self.emit(f"param_decl {p.ID().getText()}")

        self.visit(ctx.bloque())
        self.emit(f"func_end {nombre}")

        self.tabla = tabla_anterior

    def visitParametros(self, ctx):
        return None

    def visitParametro(self, ctx):
        return None

    def visitTipo_retorno(self, ctx):
        return None

    #  llamada a funcion ─
    # Formato C3D:
    #   arg val1
    #   arg val2
    #   tN = call nombre

    def visitLlamada_funcion(self, ctx):
        nombre = ctx.ID().getText()

        # evaluar argumentos y emitir arg
        if ctx.argumentos():
            for expr_ctx in ctx.argumentos().expr():
                val = self.visit(expr_ctx)
                self.emit(f"arg {val}")

        temp = self.new_temp()
        self.emit(f"{temp} = call {nombre}")
        return temp

    def visitLlamada_funcion_stmt(self, ctx):
        nombre = ctx.llamada_funcion().ID().getText()

        if ctx.llamada_funcion().argumentos():
            for expr_ctx in ctx.llamada_funcion().argumentos().expr():
                val = self.visit(expr_ctx)
                self.emit(f"arg {val}")

        self.emit(f"call {nombre}")

    def visitArgumentos(self, ctx):
        return self.visitChildren(ctx)

    #  expresiones ─

    def visitExpr(self, ctx):
        if ctx.llamada_funcion():
            return self.visit(ctx.llamada_funcion())

        if ctx.getChildCount() == 1:
            return ctx.getText()

        left  = self.visit(ctx.expr(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_entera(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left  = self.visit(ctx.expr_entera(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_entera(1))

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_decimal(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left  = self.visit(ctx.expr_decimal(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_decimal(1))

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_string(self, ctx):
        return ctx.getText()

    def visitErrorInstr(self, ctx):
        pass

    def visitTipo(self, ctx):
        return None

    def get_codigo(self):
        return "\n".join(self.codigo)


# ═══════════════════════════════════════════════════════════════
#  TRADUCTOR C3D → C++
# ═══════════════════════════════════════════════════════════════

class C3DAC_Traductor:

    OP_MAP = {
        'plu':    '+',
        'moan':   '-',
        'par':    '*',
        'bag':    '/',
        'minog':  '<',
        'aye':    '>',
        'compag': '==',
    }

    TIPO_CPP = {
        'ontie': 'int',
        'flote': 'float',
        'duble': 'double',
        'shen':  'const char*',
        'vid':   'void',
    }

    def __init__(self, codigo_c3d, tabla_simbolos, tabla_funciones=None):
        self.lineas          = codigo_c3d
        self.tabla           = tabla_simbolos
        self.tabla_funciones = tabla_funciones or {}

    def _tc(self, tipo):
        return self.TIPO_CPP.get(tipo, 'double')

    def _es_temp(self, s):
        return s.startswith('t') and s[1:].isdigit()

    def _expr(self, e):
        for op_l, op_c in self.OP_MAP.items():
            e = e.replace(op_l, op_c)
        return e

    def _es_shen(self, val):
        return val.startswith('"') or self.tabla.get(val, '') == 'shen'

    #  separar funciones del codigo principal 

    def _separar(self):
        funciones = {}   # nombre -> lista de lineas C3D
        main      = []
        actual    = None

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

    #  declaraciones de variables de usuario ─

    def _decl_usuario(self, tabla):
        lines = []
        for nombre, tipo in tabla.items():
            if tipo == 'shen':
                lines.append(f'    const char* {nombre} = "";')
            else:
                lines.append(f'    {self._tc(tipo)} {nombre} = 0;')
        return lines

    #  declaraciones de temporales inferidos ─

    def _decl_temps(self, lineas):
        temps = set()
        for l in lineas:
            ls = l.strip()
            if '=' in ls and not ls.endswith(':') \
               and not ls.startswith('func_') \
               and not ls.startswith('param_decl') \
               and not ls.startswith('arg ') \
               and not ls.startswith('call '):
                dest = ls.split('=')[0].strip()
                if self._es_temp(dest):
                    temps.add(dest)
        return [f'    double {t};'
                for t in sorted(temps, key=lambda x: int(x[1:]))]

    #  traducir bloque de lineas C3D con manejo de args ─

    def _traducir_bloque(self, lineas, indent='    '):
        resultado = []
        # buffer de args pendientes para la proxima call
        args_buf  = []

        for linea in lineas:
            l = linea.strip()
            if not l:
                continue

            # etiqueta
            if l.endswith(':') and ' ' not in l:
                resultado.append(f'{indent}{l}')
                continue

            # arg — acumular sin emitir nada
            if l.startswith('arg '):
                args_buf.append(self._expr(l[4:].strip()))
                continue

            # param_decl — ya esta en la firma, ignorar
            if l.startswith('param_decl '):
                continue

            # tN = call nombre
            if '= call ' in l:
                dest   = l.split('=')[0].strip()
                nombre = l.split('call ')[1].strip()
                args   = ', '.join(args_buf)
                args_buf = []
                resultado.append(f'{indent}{dest} = {nombre}({args});')
                continue

            # call nombre  (sin retorno)
            if l.startswith('call '):
                nombre = l[5:].strip()
                args   = ', '.join(args_buf)
                args_buf = []
                resultado.append(f'{indent}{nombre}({args});')
                continue

            # print
            if l.startswith('print '):
                val = self._expr(l[6:].strip())

                if self._es_shen(val):
                    resultado.append(
                        indent + 'printf("%s\\\\n", ' + val + ');'
                    )
                else:
                    resultado.append(
                        f'{indent}printf("%g\\\\n", (double)({val}));'
                    )

                continue

            # read
            if l.startswith('read '):
                var  = l[5:].strip()
                tipo = self.tabla.get(var, 'ontie')
                fmt  = {'ontie':'%d','flote':'%f',
                        'duble':'%lf','shen':'%s'}.get(tipo,'%d')
                resultado.append(f'{indent}scanf("{fmt}", &{var});')
                continue

            # return
            if l.startswith('return'):
                resto = l[6:].strip()
                if resto:
                    resultado.append(f'{indent}return {self._expr(resto)};')
                else:
                    resultado.append(f'{indent}return;')
                continue

            # if cond goto L
            if l.startswith('if '):
                idx   = l.rfind(' goto ')
                cond  = self._expr(l[3:idx].strip())
                label = l.split()[-1]
                resultado.append(f'{indent}if ({cond}) goto {label};')
                continue

            # goto
            if l.startswith('goto '):
                resultado.append(f'{indent}goto {l.split()[1]};')
                continue

            # asignacion
            if '=' in l:
                dest, resto = l.split('=', 1)
                resultado.append(
                    f'{indent}{dest.strip()} = {self._expr(resto.strip())};')
                continue

            resultado.append(f'{indent}// {l}')

        return resultado

    #  generar C++ completo 

    def generar_cpp(self):
        funciones, main_lineas = self._separar()

        cpp = ['#include <stdio.h>', '#include <stdlib.h>', '']

        # declaraciones forward de funciones
        for nombre, info in self.tabla_funciones.items():
            tipo_r    = self._tc(info.get('retorno', 'vid'))
            params    = info.get('params', [])
            param_str = ', '.join(f"{self._tc(t)} {n}" for t, n in params)
            cpp.append(f'{tipo_r} {nombre}({param_str});')

        if self.tabla_funciones:
            cpp.append('')

        # definiciones de funciones
        for nombre, lineas_func in funciones.items():
            info      = self.tabla_funciones.get(nombre, {})
            tipo_r    = self._tc(info.get('retorno', 'vid'))
            params    = info.get('params', [])
            param_str = ', '.join(f"{self._tc(t)} {n}" for t, n in params)

            cpp.append(f'{tipo_r} {nombre}({param_str}) {{')

            # temporales locales de la funcion
            for d in self._decl_temps(lineas_func):
                cpp.append(d)
            if self._decl_temps(lineas_func):
                cpp.append('')

            cpp += self._traducir_bloque(lineas_func)
            cpp.append('}')
            cpp.append('')

        # main
        cpp.append('int main() {')
        cpp += self._decl_usuario(self.tabla)
        cpp += self._decl_temps(main_lineas)

        if self._decl_usuario(self.tabla) or self._decl_temps(main_lineas):
            cpp.append('')

        cpp += self._traducir_bloque(main_lineas)
# solo agregar return 0 si el ultimo codigo del main no tiene return
        ultimas = [l.strip() for l in self._traducir_bloque(main_lineas) if l.strip()]
        tiene_return = ultimas and ultimas[-1].startswith('return')
        if not tiene_return:
            cpp.append('')
            cpp.append('    return 0;')
        cpp.append('}')

        return '\n'.join(cpp)

    def guardar(self, ruta='salida.cpp'):
        contenido = self.generar_cpp()
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return contenido