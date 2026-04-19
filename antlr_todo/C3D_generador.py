from LenguajeVisitor import LenguajeVisitor

class C3DGenerador(LenguajeVisitor):

#Base del generador  
    def __init__(self):
        self.codigo = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def emit(self, line):
        self.codigo.append(line)

    #Deviinimos las expresiones a partir del visitor
    def visitExpr(self, ctx):
        #si se encuentra el nodo hijo del arbol retorna el texto que contenga
        if ctx.getChildCount() == 1:
            return ctx.getText()
        
        #Recorre el arbol
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.OP().getText()

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")

        return temp
    
    #identificamos las declaraciones de variables
    def visitDeclaracion(self, ctx):
        var = ctx.ID().getText()

        if ctx.expr_expr_entera():
            value = self.visit(ctx.expr_entera())
        else:
            value = self.visit(ctx.expr_decimal())
        
        self.emit(f"{var} = {value}")

    