import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer


VOCABULARIO = [
    "principal", "wi", "otre", "pendan", "fer_pendan", "pur",
    "shangshe", "ca", "difu", "pos", "contine", "su",
    "retur", "funcion", "vid", "lirf",
    "ontie", "flote", "duble", "shen",
    "amprimi",
    "iyal", "puavir", "pasuvert", "pasferme", "cleuvert", "cleferme",
    "plu", "moan", "par", "bag", "minog", "aye", "compag"
]


def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.4)
    return sugerencias[0] if sugerencias else ""


def procesar_tokens(lexer):
    recuperables = []
    token = lexer.nextToken()

    while token.type != Token.EOF:
        tipo   = lexer.symbolicNames[token.type] if token.type >= 0 else "UNKNOWN"
        lexema = token.text

        if tipo == "ERROR_CHAR":
            sugerencia = sugerir_palabra(lexema)
            if sugerencia:
                recuperables.append({
                    "linea":      token.line,
                    "columna":    token.column,
                    "lexema":     lexema,
                    "sugerencia": sugerencia
                })
        elif tipo == "ID":
            sugerencia = sugerir_palabra(lexema)
            if sugerencia:
                recuperables.append({
                    "linea":      token.line,
                    "columna":    token.column,
                    "lexema":     lexema,
                    "sugerencia": sugerencia
                })

        token = lexer.nextToken()

    return recuperables


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"), encoding='utf-8')
    lexer = LenguajeLexer(input_stream)
    recuperables = procesar_tokens(lexer)

    ruta_base = os.path.join(ruta_raiz, "reportes_html", "recuperables_base.html")
    if not os.path.exists(ruta_base):
        print("ERROR: No existe recuperables_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    filas = ""
    for r in recuperables:
        filas += f"""
        <tr>
            <td>{r['linea']}</td>
            <td>{r['columna']}</td>
            <td>{r['lexema']}</td>
            <td>{r['sugerencia']}</td>
        </tr>"""

    html = html.replace('<tbody id="tbody">', f'<tbody id="tbody">{filas}')

    with open(os.path.join(ruta_raiz, "reportes_html", "reporte_recuperables.html"), "w", encoding="utf-8") as f:
        f.write(html)

    total = len(recuperables)
    if total == 0:
        print("Sin recuperables")
    elif total == 1:
        print("1 recuperable encontrado")
    else:
        print(f"{total} recuperables encontrados")


if __name__ == "__main__":
    main()