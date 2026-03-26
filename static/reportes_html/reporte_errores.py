import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener


VOCABULARIO = [
    "ontie", "flote", "duble",
    "wi", "otre", "pendan", "retur",
    "amprimi", "principal",
    "iyal", "puavir", "pasuvert", "pasferme", "cleuvert", "cleferme",
    "plu", "moan", "par", "bag", "minog", "aye", "compag"
]

def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.4)
    return sugerencias[0] if sugerencias else ""


class MiErrorListener(ErrorListener):
    def __init__(self):
        self.errores = []  # ← antes decía: self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if offendingSymbol is not None and sugerir_palabra(offendingSymbol.text):
            return
        self.errores.append({
            "linea": line,
            "columna": column,
            "mensaje": msg
        })


def procesar_tokens(lexer):
    tokens_lista = []
    token = lexer.nextToken()

    while token.type != Token.EOF:
        tipo = lexer.symbolicNames[token.type] if token.type >= 0 else "UNKNOWN"

        if tipo != "WS":
            tokens_lista.append({
                "tipo": tipo,
                "lexema": token.text,
                "linea": token.line,
                "columna": token.column
            })

        token = lexer.nextToken()

    return tokens_lista


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    # ── LÉXICO ──
    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)
    errores_lexicos = procesar_tokens(lexer)

    # ── SINTÁCTICO ──
    input_stream2 = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    parser.programa()

    # ✅ Si no hay nada, salir sin generar HTML
    if not errores_lexicos and not listener.errores:
        print("Sin errores")
        return

    # ✅ Si hay errores, siempre generar el HTML
    ruta_base = os.path.join(ruta_raiz, "reportes_html", "errores_base.html")
    if not os.path.exists(ruta_base):
        print("ERROR: No existe errores_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    filas = ""
    for e in errores_lexicos:
        filas += f"""
        <tr>
            <td>Léxico</td>
            <td>{e['lexema']}</td>
            <td>{e['linea']}</td>
            <td>{e['columna']}</td>
        </tr>
        """

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

    print(f"Reporte de errores generado ({len(errores_lexicos)} léxicos, {len(listener.errores)} sintácticos)")


if __name__ == "__main__":
    main()