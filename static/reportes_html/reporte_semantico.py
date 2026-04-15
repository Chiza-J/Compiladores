import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr_todo.AnalizadorSemantico import AnalizadorSemantico


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    archivo = os.path.join(ruta_raiz, "programa.leng")

    input_stream = FileStream(archivo, encoding="utf-8")
    lexer        = LenguajeLexer(input_stream)
    stream       = CommonTokenStream(lexer)
    parser       = LenguajeParser(stream)

    # Silenciar errores del parser (ya los reporta reporte_errores.py)
    parser.removeErrorListeners()

    tree = parser.programa()

    semantico = AnalizadorSemantico()
    semantico.visit(tree)

    errores = semantico.errores

    # ---- Construir filas HTML ----
    if not errores:
        filas = ""
    else:
        filas = ""
        for e in errores:
            filas += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['mensaje']}</td>
                <td>{e['tipo']}</td>
            </tr>
            """

    # ---- Cargar base HTML ----
    ruta_base = os.path.join(ruta_raiz, "reportes_html", "semantico_base.html")

    if not os.path.exists(ruta_base):
        print("SEMANTICO: No se encontró semantico_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace('<tbody id="tbody">', f'<tbody id="tbody">{filas}')

    salida = os.path.join(ruta_raiz, "reportes_html", "reporte_semantico.html")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)

    total = len(errores)
    if total == 0:
        print("Sin errores semánticos")
    elif total == 1:
        print("1 error semántico encontrado")
    else:
        print(f"{total} errores semánticos encontrados")


if __name__ == "__main__":
    main()