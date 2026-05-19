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


# VOCABULARIO COMPLETO ZIZU

VOCABULARIO = [

    # tipos
    "ontie",
    "flote",
    "duble",
    "shen",
    "vid",
    "cur",
    "lon",
    "sinie",
    "nonsinie",

    # control
    "wi",
    "otre",
    "pendan",
    "fer_pendan",
    "pur",
    "retur",
    "pos",
    "contine",
    "su",

    # switch
    "shangshe",
    "ca",
    "difu",

    # funciones
    "funcion",

    # io
    "amprimi",
    "lirf",

    # memoria
    "reserve",
    "reserveplu",
    "redimonsione",
    "gratui",

    # estructura
    "structiur",
    "lie",
    "enumere",
    "ga",

    # principal
    "principal",

    # simbolos
    "iyal",
    "puavir",
    "pasuvert",
    "pasferme",
    "cleuvert",
    "cleferme",

    # operadores
    "plu",
    "moan",
    "par",
    "bag",
    "minog",
    "aye",
    "compag",

    # comentarios
    "comenter",
    "lementer",
    "blomenter"
]


# NOMBRES DE TOKENS

NOMBRES_TOKENS = {

    # estructura
    "PRINCIPAL":           "principal",
    "FUNCION":             "funcion",
    "VID":                 "vid (void)",

    # control
    "WI":                  "wi (if)",
    "OTRE":                "otre (else)",
    "PENDAN":              "pendan (while)",
    "FER_PENDAN":          "fer_pendan (do while)",
    "PUR":                 "pur (for)",
    "RETUR":               "retur (return)",
    "POS":                 "pos (break)",
    "CONTINE":             "contine (continue)",
    "SU":                  "su (goto)",

    # switch
    "SHANGSHE":            "shangshe (switch)",
    "CA":                  "ca (case)",
    "DIFU":                "difu (default)",

    # tipos
    "ONTIE":               "ontie (int)",
    "FLOTE":               "flote (float)",
    "DUBLE":               "duble (double)",
    "SHEN":                "shen (string)",

    # io
    "AMPRIMI":             "amprimi (print)",
    "LIRF":                "lirf (scanf)",

    # simbolos
    "IGUAL":               "iyal (=)",
    "PUNTOCOMA":           "puavir (;)",
    "PARENTESIS_ABIERTO":  "pasuvert (()",
    "PARENTESIS_CERRADO":  "pasferme ())",
    "LLAVE_ABIERTA":       "cleuvert ({)",
    "LLAVE_CERRADA":       "cleferme (})",

    # operadores
    "OP":                  "operador",

    # generales
    "ID":                  "identificador",
    "INT":                 "numero entero",
    "FLOAT_LIT":           "numero decimal",
    "STRING":              "cadena de texto",

    # comentarios
    "COMMENT":             "comentario multilinea",
    "LINE_COMMENT":        "comentario linea",

    "EOF":                 "fin de archivo",
}


# SUGERENCIAS

def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(
        lexema,
        VOCABULARIO,
        n=1,
        cutoff=0.4
    )
    return sugerencias[0] if sugerencias else ""


# TRADUCCION TOKENS

def traducir_token(token_str):

    limpio = token_str.strip("'")

    return NOMBRES_TOKENS.get(
        limpio,
        token_str
    )


def traducir_conjunto(conjunto_str):

    tokens = re.findall(r"'([^']+)'", conjunto_str)

    if not tokens:
        return conjunto_str

    traducidos = [
        NOMBRES_TOKENS.get(t, t)
        for t in tokens
    ]

    return "{" + ", ".join(traducidos) + "}"


# TRADUCIR MENSAJES ANTLR

def traducir_mensaje_antlr(msg):

    # mismatched input
    m = re.match(
        r"mismatched input '(.+?)' expecting (.+)",
        msg
    )

    if m:

        encontrado = traducir_token(m.group(1))
        esperado = traducir_conjunto(m.group(2))

        return (
            f"Token inesperado '{encontrado}', "
            f"se esperaba: {esperado}"
        )

    # extraneous input
    m = re.match(
        r"extraneous input '(.+?)' expecting (.+)",
        msg
    )

    if m:

        encontrado = traducir_token(m.group(1))
        esperado = traducir_conjunto(m.group(2))

        return (
            f"Entrada extra '{encontrado}', "
            f"se esperaba: {esperado}"
        )

    # no viable alternative
    m = re.match(
        r"no viable alternative at input '(.+?)'",
        msg
    )

    if m:

        return (
            f"Construccion invalida en "
            f"'{m.group(1)}'"
        )

    # missing
    m = re.match(
        r"missing (.+?) at '(.+?)'",
        msg
    )

    if m:

        faltante = traducir_conjunto(m.group(1))
        en_donde = traducir_token(m.group(2))

        return (
            f"Falta {faltante} "
            f"antes de '{en_donde}'"
        )

    # token recognition
    m = re.match(
        r"token recognition error at: '(.+?)'",
        msg
    )

    if m:

        return (
            f"Simbolo no reconocido: "
            f"'{m.group(1)}'"
        )

    # input mismatch
    if "input mismatch" in msg.lower():

        return (
            "Error de sintaxis: "
            "token fuera de lugar"
        )

    # EOF
    if "EOF" in msg:
        msg = msg.replace(
            "EOF",
            "fin de archivo"
        )

    return msg


# ERROR LISTENER

class MiErrorListener(ErrorListener):

    def __init__(self):
        self.errores = []

    def syntaxError(
        self,
        recognizer,
        offendingSymbol,
        line,
        column,
        msg,
        e
    ):

        mensaje = traducir_mensaje_antlr(msg)

        if offendingSymbol is not None:

            sugerencia = sugerir_palabra(
                offendingSymbol.text
            )

            if sugerencia:

                mensaje += (
                    f" | Sugerencia: "
                    f"'{sugerencia}'"
                )

        self.errores.append({

            "linea":   line,
            "columna": column,
            "mensaje": mensaje,
            "tipo":    "Sintactico"
        })


# OBTENER TOKENS

def obtener_tokens(lexer):

    tokens = []

    token = lexer.nextToken()

    while token.type != Token.EOF:

        tipo = (
            lexer.symbolicNames[token.type]
            if token.type >= 0
            else "UNKNOWN"
        )

        if tipo not in ["WS"]:

            tokens.append({

                "linea":   token.line,
                "columna": token.column,
                "lexema":  token.text,
                "tipo":    tipo
            })

        token = lexer.nextToken()

    return tokens


# MAIN

def main():

    os.makedirs(
        os.path.join(ruta_raiz, "reportes_html"),
        exist_ok=True
    )

    archivo = os.path.join(
        ruta_raiz,
        "programa.leng"
    )


    # LEXICO


    input_stream = FileStream(
        archivo,
        encoding='utf-8'
    )

    lexer = LenguajeLexer(input_stream)

    tokens = obtener_tokens(lexer)

    errores_lexicos = []

    for t in tokens:

        if t["tipo"] == "ERROR_CHAR":

            sugerencia = sugerir_palabra(
                t["lexema"]
            )

            mensaje = (
                f"Simbolo no reconocido: "
                f"'{t['lexema']}'"
            )

            if sugerencia:

                mensaje += (
                    f" | Sugerencia: "
                    f"'{sugerencia}'"
                )

            errores_lexicos.append({

                "linea": t["linea"],
                "columna": t["columna"],
                "mensaje": mensaje,
                "tipo": "Lexico"
            })


    # SINTACTICO


    input_stream2 = FileStream(
        archivo,
        encoding='utf-8'
    )

    lexer2 = LenguajeLexer(input_stream2)

    stream = CommonTokenStream(lexer2)

    parser = LenguajeParser(stream)

    listener = MiErrorListener()

    parser.removeErrorListeners()
    parser.addErrorListener(listener)

    parser.programa()

    errores_sintacticos = listener.errores


    # SEMANTICO


    input_stream3 = FileStream(
        archivo,
        encoding='utf-8'
    )

    lexer3 = LenguajeLexer(input_stream3)

    stream3 = CommonTokenStream(lexer3)

    parser3 = LenguajeParser(stream3)

    parser3.removeErrorListeners()

    tree = parser3.programa()

    semantico = AnalizadorSemantico()

    semantico.visit(tree)

    errores_semanticos = semantico.errores


    # HTML FILAS


    def filas_lexicos():

        html = ""

        for e in errores_lexicos:

            html += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['mensaje']}</td>
                <td>{e['tipo']}</td>
            </tr>
            """

        return html


    def filas_sintacticos():

        html = ""

        for e in errores_sintacticos:

            html += f"""
            <tr>
                <td>{e['linea']}</td>
                <td>{e['columna']}</td>
                <td>{e['mensaje']}</td>
                <td>{e['tipo']}</td>
            </tr>
            """

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
            </tr>
            """

        return html



    # HTML BASE


    ruta_base = os.path.join(
        ruta_raiz,
        "reportes_html",
        "errores_base.html"
    )

    if not os.path.exists(ruta_base):

        print(
            "ERRORES: "
            "No se pudo generar reporte"
        )

        return

    with open(
        ruta_base,
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()


    # INSERTAR TABLAS


    html = html.replace(
        '<tbody id="tbody-lexico">',
        f'<tbody id="tbody-lexico">{filas_lexicos()}'
    )

    html = html.replace(
        '<tbody id="tbody-sintactico">',
        f'<tbody id="tbody-sintactico">{filas_sintacticos()}'
    )

    html = html.replace(
        '<tbody id="tbody-semantico">',
        f'<tbody id="tbody-semantico">{filas_semanticos()}'
    )


    # GUARDAR


    salida = os.path.join(
        ruta_raiz,
        "reportes_html",
        "reporte_errores.html"
    )

    with open(
        salida,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)


    # RESUMEN
    total = (
        len(errores_lexicos)
        + len(errores_sintacticos)
        + len(errores_semanticos)
    )

    if total == 0:

        print("Sin errores")

    elif total == 1:

        print("1 error encontrado")

    else:

        print(f"{total} errores encontrados")


# RUN

if __name__ == "__main__":
    main()