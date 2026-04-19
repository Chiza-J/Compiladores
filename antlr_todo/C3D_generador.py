from antlr_todo.LenguajeVisitor import LenguajeVisitor

class C3DGenerador(LenguajeVisitor):

    # Base del generador  
    def __init__(self, tabla_simbolos):
        self.codigo = []
        self.temp_count = 0
        self.tabla = tabla_simbolos

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def emit(self, line):
        self.codigo.append(line)

    #Deviinimos las expresiones a partir del visitor
    def visitExpr(self, ctx):
        if ctx.getChildCount() == 1:
            return ctx.getText()
        
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.OP().getText()

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")

        return temp
    
    #identificamos las declaraciones de variables
    def visitDeclaracion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        # detectar tipo de expresión
        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        else:
            value = self.visit(ctx.expr_decimal())
        
        self.emit(f"{var} = {value}")


# definicion de asignaciones
    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()

        if var not in self.tabla:
            return

        value = self.visit(ctx.expr())
        self.emit(f"{var} = {value}")

#print del C3D
    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")

    # funcion de if
    def visitCondicion_if(self, ctx):
        cond = self.visit(ctx.expr())

        label_true = self.new_temp()
        label_false = self.new_temp()

        self.emit(f"if {cond} goto {label_true}")
        self.emit(f"goto {label_false}")

        self.emit(f"{label_true}:")

        self.visit(ctx.bloque(0))

        if ctx.OTRE():
            label_end = self.new_temp()

            self.emit(f"goto {label_end}")

            self.emit(f"{label_false}:")
            self.visit(ctx.bloque(1))

            self.emit(f"{label_end}:")
        else:
            self.emit(f"{label_false}:")

    # Ciclo while
    def visitCiclo_while(self, ctx):
        label_start = self.new_temp()
        label_true = self.new_temp()
        label_end = self.new_temp()

        self.emit(f"{label_start}:")

        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {label_true}")
        self.emit(f"goto {label_end}")

        self.emit(f"{label_true}:")
        self.visit(ctx.bloque())

        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    #Return
    def visitRetorno(self, ctx):
        if ctx.expr():
            value = self.visit(ctx.expr())
            self.emit(f"return {value}")
        else:
            self.emit("return")