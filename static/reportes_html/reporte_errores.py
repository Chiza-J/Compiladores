import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener


#VOCABULARIO 
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

    input_stream = FileStream(archivo)
    lexer = LenguajeLexer(input_stream)

    tokens = obtener_tokens(lexer)

    # 🔥 SOLO errores reales
    errores_lexicos = [t for t in tokens if t["tipo"] == "ERROR_CHAR"]

    input_stream2 = FileStream(archivo)
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    parser.programa()

    errores_sintacticos = listener.errores

    # SI NO HAY ERRORES, IGUAL GENERAR REPORTE VACÍO
    if not errores_lexicos and not errores_sintacticos:
        filas = """
        <tr>
            <td colspan="4">Sin errores</td>
        </tr>
        """
    else:
        filas = ""

        for e in errores_lexicos:
            filas += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['lexema']}</td>
                <td>Léxico</td>
            </tr>
            """

        for e in errores_sintacticos:
            filas += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['lexema']}</td>
                <td>Sintactico</td>
            </tr>
            """

    #LLAMA LA BASE DE HTML LA INTERFAZ BONITA
    ruta_base = os.path.join(ruta_raiz, "reportes_html", "errores_base.html")

    if not os.path.exists(ruta_base):
        print("ERRORES: No se pudo generar reporte")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    filas = ""

    # ERRORES LÉXICOS
    for e in errores_lexicos:
        filas += f"""
        <tr>
            <td>{e['linea']}</td>
            <td>{e['columna']}</td>
            <td>{e['lexema']}</td>
            <td>Léxico</td>
        </tr>
        """

    # ERRORES SINTÁCTICOS
    for e in errores_sintacticos:
        filas += f"""
        <tr>
            <td>{e['linea']}</td>
            <td>{e['columna']}</td>
            <td>{e['lexema']}</td>
            <td>Sintactico</td>
        </tr>
        """

    html = html.replace('<tbody id="tbody">', f'<tbody id="tbody">{filas}')

    salida = os.path.join(ruta_raiz, "reportes_html", "reporte_errores.html")

    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)

    total_errores = len(errores_lexicos) + len(errores_sintacticos)

    if total_errores == 0:
        print("Sin errores")
    elif total_errores == 1:
        print("1 error encontrado")
    else:
        print(f"{total_errores} errores encontrados")


if __name__ == "__main__":
    main()