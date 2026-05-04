from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo   = []          # líneas de código 3 direcciones
        self.temp_count = 0
        self.label_count = 0
        self.tabla    = tabla_simbolos  # { nombre: 'ontie'|'flote'|'duble'|'shen' }

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
    #                shen  x iyal expr_string  puavir   ← NUEVO

    def visitDeclaracion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return  # el semántico ya reportó el error

        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        elif ctx.expr_decimal():
            value = self.visit(ctx.expr_decimal())
        elif ctx.expr_string():                        # ← NUEVO
            value = self.visit(ctx.expr_string())
        else:
            value = ctx.getText()

        self.emit(f"{var} = {value}")

    #  Asignación:  x iyal expr puavir

    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        # Si la variable es shen, visitar expr_string si existe
        value = self.visit(ctx.expr())

    #  Impresión:  amprimi(expr) puavir
    #  Funciona igual para números y strings — el traductor distingue

    def visitImpresion(self, ctx):
        # Soporta expr numérica o expr_string con la misma instrucción print
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")
        self.emit(f"print {value}")

    #  Expresión general:
    #    expr OP expr   |   INT   |   FLOAT_LIT   |   ID

    def visitExpr(self, ctx):
        # Hoja: un solo hijo
        if ctx.getChildCount() == 1:
            return ctx.getText()

        # Nodo binario: expr OP expr
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

    #  Expresión string (NUEVO):
    #    expr_string plu expr_string   |   STRING_LIT   |   ID

    def visitExpr_string(self, ctx):                   # ← NUEVO MÉTODO
        if ctx.getChildCount() == 1:
            return ctx.getText()                       # STRING_LIT o ID

        # Concatenación:  expr_string plu expr_string
        left  = self.visit(ctx.expr_string(0))
        op    = ctx.getChild(1).getText()              # 'plu'
        right = self.visit(ctx.expr_string(1))

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
        plu   →  +  (números) / strcat (strings)
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
        self.lineas  = codigo_c3d
        self.tabla   = tabla_simbolos   # { nombre: 'ontie'|'flote'|'duble'|'shen' }

    # ── helpers ──────────────────────────────────────────────

    def _tipo_cpp(self, tipo_leng):
        return {
            'ontie': 'int',
            'flote': 'float',
            'duble': 'double',
            'shen':  'const char*',                    # ← NUEVO
        }.get(tipo_leng, 'double')

    def _es_temp(self, nombre):
        return nombre.startswith('t') and nombre[1:].isdigit()

    def _es_string_val(self, val):
        """Devuelve True si el valor es un literal string (entre comillas)."""
        return val.strip().startswith('"')

    def _op(self, op_leng):
        return self.OP_MAP.get(op_leng, op_leng)

    def _traducir_expr(self, expr):
        for op_l, op_c in self.OP_MAP.items():
            expr = expr.replace(op_l, op_c)
        return expr

    # ── declaraciones ────────────────────────────────────────

    def _declaraciones_usuario(self):
        lines = []
        for nombre, tipo in self.tabla.items():
            if tipo == 'shen':
                lines.append(f'    const char* {nombre} = "";')  # ← NUEVO
            else:
                lines.append(f'    {self._tipo_cpp(tipo)} {nombre} = 0;')
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

    # ── traducción línea a línea ──────────────────────────────

    def _traducir_linea(self, linea):
        linea = linea.strip()

        # Etiqueta:   L1:
        if linea.endswith(':') and ' ' not in linea:
            return f"    {linea}"

        # print valor  — mismo keyword para número y string
        if linea.startswith('print '):
            val = self._traducir_expr(linea[6:].strip())
            if self._es_string_val(val):               # ← NUEVO: string
                return f'    printf("%s\\n", {val});'
            # es variable shen (ID) o temporal de string
            if val in self.tabla and self.tabla[val] == 'shen':
                return f'    printf("%s\\n", {val});'  # ← NUEVO
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
            idx_goto = linea.rfind(' goto ')
            cond_raw = linea[3:idx_goto].strip()
            cond  = self._traducir_expr(cond_raw)
            label = linea.split()[-1]
            return f"    if ({cond}) goto {label};"

        # goto LX
        if linea.startswith('goto '):
            return f"    goto {linea.split()[1]};"

        # asignación
        if '=' in linea:
            dest, resto = linea.split('=', 1)
            dest  = dest.strip()
            resto = self._traducir_expr(resto.strip())
            return f"    {dest} = {resto};"

        return f"    // {linea}"

    # ── punto de entrada ─────────────────────────────────────

    def generar_cpp(self):
        cpp = []
        cpp.append('#include <stdio.h>')
        cpp.append('#include <string.h>')                  # ← NUEVO para strings
        cpp.append('')
        cpp.append('int main() {')

        cpp += self._declaraciones_usuario()
        cpp += self._declaraciones_temps()

        if self._declaraciones_usuario() or self._declaraciones_temps():
            cpp.append('')

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