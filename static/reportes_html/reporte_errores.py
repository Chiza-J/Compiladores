import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener


class MiErrorListener(ErrorListener):
    def __init__(self):
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errores.append({
            "linea": line,
            "columna": column,
            "mensaje": msg
        })


def procesar_tokens_recursivo(lexer, token, errores_lexicos):
    if token.type == Token.EOF:
        return

    tipo = lexer.symbolicNames[token.type]

    # ✔ SOLO error real (sin sugerencias)
    if tipo == "ERROR_CHAR":
        errores_lexicos.append({
            "linea": token.line,
            "columna": token.column,
            "lexema": token.text
        })

    procesar_tokens_recursivo(lexer, lexer.nextToken(), errores_lexicos)


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    # ── LÉXICO ──
    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)

    errores_lexicos = []
    procesar_tokens_recursivo(lexer, lexer.nextToken(), errores_lexicos)

    # ── SINTÁCTICO ──
    input_stream2 = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)

    parser.programa()

    # 🚨 CLAVE: si no hay errores → NO generar HTML
    if not errores_lexicos and not listener.errores:
        print("Sin errores")
        return

    ruta_base = os.path.join(ruta_raiz, "reportes_html", "errores_base.html")

    if not os.path.exists(ruta_base):
        print("ERROR: No existe errores_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    filas = ""

    # ── ERRORES LÉXICOS ──
    for e in errores_lexicos:
        filas += f"""
        <tr>
            <td>Léxico</td>
            <td>{e['lexema']}</td>
            <td>{e['linea']}</td>
            <td>{e['columna']}</td>
        </tr>
        """

    # ── ERRORES SINTÁCTICOS ──
    for e in listener.errores:
        filas += f"""
        <tr>
            <td>Sintáctico</td>
            <td>{e['mensaje']}</td>
            <td>{e['linea']}</td>
            <td>{e['columna']}</td>
        </tr>
        """

    html = html.replace('<tbody id="tbody">', f'<tbody id="tbody">{filas}')

    with open(os.path.join(ruta_raiz, "reportes_html", "reporte_errores.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte de errores generado")


if __name__ == "__main__":
    main()