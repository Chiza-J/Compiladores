import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_raiz)

from antlr4 import *
from LenguajeLexer import LenguajeLexer
from LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener

VOCABULARIO = [
    "variabli",
    "ontie",
    "flote",
    "duble",
    "amprimi"
]


# SUGERENCIAS PARA EL VOCABULARIO
def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.6)
    return sugerencias[0] if sugerencias else ""


# ERROR SINTÁCTICO 
class MiErrorListener(ErrorListener):
    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


# RECURSIVIDAD
def procesar_tokens_recursivo(lexer, token, lista, errores_lexicos):
    if token.type == Token.EOF:
        return

    tipo = lexer.symbolicNames[token.type]

    # ERROR LÉXICO + SUGERENCIA
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
    os.makedirs("reportes_html", exist_ok=True)

    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)

    tokens_lista = []
    errores_lexicos = []

    primer_token = lexer.nextToken()
    procesar_tokens_recursivo(lexer, primer_token, tokens_lista, errores_lexicos)

    input_stream2 = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)

    parser.programa()

    # ERROR LÉXICO
    if errores_lexicos:
        print("Error LÉXICO detectado\n")

        for e in errores_lexicos:
            if e["sugerencia"]:
                print(f"Línea {e['linea']}: '{e['lexema']}' → ¿Quiso decir '{e['sugerencia']}'?")
            else:
                print(f"Línea {e['linea']}: símbolo no reconocido '{e['lexema']}'")

        return

    # ERROR SINTÁCTICO
    if listener.hay_error:
        print("Error SINTÁCTICO detectado")
        return

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

    print("Reporte de tokens generado")


if __name__ == "__main__":
    main()