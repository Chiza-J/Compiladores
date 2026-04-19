import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.AnalizadorSemantico import AnalizadorSemantico
from static.reportes_html import TablaSimbolosVisitor
from static.reportes_html import C3DGenerador


def main():

    archivo = os.path.join(ruta_raiz, "programa.leng")

    input_stream = FileStream(archivo, encoding="utf-8")
    lexer = LenguajeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LenguajeParser(stream)

    parser.removeErrorListeners()
    tree = parser.programa()

    #            SEMÁNTICO 
    semantico = AnalizadorSemantico()
    semantico.visit(tree)

    if semantico.errores:
        print("No se puede generar C3D (errores semánticos)")
        return

    #            TABLA 
    tabla_visitor = TablaSimbolosVisitor()
    tabla_visitor.visit(tree)

    if tabla_visitor.errores:
        print("No se puede generar C3D (errores en tabla)")
        return

    tabla = tabla_visitor.tabla_simbolos

    #            C3D 
    generador = C3DGenerador(tabla)
    generador.visit(tree)

    print("\n=== CÓDIGO 3 DIRECCIONES ===\n")

    for linea in generador.codigo:
        print(linea)


if __name__ == "__main__":
    main()