from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0
        self.tabla = tabla_simbolos
        self.tipos_temp = {}   #  TIPADO AUTOMÁTICO

    # HELPERS

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, line):
        self.codigo.append(line)

    #  OBTENER TIPO DE UN VALOR
    def obtener_tipo(self, val):

        if val in self.tabla:
            return self.tabla[val]

        if val in self.tipos_temp:
            return self.tipos_temp[val]

        if val.startswith('"'):
            return 'shen'

        if '.' in val:
            return 'duble'

        if val.isdigit():
            return 'ontie'

        return 'ontie'

    #  PROMOCIÓN DE TIPOS
    def promocion(self, t1, t2):
        if 'shen' in (t1, t2):
            return 'shen'
        if 'duble' in (t1, t2):
            return 'duble'
        if 'flote' in (t1, t2):
            return 'flote'
        return 'ontie'

    # ESTRUCTURA

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

        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        elif ctx.expr_decimal():
            value = self.visit(ctx.expr_decimal())
        elif ctx.expr_string():
            value = self.visit(ctx.expr_string())
        else:
            value = ctx.getText()

        self.emit(f"{var} = {value}")

    # ASIGNACIÓN

    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

    # PRINT

    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")

    # EXPRESIONES ( AQUÍ PASA LA MAGIA)

    def visitExpr(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))

        temp = self.new_temp()

        tipo_izq = self.obtener_tipo(left)
        tipo_der = self.obtener_tipo(right)

        #  REGLAS
        if tipo_izq == 'shen' or tipo_der == 'shen':
            tipo_result = 'shen'
        else:
            tipo_result = self.promocion(tipo_izq, tipo_der)

        #  GUARDAR TIPO
        self.tipos_temp[temp] = tipo_result

        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_entera(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left = self.visit(ctx.expr_entera(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_entera(1))

        temp = self.new_temp()

        self.tipos_temp[temp] = 'ontie'   #  FORZADO

        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_decimal(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left = self.visit(ctx.expr_decimal(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_decimal(1))

        temp = self.new_temp()

        self.tipos_temp[temp] = 'duble'   #  FORZADO

        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visitExpr_string(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()

        left = self.visit(ctx.expr_string(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.expr_string(1))

        temp = self.new_temp()

        self.tipos_temp[temp] = 'shen'   #  STRING

        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    # CONTROL

    def visitCondicion_if(self, ctx):
        cond = self.visit(ctx.expr())

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

    def visitCiclo_while(self, ctx):
        Lstart = self.new_label()
        Lbody = self.new_label()
        Lend = self.new_label()

        self.emit(f"{Lstart}:")
        cond = self.visit(ctx.expr())

        self.emit(f"if {cond} goto {Lbody}")
        self.emit(f"goto {Lend}")

        self.emit(f"{Lbody}:")
        self.visit(ctx.bloque())
        self.emit(f"goto {Lstart}")

        self.emit(f"{Lend}:")

    def visitRetorno(self, ctx):
        if ctx.expr():
            val = self.visit(ctx.expr())
            self.emit(f"return {val}")
        else:
            self.emit("return")

    def get_codigo(self):
        return "\n".join(self.codigo)


# ============================================
# TRADUCTOR CON TIPOS REALES
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

    def __init__(self, codigo_c3d, tabla_simbolos, tipos_temp):
        self.lineas = codigo_c3d
        self.tabla = tabla_simbolos
        self.tipos_temp = tipos_temp   #  IMPORTANTE

    def _tipo_cpp(self, tipo):
        return {
            'ontie': 'int',
            'flote': 'float',
            'duble': 'double',
            'shen': 'string'
        }.get(tipo, 'double')

    def _es_temp(self, nombre):
        return nombre.startswith('t')

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

    #  TEMPORALES TIPADOS
    def _declaraciones_temps(self):
        temps = set()

        for linea in self.lineas:
            if '=' in linea:
                dest = linea.split('=')[0].strip()
                if self._es_temp(dest):
                    temps.add(dest)

        decls = []
        for t in sorted(temps, key=lambda x: int(x[1:])):
            tipo = self.tipos_temp.get(t, 'duble')
            cpp_tipo = self._tipo_cpp(tipo)
            decls.append(f"    {cpp_tipo} {t};")

        return decls

    # TRADUCCIÓN
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

    # GENERAR CPP
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