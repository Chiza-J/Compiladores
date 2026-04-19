from LenguajeVisitor import LenguajeVisitor

class C3DGenerador(LenguajeVisitor):

#Base del generador  
    def __init__(self):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"
    
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

        if ctx.expr_entera():
            value = self.visit(ctx.expr_entera())
        else:
            value = self.visit(ctx.expr_decimal())
        
        self.emit(f"{var} = {value}")


# definicion de asignaciones
    def visitAsignacion(self, ctx):
        var = ctx.ID().getText()
        value = self.visit(ctx.expr())

        self.emit(f"{var} = {value}")

#print del C3D
    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())
        self.emit(f"print {value}")

    # funcion de if
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

    # Ciclo while
    def visitCiclo_while(self, ctx):
        Lstart = self.new_label()
        Ltrue = self.new_label()
        Lend = self.new_label()

        self.emit(f"{Lstart}:")

        cond = self.visit(ctx.expr())
        self.emit(f"if {cond} goto {Ltrue}")
        self.emit(f"goto {Lend}")

        self.emit(f"{Ltrue}:")
        self.visit(ctx.bloque())

        self.emit(f"goto {Lstart}")
        self.emit(f"{Lend}:")

    #Return
    def visitRetorno(self, ctx):
        if ctx.expr():
            value = self.visit(ctx.expr())
            self.emit(f"return {value}")
        else:
            self.emit("return")