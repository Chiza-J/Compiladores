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
    "principal", "wi", "otre", "pendan", "fer_pendan", "pur",
    "shangshe", "ca", "difu", "pos", "contine", "su",
    "retur", "funcion", "vid", "lirf",
    "ontie", "flote", "duble", "shen",
    "amprimi",
    "iyal", "puavir", "pasuvert", "pasferme", "cleuvert", "cleferme",
    "plu", "moan", "par", "bag", "minog", "aye", "compag",
    "comenter"
]


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
            "linea":      token.line,
            "columna":    token.column,
            "lexema":     token.text,
            "sugerencia": sugerencia
        })
    elif tipo != "WS":
        lista.append({
            "tipo":    tipo,
            "lexema":  token.text,
            "linea":   token.line,
            "columna": token.column
        })

    siguiente = lexer.nextToken()
    procesar_tokens_recursivo(lexer, siguiente, lista, errores_lexicos)


def obtener_equivalente(tipo, lexema):
    lex = lexema.lower()

    equivalencias = {
        "principal":  "int main",
        "wi":         "if",
        "otre":       "else",
        "pendan":     "while",
        "fer_pendan": "do { } while",
        "pur":        "for",
        "shangshe":   "switch",
        "ca":         "case",
        "difu":       "default",
        "pos":        "break",
        "contine":    "continue",
        "su":         "goto",
        "retur":      "return",
        "funcion":    "function",
        "vid":        "void",
        "lirf":       "scanf",
        "ontie":      "int",
        "flote":      "float",
        "duble":      "double",
        "shen":       "string",
        "amprimi":    "printf",
        "iyal":       "=",
        "puavir":     ";",
        "pasuvert":   "(",
        "pasferme":   ")",
        "cleuvert":   "{",
        "cleferme":   "}",
        "plu":        "+",
        "moan":       "-",
        "par":        "*",
        "bag":        "/",
        "minog":      "<",
        "aye":        ">",
        "compag":     "==",
    }

    if lex in equivalencias:
        return equivalencias[lex]

    if tipo in ["INT", "FLOAT_LIT", "STRING", "ID"]:
        return lexema

    return ""


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    ruta_salida = os.path.join(ruta_raiz, "reportes_html", "reporte_tokens.html")
    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    archivo = os.path.join(ruta_raiz, "programa.leng")

    input_stream = FileStream(archivo, encoding="utf-8")
    lexer = LenguajeLexer(input_stream)

    tokens_lista    = []
    errores_lexicos = []
    procesar_tokens_recursivo(lexer, lexer.nextToken(), tokens_lista, errores_lexicos)

    input_stream2 = FileStream(archivo, encoding="utf-8")
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener_error = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener_error)
    parser.programa()

    if errores_lexicos:
        print("0 tokens (error lexico)")
        return

    if listener_error.hay_error:
        print("0 tokens (error sintactico)")
        return

    ruta_base = os.path.join(ruta_raiz, "reportes_html", "tokens_base.html")
    if not os.path.exists(ruta_base):
        print("ERROR: No existe tokens_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    filas = ""
    for t in tokens_lista:
        equivalente = obtener_equivalente(t['tipo'], t['lexema'])
        filas += f"""
        <tr>
            <td>{t['tipo']}</td>
            <td>{t['lexema']}</td>
            <td>{t['linea']}</td>
            <td>{t['columna']}</td>
            <td>{equivalente}</td>
        </tr>"""

    html = html.replace('<tbody id="tbody">', f'<tbody id="tbody">{filas}')

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html)

    cantidad = len(tokens_lista)
    if cantidad == 0:
        print("Sin tokens")
    elif cantidad == 1:
        print("1 token encontrado")
    else:
        print(f"{cantidad} tokens encontrados")


if __name__ == "__main__":
    main()