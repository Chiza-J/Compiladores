import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer


VOCABULARIO = ["variabli", "ontie", "flote", "duble", "amprimi"]


def sugerir_palabra(lexema):
    # 🔥 Bajamos el cutoff para detectar más errores tipo "onti"
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.4)
    return sugerencias[0] if sugerencias else ""


def procesar_tokens_recursivo(lexer, token, recuperables):
    while token.type != Token.EOF:
        tipo = lexer.symbolicNames[token.type]
        lexema = token.text

        # 🔥 CASO 1: ERROR_CHAR (como antes)
        if tipo == "ERROR_CHAR":
            sugerencia = sugerir_palabra(lexema)

            recuperables.append({
                "lexema": lexema,
                "sugerencia": sugerencia if sugerencia else "Sin sugerencia",
                "linea": token.line,
                "columna": token.column
            })

        # 🔥 CASO 2: ID MAL ESCRITO (ESTO ES LO QUE TE FALTABA)
        elif tipo == "ID":
            sugerencia = sugerir_palabra(lexema)

            if sugerencia:  # solo si hay algo parecido
                recuperables.append({
                    "lexema": lexema,
                    "sugerencia": sugerencia,
                    "linea": token.line,
                    "columna": token.column
                })

        token = lexer.nextToken()

    # 🔹 Último buffer (por si termina en error)
    if buffer_error:
        sugerencia = sugerir_palabra(buffer_error)

        recuperables.append({
            "lexema": buffer_error,
            "sugerencia": sugerencia if sugerencia else "Sin sugerencia",
            "linea": linea_inicio,
            "columna": columna_inicio
        })


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)

    recuperables = []
    procesar_tokens_recursivo(lexer, lexer.nextToken(), recuperables)

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
            <td>{r['lexema']}</td>
            <td>{r['sugerencia']}</td>
            <td>{r['linea']}</td>
            <td>{r['columna']}</td>
        </tr>
        """

    # 🔥 IMPORTANTE: mantiene el diseño bonito
    html = html.replace('<tbody id="tbody">', f'<tbody id="tbody">{filas}')

    with open(os.path.join(ruta_raiz, "reportes_html", "reporte_recuperables.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte de recuperables generado")


if __name__ == "__main__":
    main()