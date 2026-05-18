import sys
import os
import difflib
import re

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr_todo.AnalizadorSemantico import AnalizadorSemantico


VOCABULARIO = [
    "ontie", "flote", "duble", "shen",
    "wi", "otre", "pendan", "retur",
    "amprimi", "principal",
    "iyal", "puavir", "pasuvert", "pasferme", "cleuvert", "cleferme",
    "plu", "moan", "par", "bag", "minog", "aye", "compag"
]

# Mapeo de tokens ANTLR a nombres legibles en espanol
NOMBRES_TOKENS = {
    "PRINCIPAL":           "principal",
    "WI":                  "wi (if)",
    "OTRE":                "otre (else)",
    "PENDAN":              "pendan (while)",
    "RETUR":               "retur (return)",
    "ONTIE":               "ontie (int)",
    "FLOTE":               "flote (float)",
    "DUBLE":               "duble (double)",
    "SHEN":                "shen (varchar)",
    "AMPRIMI":             "amprimi (print)",
    "IGUAL":               "iyal (=)",
    "PUNTOCOMA":           "puavir (;)",
    "PARENTESIS_ABIERTO":  "pasuvert ((",
    "PARENTESIS_CERRADO":  "pasferme ())",
    "LLAVE_ABIERTA":       "cleuvert ({)",
    "LLAVE_CERRADA":       "cleferme (})",
    "OP":                  "operador",
    "ID":                  "identificador",
    "INT":                 "numero entero",
    "FLOAT_LIT":           "numero decimal",
    "STRING":              "cadena de texto",
    "EOF":                 "fin de archivo",
}


def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.4)
    return sugerencias[0] if sugerencias else ""


def traducir_token(token_str):
    # quita comillas simples si las tiene
    limpio = token_str.strip("'")
    return NOMBRES_TOKENS.get(limpio, token_str)


def traducir_conjunto(conjunto_str):
    # traduce listas como {'puavir', 'cleferme'} a espanol
    tokens = re.findall(r"'([^']+)'", conjunto_str)
    if not tokens:
        return conjunto_str
    traducidos = [NOMBRES_TOKENS.get(t, t) for t in tokens]
    return "{" + ", ".join(traducidos) + "}"


def traducir_mensaje_antlr(msg):
    # mismatched input 'X' expecting Y
    m = re.match(r"mismatched input '(.+?)' expecting (.+)", msg)
    if m:
        encontrado  = traducir_token(m.group(1))
        esperado    = traducir_conjunto(m.group(2))
        return f"Token inesperado '{encontrado}', se esperaba: {esperado}"

    # extraneous input 'X' expecting Y
    m = re.match(r"extraneous input '(.+?)' expecting (.+)", msg)
    if m:
        encontrado = traducir_token(m.group(1))
        esperado   = traducir_conjunto(m.group(2))
        return f"Entrada extra '{encontrado}', se esperaba: {esperado}"

    # no viable alternative at input 'X'
    m = re.match(r"no viable alternative at input '(.+?)'", msg)
    if m:
        return f"Construccion invalida en '{m.group(1)}'"

    # missing X at Y
    m = re.match(r"missing (.+?) at '(.+?)'", msg)
    if m:
        faltante  = traducir_conjunto(m.group(1))
        en_donde  = traducir_token(m.group(2))
        return f"Falta {faltante} antes de '{en_donde}'"

    # token recognition error at: 'X'
    m = re.match(r"token recognition error at: '(.+?)'", msg)
    if m:
        return f"Simbolo no reconocido: '{m.group(1)}'"

    # input mismatch
    if "input mismatch" in msg.lower():
        return "Error de sintaxis: token fuera de lugar"

    # EOF
    if "EOF" in msg:
        msg = msg.replace("EOF", "fin de archivo")

    return msg


class MiErrorListener(ErrorListener):
    def __init__(self):
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # traducir mensaje de ingles a espanol
        mensaje = traducir_mensaje_antlr(msg)

        # agregar sugerencia si hay un lexema cercano al vocabulario
        if offendingSymbol is not None:
            sugerencia = sugerir_palabra(offendingSymbol.text)
            if sugerencia:
                mensaje += f" | Sugerencia: '{sugerencia}'"

        self.errores.append({
            "linea":   line,
            "columna": column,
            "mensaje": mensaje
        })


def obtener_tokens(lexer):
    tokens = []
    token = lexer.nextToken()
    while token.type != Token.EOF:
        tipo = lexer.symbolicNames[token.type] if token.type >= 0 else "UNKNOWN"
        if tipo not in ["WS", "COMMENT", "LINE_COMMENT"]:
            tokens.append({
                "linea":   token.line,
                "columna": token.column,
                "lexema":  token.text,
                "tipo":    tipo
            })
        token = lexer.nextToken()
    return tokens


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    archivo = os.path.join(ruta_raiz, "programa.leng")

    # Errores lexicos
    input_stream = FileStream(archivo, encoding='utf-8')
    lexer = LenguajeLexer(input_stream)
    tokens = obtener_tokens(lexer)
    errores_lexicos = [t for t in tokens if t["tipo"] == "ERROR_CHAR"]

    # Errores sintacticos
    input_stream2 = FileStream(archivo, encoding='utf-8')
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    parser.programa()

    errores_sintacticos = listener.errores

    # Errores semanticos
    input_stream3 = FileStream(archivo, encoding='utf-8')
    lexer3 = LenguajeLexer(input_stream3)
    stream3 = CommonTokenStream(lexer3)
    parser3 = LenguajeParser(stream3)
    parser3.removeErrorListeners()
    tree = parser3.programa()

    semantico = AnalizadorSemantico()
    semantico.visit(tree)
    errores_semanticos = semantico.errores

    # Construir filas HTML
    def filas_lexicos():
        html = ""
        for e in errores_lexicos:
            html += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>Simbolo no reconocido: '{e['lexema']}'</td>
                <td>Lexico</td>
            </tr>"""
        return html

    def filas_sintacticos():
        html = ""
        for e in errores_sintacticos:
            html += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['mensaje']}</td>
                <td>Sintactico</td>
            </tr>"""
        return html

    def filas_semanticos():
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

    # Cargar base HTML
    ruta_base = os.path.join(ruta_raiz, "reportes_html", "errores_base.html")
    if not os.path.exists(ruta_base):
        print("ERRORES: No se pudo generar reporte")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace('<tbody id="tbody-lexico">',
                        f'<tbody id="tbody-lexico">{filas_lexicos()}')
    html = html.replace('<tbody id="tbody-sintactico">',
                        f'<tbody id="tbody-sintactico">{filas_sintacticos()}')
    html = html.replace('<tbody id="tbody-semantico">',
                        f'<tbody id="tbody-semantico">{filas_semanticos()}')

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