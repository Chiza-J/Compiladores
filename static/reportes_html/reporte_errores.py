import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr_todo.AnalizadorSemantico import AnalizadorSemantico


# VOCABULARIO
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
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if offendingSymbol is not None:
            sugerencia = sugerir_palabra(offendingSymbol.text)
            if sugerencia:
                msg += f" | Sugerencia: '{sugerencia}'"

        self.errores.append({
            "linea": line,
            "columna": column,
            "mensaje": msg
        })


def obtener_tokens(lexer):
    tokens = []
    token = lexer.nextToken()

    while token.type != Token.EOF:
        tipo = lexer.symbolicNames[token.type] if token.type >= 0 else "UNKNOWN"

        if tipo not in ["WS", "COMMENT", "LINE_COMMENT"]:
            tokens.append({
                "linea": token.line,
                "columna": token.column,
                "lexema": token.text,
                "tipo": tipo
            })

        token = lexer.nextToken()

    return tokens


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    archivo = os.path.join(ruta_raiz, "programa.leng")

    # ── Errores léxicos ──────────────────────────────────────────────
    input_stream = FileStream(archivo)
    lexer = LenguajeLexer(input_stream)
    tokens = obtener_tokens(lexer)
    errores_lexicos = [t for t in tokens if t["tipo"] == "ERROR_CHAR"]

    # ── Errores sintácticos ──────────────────────────────────────────
    input_stream2 = FileStream(archivo)
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    parser.programa()

    errores_sintacticos = listener.errores

    # ── Errores semánticos ───────────────────────────────────────────
    input_stream3 = FileStream(archivo, encoding="utf-8")
    lexer3 = LenguajeLexer(input_stream3)
    stream3 = CommonTokenStream(lexer3)
    parser3 = LenguajeParser(stream3)
    parser3.removeErrorListeners()
    tree = parser3.programa()

    semantico = AnalizadorSemantico()
    semantico.visit(tree)
    errores_semanticos = semantico.errores

    # ── Construir filas HTML por pestaña ─────────────────────────────
    def filas_lexicos():
        if not errores_lexicos:
            return ""
        html = ""
        for e in errores_lexicos:
            html += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['lexema']}</td>
                <td>Léxico</td>
            </tr>"""
        return html

    def filas_sintacticos():
        if not errores_sintacticos:
            return ""
        html = ""
        for e in errores_sintacticos:
            html += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['mensaje']}</td>
                <td>Sintáctico</td>
            </tr>"""
        return html

    def filas_semanticos():
        if not errores_semanticos:
            return ""
        html = ""
        for e in errores_semanticos:
            html += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['mensaje']}</td>
                <td>{e['tipo']}</td>
            </tr>"""
        return html

    # ── Cargar base HTML ─────────────────────────────────────────────
    ruta_base = os.path.join(ruta_raiz, "reportes_html", "errores_base.html")

    if not os.path.exists(ruta_base):
        print("ERRORES: No se pudo generar reporte")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    # Inyectar filas en cada tbody de cada pestaña
    html = html.replace('<tbody id="tbody-lexico">',
                        f'<tbody id="tbody-lexico">{filas_lexicos()}')
    html = html.replace('<tbody id="tbody-sintactico">',
                        f'<tbody id="tbody-sintactico">{filas_sintacticos()}')
    html = html.replace('<tbody id="tbody-semantico">',
                        f'<tbody id="tbody-semantico">{filas_semanticos()}')

    # ── Guardar reporte final ────────────────────────────────────────
    salida = os.path.join(ruta_raiz, "reportes_html", "reporte_errores.html")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)

    total = len(errores_lexicos) + len(errores_sintacticos) + len(errores_semanticos)

    if total == 0:
        print("Sin errores")
    elif total == 1:
        print("1 error encontrado")
    else:
        print(f"{total} errores encontrados")


if __name__ == "__main__":
    main()