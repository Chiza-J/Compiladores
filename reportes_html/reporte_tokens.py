import sys
import os

# Ruta para encontrar el lexer en la carpeta padre
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_raiz)

from antlr4 import *
from LenguajeLexer import LenguajeLexer


# 🔁 FUNCIÓN RECURSIVA
def procesar_tokens_recursivo(lexer, token, lista):
    if token.type == Token.EOF:
        return

    tipo = lexer.symbolicNames[token.type]

    # Ignorar espacios
    if tipo != "WS":
        lista.append({
            "tipo": tipo,
            "lexema": token.text,
            "linea": token.line,
            "columna": token.column
        })

    siguiente = lexer.nextToken()
    procesar_tokens_recursivo(lexer, siguiente, lista)


def main():
    os.makedirs("reportes_html", exist_ok=True)

    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)

    tokens_lista = []

    primer_token = lexer.nextToken()
    procesar_tokens_recursivo(lexer, primer_token, tokens_lista)

    # Generar HTML
    html = """
    <html>
    <head><title>Reporte de Tokens</title></head>
    <body>
    <h1>Reporte de Tokens</h1>
    <table border="1">
    <tr><th>Tipo</th><th>Lexema</th><th>Línea</th><th>Columna</th></tr>
    """

    for t in tokens_lista:
        html += f"""
        <tr>
            <td>{t['tipo']}</td>
            <td>{t['lexema']}</td>
            <td>{t['linea']}</td>
            <td>{t['columna']}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open(os.path.join(ruta_raiz, "reportes_html", "reporte_tokens.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte de tokens generado ✔")


if __name__ == "__main__":
    main()