from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo   = []          # líneas de código 3 direcciones
        self.temp_count = 0
        self.label_count = 0
        self.tabla    = tabla_simbolos  # { nombre: 'ontie'|'flote'|'duble' }

    # ─────────────────────────────────────────────
    #  Helpers
    # ─────────────────────────────────────────────

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, line):
        self.codigo.append(line)


    #  Programa y bloque — solo recorren hijos

    def visitPrograma(self, ctx):
        return self.visitChildren(ctx)

    def visitBloque(self, ctx):
        return self.visitChildren(ctx)

    def visitInstrucciones(self, ctx):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx):
        return self.visitChildren(ctx)

    #  Declaración:  ontie x iyal expr_entera puavir
    #                flote x iyal expr_decimal puavir
    #                duble x iyal expr_decimal puavir


    def visitDeclaracion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return  # el semántico ya reportó el error

        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        else:
            value = self.visit(ctx.expr_decimal())

        self.emit(f"{var} = {value}")

    #  Asignación:  x iyal expr puavir

    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    #  Impresión:  amprimi(expr) puavir

    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")

    #  Expresión general:
    #    expr OP expr   |   INT   |   FLOAT_LIT   |   ID

    def visitExpr(self, ctx):
        # Hoja: un solo hijo
        if ctx.getChildCount() == 1:
            return ctx.getText()

        # Nodo binario: expr OP expr
        # getChild(1) es el token OP entre los dos expr
        left  = self.visit(ctx.expr(0))
        op    = ctx.getChild(1).getText()   # plu, moan, par, bag, minog, aye, compag
        right = self.visit(ctx.expr(1))

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    #  Expresión entera:
    #    expr_entera OP expr_entera   |   INT   |   ID

    def visitExpr_entera(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left  = self.visit(ctx.expr_entera(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_entera(1))

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    #  Expresión decimal:
    #    expr_decimal OP expr_decimal   |   FLOAT_LIT   |   INT   |   ID

    def visitExpr_decimal(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left  = self.visit(ctx.expr_decimal(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_decimal(1))

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    #  Condicional:  wi (expr) bloque (otre bloque)?

    def visitCondicion_if(self, ctx):
        cond = self.visit(ctx.expr())

        label_true  = self.new_label()
        label_false = self.new_label()

        self.emit(f"if {cond} goto {label_true}")
        self.emit(f"goto {label_false}")
        self.emit(f"{label_true}:")

        self.visit(ctx.bloque(0))   # bloque del if

        if ctx.OTRE():
            label_end = self.new_label()
            self.emit(f"goto {label_end}")
            self.emit(f"{label_false}:")
            self.visit(ctx.bloque(1))   # bloque del else
            self.emit(f"{label_end}:")
        else:
            self.emit(f"{label_false}:")

    #  Ciclo while:  pendan (expr) bloque

    def visitCiclo_while(self, ctx):
        label_start = self.new_label()
        label_body  = self.new_label()
        label_end   = self.new_label()

        self.emit(f"{label_start}:")

        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {label_body}")
        self.emit(f"goto {label_end}")

        self.emit(f"{label_body}:")
        self.visit(ctx.bloque())

        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    #  Retorno:  retur expr? puavir

    def visitRetorno(self, ctx):
        if ctx.expr():
            value = self.visit(ctx.expr())
            self.emit(f"return {value}")
        else:
            self.emit("return")

    #  Error — no genera código

    def visitErrorInstr(self, ctx):
        pass

    #  Obtener el C3D como string

    def get_codigo(self):
        return "\n".join(self.codigo)


#  TRADUCTOR C3D  →  C++
#  Toma la lista self.codigo del generador y produce un .cpp
#  compilable con:  g++ salida.cpp -o salida

class C3DAC_Traductor:
    """
    Traduce el código de 3 direcciones generado por C3DGenerador
    a un archivo C++ válido y compilable con g++.

    Operadores del lenguaje → C++:
        plu   →  +
        moan  →  -
        par   →  *
        bag   →  /
        minog →  <
        aye   →  >
        compag→  ==
    """

    OP_MAP = {
        'plu':   '+',
        'moan':  '-',
        'par':   '*',
        'bag':   '/',
        'minog': '<',
        'aye':   '>',
        'compag':'==',
    }

    def __init__(self, codigo_c3d: list, tabla_simbolos: dict):
        self.lineas  = codigo_c3d       # lista de strings del C3D
        self.tabla   = tabla_simbolos   # { nombre: 'ontie'|'flote'|'duble' }

    # tipo C++ según tipo del lenguaje 

    def _tipo_cpp(self, tipo_leng):
        return {'ontie': 'int', 'flote': 'float', 'duble': 'double'}.get(tipo_leng, 'double')

    #  detecta si un token es temporal (t1, t2, …) 

    def _es_temp(self, nombre):
        return nombre.startswith('t') and nombre[1:].isdigit()

    #  traduce un operador del lenguaje a C++ 

    def _op(self, op_leng):
        return self.OP_MAP.get(op_leng, op_leng)

    #  traduce una expresión simple (puede contener operadores) 

    def _traducir_expr(self, expr):
        for op_l, op_c in self.OP_MAP.items():
            expr = expr.replace(op_l, op_c)
        return expr

    #  genera el bloque de declaraciones de variables del usuario 

    def _declaraciones_usuario(self):
        lines = []
        for nombre, tipo in self.tabla.items():
            lines.append(f"    {self._tipo_cpp(tipo)} {nombre} = 0;")
        return lines

    #  recorre el C3D e infiere qué temporales se necesitan 

    def _declaraciones_temps(self):
        temps = set()
        for linea in self.lineas:
            linea = linea.strip()
            if '=' in linea and not linea.endswith(':'):
                dest = linea.split('=')[0].strip()
                if self._es_temp(dest):
                    temps.add(dest)
        # ordenar t1, t2, t3 …
        temps = sorted(temps, key=lambda x: int(x[1:]))
        return [f"    double {t};" for t in temps]

    #  traduce una línea de C3D a C++ 

    def _traducir_linea(self, linea):
        linea = linea.strip()

        # Etiqueta:   L1:
        if linea.endswith(':') and ' ' not in linea:
            return f"    {linea}"

        # print valor
        if linea.startswith('print '):
            val = self._traducir_expr(linea[6:].strip())
            return f'    printf("%g\\n", (double)({val}));'

        # return expr  /  return
        if linea.startswith('return'):
            resto = linea[6:].strip()
            if resto:
                val = self._traducir_expr(resto)
                return f"    return (int)({val});"
            return "    return 0;"

        # if cond goto LX
        if linea.startswith('if '):
            # formato: "if <cond> goto <label>"
            partes = linea.split()
            # partes: ['if', ..cond.., 'goto', 'LX']
            label  = partes[-1]
            # la condición está entre 'if' y 'goto'
            idx_goto = linea.rfind(' goto ')
            cond_raw = linea[3:idx_goto].strip()
            cond = self._traducir_expr(cond_raw)
            return f"    if ({cond}) goto {label};"

        # goto LX
        if linea.startswith('goto '):
            label = linea.split()[1]
            return f"    goto {label};"

        # asignación:  dest = left OP right  |  dest = valor
        if '=' in linea:
            dest, resto = linea.split('=', 1)
            dest  = dest.strip()
            resto = self._traducir_expr(resto.strip())
            return f"    {dest} = {resto};"

        return f"    // {linea}"   # línea desconocida → comentario

    #  punto de entrada: genera el string del .cpp completo 

    def generar_cpp(self):
        cpp = []
        cpp.append('#include <stdio.h>')
        cpp.append('')
        cpp.append('int main() {')

        # declaraciones de variables del usuario
        cpp += self._declaraciones_usuario()

        # declaraciones de temporales inferidas
        cpp += self._declaraciones_temps()

        if self._declaraciones_usuario() or self._declaraciones_temps():
            cpp.append('')

        # cuerpo traducido
        for linea in self.lineas:
            cpp.append(self._traducir_linea(linea))

        cpp.append('')
        cpp.append('    return 0;')
        cpp.append('}')

        return '\n'.join(cpp)

    def guardar(self, ruta='salida.cpp'):
        contenido = self.generar_cpp()
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return contenido