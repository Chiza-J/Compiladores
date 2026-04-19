from LenguajeVisitor import LenguajeVisitor

class C3DGenerador(LenguajeVisitor):

    def __init__(self):
        self.codigo = []
        self.temp_count = 0

    
