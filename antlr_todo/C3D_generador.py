from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0
        self.tabla = tabla_simbolos
        self.temp_tipos = {}   #  TIPOS DE TEMPORALES

    # Helpers
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, line):
        self.codigo.append(line)

    # Estructura base
    def visitPrograma(self, ctx):
        return self.visitChildren(ctx)

    def visitBloque(self, ctx):
        return self.visitChildren(ctx)

    def visitInstrucciones(self, ctx):
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx):
        return self.visitChildren(ctx)

    # DECLARACIÓN
    def visitDeclaracion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        if ctx.expr():
            value, _ = self.visit(ctx.expr())
            self.emit(f"{var} = {value}")

    # ASIGNACIÓN
    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        value, _ = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    # PRINT
    def visitImpresion(self, ctx):
        val, _ = self.visit(ctx.expr())
        self.emit(f"print {val}")

    # EXPRESIONES CON TIPADO
    def visitExpr(self, ctx):

        # 🔹 Caso simple
        if ctx.getChildCount() == 1:
            val = ctx.getText()

            if val.replace('.', '', 1).isdigit():
                if '.' in val:
                    return val, 'duble'
                return val, 'ontie'

            if val.startswith('"'):
                return val, 'shen'

            if val in self.tabla:
                return val, self.tabla[val]

            return val, 'error'

        # 🔹 Caso binario
        left, tipo1 = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()
        right, tipo2 = self.visit(ctx.expr(1))

        temp = self.new_temp()

        #  REGLAS DE TIPADO
        if tipo1 == 'shen' or tipo2 == 'shen':
            tipo_res = 'shen'
        elif tipo1 == 'duble' or tipo2 == 'duble':
            tipo_res = 'duble'
        elif tipo1 == 'flote' or tipo2 == 'flote':
            tipo_res = 'flote'
        else:
            tipo_res = 'ontie'

        self.temp_tipos[temp] = tipo_res

        self.emit(f"{temp} = {left} {op} {right}")
        return temp, tipo_res

    # CONTROL IF
    def visitCondicion_if(self, ctx):
        cond, _ = self.visit(ctx.expr())

        Ltrue = self.new_label()
        Lfalse = self.new_label()

        self.emit(f"if {cond} goto {Ltrue}")
        self.emit(f"goto {Lfalse}")
        self.emit(f"{Ltrue}:")

        self.visit(ctx.bloque(0))

        if ctx.OTRE():
            Lend = self.new_label()
            self.emit(f"goto {Lend}")
            self.emit(f"{Lfalse}:")
            self.visit(ctx.bloque(1))
            self.emit(f"{Lend}:")
        else:
            self.emit(f"{Lfalse}:")

    # WHILE
    def visitCiclo_while(self, ctx):
        Lstart = self.new_label()
        Lbody = self.new_label()
        Lend = self.new_label()

        self.emit(f"{Lstart}:")
        cond, _ = self.visit(ctx.expr())

        self.emit(f"if {cond} goto {Lbody}")
        self.emit(f"goto {Lend}")

        self.emit(f"{Lbody}:")
        self.visit(ctx.bloque())
        self.emit(f"goto {Lstart}")

        self.emit(f"{Lend}:")

    # RETURN
    def visitRetorno(self, ctx):
        if ctx.expr():
            val, _ = self.visit(ctx.expr())
            self.emit(f"return {val}")
        else:
            self.emit("return")

    def get_codigo(self):
        return "\n".join(self.codigo)


# ============================================
# TRADUCTOR A C++
# ============================================

class C3DAC_Traductor:

    OP_MAP = {
        'plu': '+',
        'moan': '-',
        'par': '*',
        'bag': '/',
        'minog': '<',
        'aye': '>',
        'compag': '=='
    }

    def __init__(self, codigo_c3d, tabla_simbolos, temp_tipos):
        self.lineas = codigo_c3d
        self.tabla = tabla_simbolos
        self.temp_tipos = temp_tipos

    def _tipo_cpp(self, tipo):
        return {
            'ontie': 'int',
            'flote': 'float',
            'duble': 'double',
            'shen': 'string'
        }.get(tipo, 'double')

    def _traducir_expr(self, expr):
        for k, v in self.OP_MAP.items():
            expr = expr.replace(k, v)
        return expr

    # VARIABLES
    def _declaraciones_usuario(self):
        lines = []
        for nombre, tipo in self.tabla.items():
            if tipo == 'shen':
                lines.append(f'    string {nombre} = "";')
            else:
                lines.append(f'    {self._tipo_cpp(tipo)} {nombre} = 0;')
        return lines

    # TEMPORALES TIPADOS
    def _declaraciones_temps(self):
        lines = []
        for t, tipo in self.temp_tipos.items():
            if tipo == 'shen':
                lines.append(f'    string {t};')
            else:
                lines.append(f'    {self._tipo_cpp(tipo)} {t} = 0;')
        return lines

    # TRADUCCIÓN DE LÍNEAS
    def _traducir_linea(self, linea):
        linea = linea.strip()

        if linea.endswith(':'):
            return f"    {linea}"

        if linea.startswith('print '):
            val = self._traducir_expr(linea[6:])
            return f'    cout << {val} << endl;'

        if linea.startswith('return'):
            val = linea[6:].strip()
            return f"    return {val};" if val else "    return 0;"

        if linea.startswith('if '):
            idx = linea.rfind(' goto ')
            cond = self._traducir_expr(linea[3:idx])
            label = linea.split()[-1]
            return f"    if ({cond}) goto {label};"

        if linea.startswith('goto '):
            return f"    {linea};"

        if '=' in linea:
            dest, expr = linea.split('=')
            return f"    {dest.strip()} = {self._traducir_expr(expr.strip())};"

        return f"    // {linea}"

    # GENERAR C++
    def generar_cpp(self):
        cpp = []
        cpp.append('#include <iostream>')
        cpp.append('#include <string>')
        cpp.append('using namespace std;')
        cpp.append('')
        cpp.append('int main() {')

        cpp += self._declaraciones_usuario()
        cpp += self._declaraciones_temps()
        cpp.append('')

        for linea in self.lineas:
            cpp.append(self._traducir_linea(linea))

        cpp.append('')
        cpp.append('    return 0;')
        cpp.append('}')

        return "\n".join(cpp)