import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener


#  VOCABULARIO PARA SUGERENCIAS
VOCABULARIO = [
    "principal", "wi", "otre", "pendan", "retur",
    "ontie", "flote", "duble", "shen",
    "amprimi", "iyal",
    "puavir", "pasuvert", "pasferme",
    "cleuvert", "cleferme",
    "plu", "moan", "par", "bag", "minog", "aye", "compag",
    "comenter"
]


def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.6)
    return sugerencias[0] if sugerencias else ""


#  ERROR LISTENER
class MiErrorListener(ErrorListener):
    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


#  RECORRER TOKENS
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


#  EQUIVALENTE C++ (CON COMENTARIOS)
def obtener_equivalente(tipo, lexema):

    lex = lexema.lower()

    equivalencias = {
        # estructura
        "principal": "int main",
        "wi": "if",
        "otre": "else",
        "pendan": "while",
        "retur": "return",

        # tipos
        "ontie": "int",
        "flote": "float",
        "duble": "double",
        "shen": "string",

        # funciones
        "amprimi": "cout",

        # símbolos
        "iyal": "=",
        "puavir": ";",
        "pasuvert": "(",
        "pasferme": ")",
        "cleuvert": "{",
        "cleferme": "}",

        # operadores
        "plu": "+",
        "moan": "-",
        "par": "*",
        "bag": "/",
        "minog": "<",
        "aye": ">",
        "compag": "==",
    }

    # TRADUCCIÓN POR LEXEMA
    if lex in equivalencias:
        return equivalencias[lex]

    # COMENTARIOS → // texto
    if tipo == "COMENTER" or lex.startswith("comenter"):
        # quitar la palabra "comenter"
        contenido = lexema[len("comenter"):].strip()
        return f"// {contenido}"

    # números
    if tipo in ["INT", "FLOAT_LIT"]:
        return lexema

    # strings
    if tipo == "STRING":
        return lexema

    # identificadores
    if tipo == "ID":
        return lexema

    return ""


#  MAIN
def main():

    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    ruta_salida = os.path.join(ruta_raiz, "reportes_html", "reporte_tokens.html")

    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    archivo = os.path.join(ruta_raiz, "programa.leng")

    # LEXER
    input_stream = FileStream(archivo, encoding="utf-8")
    lexer = LenguajeLexer(input_stream)

    tokens_lista = []
    errores_lexicos = []

    procesar_tokens_recursivo(lexer, lexer.nextToken(), tokens_lista, errores_lexicos)

    # PARSER
    input_stream2 = FileStream(archivo, encoding="utf-8")
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener_error = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener_error)

    parser.programa()

    # VALIDACIONES
    if errores_lexicos:
        print("0 tokens (error lexico)")
        return

    if listener_error.hay_error:
        print("0 tokens (error sintactico)")
        return

    # HTML BASE
    ruta_base = os.path.join(ruta_raiz, "reportes_html", "tokens_base.html")

    if not os.path.exists(ruta_base):
        print("ERROR: No existe tokens_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    # GENERAR FILAS
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
        </tr>
        """

    # INSERTAR EN HTML
    html = html.replace(
        '<tbody id="tbody">',
        f'<tbody id="tbody">{filas}'
    )

    # GUARDAR 
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html)

    cantidad = len(tokens_lista)

    if cantidad == 0:
        print("Sin tokens")
    elif cantidad == 1:
        print("1 token encontrado")
    else:
        print(f"{cantidad} tokens encontrados")


#  RUN
if __name__ == "__main__":
    main()