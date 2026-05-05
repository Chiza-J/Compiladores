from antlr4 import *
from antlr_todo.LenguajeVisitor import LenguajeVisitor


class C3DGenerador(LenguajeVisitor):

    def __init__(self, tabla_simbolos):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0
        self.tabla = tabla_simbolos

        # tipos de temporales
        self.temp_tipos = {}

    # HELPERS
    def new_temp(self, tipo):
        self.temp_count += 1
        t = f"t{self.temp_count}"
        self.temp_tipos[t] = tipo
        return t

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, line):
        self.codigo.append(line)

    # PROGRAMA
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
            val, tipo = self.visit(ctx.expr_entera())

        elif ctx.expr_decimal():
            val, tipo = self.visit(ctx.expr_decimal())

        elif ctx.expr_string():
            val, tipo = self.visit(ctx.expr_string())

        else:
            return

        self.emit(f"{var} = {val}")

    # ASIGNACIÓN
    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        val, tipo = self.visit(ctx.expr())
        self.emit(f"{var} = {val}")

    # PRINT
    def visitImpresion(self, ctx):
        val, _ = self.visit(ctx.expr())
        self.emit(f"print {val}")

    # EXPRESIONES GENERALES
    def visitExpr(self, ctx):
        if ctx.getChildCount() == 1:
            text = ctx.getText()

            # literal
            if text.startswith('"'):
                return text, 'shen'
            if '.' in text:
                return text, 'duble'
            if text.isdigit():
                return text, 'ontie'

            # variable
            if text in self.tabla:
                return text, self.tabla[text]

            return text, 'ontie'

        left, tipo_izq = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()
        right, tipo_der = self.visit(ctx.expr(1))

        # STRING
        if tipo_izq == 'shen' or tipo_der == 'shen':
            if op == 'plu':
                t = self.new_temp('shen')
                self.emit(f"{t} = {left} plu {right}")
                return t, 'shen'

        # NUMÉRICO (promoción de tipos)
        tipo_result = self.promocion(tipo_izq, tipo_der)

        # OPTIMIZACIÓN: evitar temporal si es simple
        if self.es_simple(left) and self.es_simple(right):
            return f"{left} {op} {right}", tipo_result

        t = self.new_temp(tipo_result)
        self.emit(f"{t} = {left} {op} {right}")
        return t, tipo_result

    # ENTEROS
    def visitExpr_entera(self, ctx):
        if ctx.getChildCount() == 1:
            text = ctx.getText()
            return text, 'ontie'

        left, _ = self.visit(ctx.expr_entera(0))
        op = ctx.getChild(1).getText()
        right, _ = self.visit(ctx.expr_entera(1))

        if self.es_simple(left) and self.es_simple(right):
            return f"{left} {op} {right}", 'ontie'

        t = self.new_temp('ontie')
        self.emit(f"{t} = {left} {op} {right}")
        return t, 'ontie'

    # DECIMALES
    def visitExpr_decimal(self, ctx):
        if ctx.getChildCount() == 1:
            text = ctx.getText()
            return text, 'duble'

        left, tipo_izq = self.visit(ctx.expr_decimal(0))
        op = ctx.getChild(1).getText()
        right, tipo_der = self.visit(ctx.expr_decimal(1))

        tipo = self.promocion(tipo_izq, tipo_der)

        if self.es_simple(left) and self.es_simple(right):
            return f"{left} {op} {right}", tipo

        t = self.new_temp(tipo)
        self.emit(f"{t} = {left} {op} {right}")
        return t, tipo

    # STRINGS
    def visitExpr_string(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText(), 'shen'

        left, _ = self.visit(ctx.expr_string(0))
        op = ctx.getChild(1).getText()
        right, _ = self.visit(ctx.expr_string(1))

        t = self.new_temp('shen')
        self.emit(f"{t} = {left} plu {right}")
        return t, 'shen'

    # CONTROL
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

    def visitRetorno(self, ctx):
        if ctx.expr():
            val, _ = self.visit(ctx.expr())
            self.emit(f"return {val}")
        else:
            self.emit("return")

    # UTILIDADES
    def promocion(self, t1, t2):
        if 'shen' in (t1, t2):
            return 'shen'
        if 'duble' in (t1, t2):
            return 'duble'
        if 'flote' in (t1, t2):
            return 'flote'
        return 'ontie'

    def es_simple(self, val):
        return val.isdigit() or val.startswith('"') or val in self.tabla

    def get_codigo(self):
        return "\n".join(self.codigo)