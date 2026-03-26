import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener


VOCABULARIO = ["variabli", "ontie", "flote", "duble", "amprimi"]

def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.6)
    return sugerencias[0] if sugerencias else ""


class MiErrorListener(ErrorListener):
    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


def procesar_tokens_recursivo(lexer, token, lista, errores_lexicos):
    if token.type == Token.EOF:
        return

    tipo = lexer.symbolicNames[token.type]

    if tipo == "ERROR_CHAR":
        sugerencia = sugerir_palabra(token.text)
        errores_lexicos.append({
            "linea": token.line,
            "columna": token.column,
            "lexema": token.text,
            "sugerencia": sugerencia
        })

    elif tipo != "WS":
        lista.append({
            "tipo": tipo,
            "lexema": token.text,
            "linea": token.line,
            "columna": token.column
        })

    siguiente = lexer.nextToken()
    procesar_tokens_recursivo(lexer, siguiente, lista, errores_lexicos)


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    # ───── LEXICO ─────
    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)

    tokens_lista = []
    errores_lexicos = []

    procesar_tokens_recursivo(lexer, lexer.nextToken(), tokens_lista, errores_lexicos)

    # ───── SINTACTICO ─────
    input_stream2 = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener_error = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener_error)

    parser.programa()

    # ───── VALIDACIONES ─────
    if errores_lexicos:
        print("Error léxico detectado")
        return

    if listener_error.hay_error:
        print("Error sintáctico detectado")
        return

    # ───── HTML BONITO ─────

    ruta_base = os.path.join(ruta_raiz, "reportes_html", "tokens_base.html")

    if not os.path.exists(ruta_base):
        print("ERROR: No existe tokens_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    filas = ""

    for t in tokens_lista:
        filas += f"""
        <tr>
            <td>{t['tipo']}</td>
            <td>{t['lexema']}</td>
            <td>{t['linea']}</td>
            <td>{t['columna']}</td>
        </tr>
        """

    html = html.replace(
        '<tbody id="tbody">',
        f'<tbody id="tbody">{filas}'
    )

    ruta_salida = os.path.join(ruta_raiz, "reportes_html", "reporte_tokens.html")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte de tokens generado")


if __name__ == "__main__":
    main()