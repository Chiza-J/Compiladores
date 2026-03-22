import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener


# Listener de errores
class MiErrorListener(ErrorListener):
    def __init__(self):
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errores.append({
            "linea": line,
            "columna": column,
            "mensaje": msg
        })


def procesar_errores_recursivo(lista, index, html):
    if index >= len(lista):
        return html

    e = lista[index]

    html += f"""
    <tr>
        <td>{e['linea']}</td>
        <td>{e['columna']}</td>
        <td>{e['mensaje']}</td>
    </tr>
    """

    return procesar_errores_recursivo(lista, index + 1, html)


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LenguajeParser(stream)

    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)

    parser.programa()

    # HTML base
    html = """
    <html>
    <head><title>Errores</title></head>
    <body>
    <h1>Errores Sintácticos</h1>
    <table border="1">
    <tr><th>Línea</th><th>Columna</th><th>Mensaje</th></tr>
    """

    # se aplica recursividad
    html = procesar_errores_recursivo(listener.errores, 0, html)

    html += "</table></body></html>"

    with open(os.path.join(ruta_raiz, "reportes_html", "reporte_errores.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte de errores generado")


if __name__ == "__main__":
    main()