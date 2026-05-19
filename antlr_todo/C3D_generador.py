from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo      = []
        self.temp_count  = 0
        self.label_count = 0
        self.tabla       = tabla_simbolos
        # para saber a que label saltar con pos (break)
        self._break_label_stack  = []
        # para saber a que label saltar con contine (continue)
        self._cont_label_stack   = []
        # tabla de funciones definidas { nombre: label_inicio }
        self.funciones   = {}

    #  helpers 

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
        return self.visitChildren(ctx)

    def visitBloque(self, ctx):
        return self.visitChildren(ctx)

    def visitInstrucciones(self, ctx):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx):
        return self.visitChildren(ctx)

    #  declaracion 
    # ontie x iyal expr_entera puavir
    # flote/duble x iyal expr_decimal puavir
    # shen x iyal expr_string puavir

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

    #  impresion 

    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")

    #  entrada (lirf) 
    # lirf(x) puavir  →  read x

    def visitEntrada(self, ctx):
        var = ctx.ID().getText()
        self.emit(f"read {var}")

    #  if / else 

    def visitCondicion_if(self, ctx):
        cond = self.visit(ctx.expr())

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

    #  while 

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

    #  do-while (fer_pendan) 
    # fer_pendan { } pendan(expr) puavir

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

    #  for (pur) 
    # pur(init puavir cond puavir step) { }

    def visitCiclo_pur(self, ctx):
        # init
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
        self.emit(f"{var} = {value}")

    def visitPur_step(self, ctx):
        var   = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    #  switch (shangshe) 
    # shangshe(expr) { ca 1 { } ca 2 { } difu { } }

    def visitCondicion_switch(self, ctx):
        expr_val  = self.visit(ctx.expr())
        label_end = self.new_label()

        self._break_label_stack.append(label_end)

        # generar etiquetas para cada caso
        casos   = ctx.caso_switch()
        labels  = [self.new_label() for _ in casos]
        label_default = self.new_label() if ctx.caso_default() else label_end

        # cadena de comparaciones
        for i, caso in enumerate(casos):
            val_caso = caso.INT().getText()
            temp = self.new_temp()
            self.emit(f"{temp} = {expr_val} compag {val_caso}")
            self.emit(f"if {temp} goto {labels[i]}")

        self.emit(f"goto {label_default}")

        # cuerpo de cada caso
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

    #  break (pos) 

    def visitSentencia_pos(self, ctx):
        if self._break_label_stack:
            self.emit(f"goto {self._break_label_stack[-1]}")

    #  continue (contine) 

    def visitSentencia_contine(self, ctx):
        if self._cont_label_stack:
            self.emit(f"goto {self._cont_label_stack[-1]}")

    #  goto (su) 

    def visitSentencia_su(self, ctx):
        label = ctx.ID().getText()
        self.emit(f"goto {label}")

    #  return 

    def visitRetorno(self, ctx):
        if ctx.expr():
            value = self.visit(ctx.expr())
            self.emit(f"return {value}")
        else:
            self.emit("return")

    #  funciones 
    # funcion ontie suma pasuvert ontie a puavir ontie b pasferme { }

    def visitFuncion_def(self, ctx):
        nombre     = ctx.ID().getText()
        label_func = f"func_{nombre}"
        label_end  = self.new_label()

        self.funciones[nombre] = label_func

        # saltar la definicion en ejecucion lineal
        self.emit(f"goto {label_end}")
        self.emit(f"{label_func}:")

        # registrar parametros en tabla local
        if ctx.parametros():
            self.visit(ctx.parametros())

        self.visit(ctx.bloque())
        self.emit("return")
        self.emit(f"{label_end}:")

    def visitParametros(self, ctx):
        return self.visitChildren(ctx)

    def visitParametro(self, ctx):
        # los parametros se reciben via pop de pila (convension simplificada)
        var = ctx.ID().getText()
        self.emit(f"param_get {var}")

    def visitLlamada_funcion_stmt(self, ctx):
        self.visit(ctx.llamada_funcion())

    def visitLlamada_funcion(self, ctx):
        nombre = ctx.ID().getText()

        # evaluar y pushear argumentos
        if ctx.argumentos():
            args = ctx.argumentos()
            for i in range(args.getChildCount()):
                child = args.getChild(i)
                # saltar comas (PUNTOCOMA en la gramatica)
                if hasattr(child, 'expr'):
                    val = self.visit(child)
                    self.emit(f"param {val}")
                elif hasattr(child, 'INT') or hasattr(child, 'ID') or hasattr(child, 'STRING'):
                    val = self.visit(child)
                    self.emit(f"param {val}")

            # forma mas robusta: recorrer expr directamente
            exprs = args.expr() if hasattr(args, 'expr') else []
            if exprs:
                # limpiar los param emitidos arriba y reemitir correctamente
                # (quitar los emitidos en el loop anterior si los hubo)
                for expr_ctx in exprs:
                    val = self.visit(expr_ctx)
                    self.emit(f"param {val}")

        temp = self.new_temp()
        self.emit(f"{temp} = call {nombre}")
        return temp

    def visitArgumentos(self, ctx):
        return self.visitChildren(ctx)

    #  expresiones 

    def visitExpr(self, ctx):
        # llamada a funcion dentro de expresion
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

    def get_codigo(self):
        return "\n".join(self.codigo)


#  TRADUCTOR C3D → C++ 

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
    }

    def __init__(self, codigo_c3d, tabla_simbolos):
        self.lineas = codigo_c3d
        self.tabla  = tabla_simbolos

    def _traducir_expr(self, expr):
        for op_l, op_c in self.OP_MAP.items():
            expr = expr.replace(op_l, op_c)
        return expr

    def _es_temp(self, nombre):
        return nombre.startswith('t') and nombre[1:].isdigit()

    def _es_string_val(self, val):
        return val.strip().startswith('"')

    def _declaraciones_usuario(self):
        lines = []
        for nombre, tipo in self.tabla.items():
            if tipo == 'shen':
                lines.append(f'    const char* {nombre} = "";')
            else:
                lines.append(f'    {self.TIPO_CPP.get(tipo, "double")} {nombre} = 0;')
        return lines

    def _declaraciones_temps(self):
        temps = set()
        for linea in self.lineas:
            linea = linea.strip()
            if '=' in linea and not linea.endswith(':'):
                dest = linea.split('=')[0].strip()
                if self._es_temp(dest):
                    temps.add(dest)
        temps = sorted(temps, key=lambda x: int(x[1:]))
        return [f"    double {t};" for t in temps]

    def _traducir_linea(self, linea):
        l = linea.strip()
        if not l:
            return ''

        # etiqueta
        if l.endswith(':') and ' ' not in l:
            return f"    {l}"

        # print
        if l.startswith('print '):
            val = self._traducir_expr(l[6:].strip())
            if self._es_string_val(val):
                return f'    printf("%s\\n", {val});'
            if val in self.tabla and self.tabla[val] == 'shen':
                return f'    printf("%s\\n", {val});'
            return f'    printf("%g\\n", (double)({val}));'

        # read (lirf)
        if l.startswith('read '):
            var = l[5:].strip()
            tipo = self.tabla.get(var, 'ontie')
            fmt = {'ontie': '%d', 'flote': '%f', 'duble': '%lf', 'shen': '%s'}.get(tipo, '%d')
            return f'    scanf("{fmt}", &{var});'

        # param (push argumento)
        if l.startswith('param ') and not l.startswith('param_get'):
            val = self._traducir_expr(l[6:].strip())
            return f'    // push {val}'

        # param_get (recibir parametro)
        if l.startswith('param_get '):
            var = l[10:].strip()
            return f'    // param {var}'

        # call
        if '= call ' in l:
            dest, resto = l.split('=', 1)
            nombre = resto.replace('call', '').strip()
            return f'    {dest.strip()} = {nombre}();'

        # return
        if l.startswith('return'):
            resto = l[6:].strip()
            if resto:
                return f'    return (int)({self._traducir_expr(resto)});'
            return '    return 0;'

        # if cond goto label
        if l.startswith('if '):
            idx   = l.rfind(' goto ')
            cond  = self._traducir_expr(l[3:idx].strip())
            label = l.split()[-1]
            return f'    if ({cond}) goto {label};'

        # goto
        if l.startswith('goto '):
            return f'    goto {l.split()[1]};'

        # asignacion
        if '=' in l:
            dest, resto = l.split('=', 1)
            return f'    {dest.strip()} = {self._traducir_expr(resto.strip())};'

        return f'    // {l}'

    def generar_cpp(self):
        cpp = [
            '#include <stdio.h>',
            '#include <string.h>',
            '',
            'int main() {',
        ]
        cpp += self._declaraciones_usuario()
        cpp += self._declaraciones_temps()
        if self._declaraciones_usuario() or self._declaraciones_temps():
            cpp.append('')

        for linea in self.lineas:
            cpp.append(self._traducir_linea(linea))

        cpp += ['', '    return 0;', '}']
        return '\n'.join(cpp)

    def guardar(self, ruta='salida.cpp'):
        contenido = self.generar_cpp()
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return contenido