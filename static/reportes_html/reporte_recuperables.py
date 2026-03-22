import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer


def procesar_recuperables_recursivo(lexer, token, errores):
    if token.type == Token.EOF:
        return

    tipo = lexer.symbolicNames[token.type]

    if tipo == "ERROR_CHAR":
        errores.append({
            "linea": token.line,
            "columna": token.column,
            "mensaje": f"Símbolo no reconocido: {token.text}"
        })

    siguiente = lexer.nextToken()
    procesar_recuperables_recursivo(lexer, siguiente, errores)


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)

    errores = []

    primer_token = lexer.nextToken()
    procesar_recuperables_recursivo(lexer, primer_token, errores)

    # HTML
    html = """
    <html>
    <head><title>Errores Recuperables</title></head>
    <body>
    <h1>Errores Léxicos (Recuperables)</h1>
    <table border="1">
    <tr><th>Línea</th><th>Columna</th><th>Mensaje</th></tr>
    """

    for e in errores:
        html += f"""
        <tr>
            <td>{e['linea']}</td>
            <td>{e['columna']}</td>
            <td>{e['mensaje']}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open(os.path.join(ruta_raiz, "reportes_html", "reporte_recuperables.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte de recuperables generado")


if __name__ == "__main__":
    main()