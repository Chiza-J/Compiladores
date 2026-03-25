import sys
import os
import difflib

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener


# ─────────────────────────────────────────────
#  VOCABULARIO
# ─────────────────────────────────────────────
VOCABULARIO = [
    "variabli",
    "ontie",
    "flote",
    "duble",
    "amprimi"
]


# ─────────────────────────────────────────────
#  SUGERENCIAS PARA VOCABULARIO
# ─────────────────────────────────────────────
def sugerir_palabra(lexema):
    sugerencias = difflib.get_close_matches(lexema, VOCABULARIO, n=1, cutoff=0.6)
    return sugerencias[0] if sugerencias else ""


# ─────────────────────────────────────────────
#  ERROR SINTÁCTICO
# ─────────────────────────────────────────────
class MiErrorListener(ErrorListener):
    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


# ─────────────────────────────────────────────
#  ANALIZADOR SEMÁNTICO (Listener sobre el árbol)
#
#  Recorre cada nodo `declaracion` del árbol y verifica:
#
#  ONTIE:
#    - El valor asignado NO puede ser un ID que no exista en la
#      tabla de símbolos.
#    - El valor asignado NO puede ser un ID declarado como flote/duble.
#    - El valor asignado PUEDE ser un INT literal o una variable ontie.
#
#  FLOTE / DUBLE:
#    - El valor asignado puede ser INT, FLOAT_LIT o cualquier variable
#      numérica ya declarada.
#
#  También detecta redeclaración de variables.
# ─────────────────────────────────────────────
class AnalizadorSemantico(ParseTreeListener):
    def __init__(self):
        self.tabla_simbolos = {}   # { nombre: tipo }
        self.errores = []          # lista de strings con los mensajes

    # ── helpers ──────────────────────────────

    def _tipo_expr_entera(self, ctx):
        """
        Recorre un nodo expr_entera y devuelve 'ontie' si es válido,
        o None si contiene un ID inválido (registrando el error).
        """
        # Hoja INT literal → siempre válido para ontie
        if ctx.INT():
            return 'ontie'

        # Hoja ID → debe existir y ser de tipo ontie
        if ctx.ID():
            nombre = ctx.ID().getText()
            if nombre not in self.tabla_simbolos:
                self.errores.append(
                    f"[Línea {ctx.start.line}] Error semántico: "
                    f"'{nombre}' no ha sido declarado."
                )
                return None
            tipo_var = self.tabla_simbolos[nombre]
            if tipo_var != 'ontie':
                self.errores.append(
                    f"[Línea {ctx.start.line}] Error de tipo: "
                    f"'ontie' no acepta '{nombre}' porque es de tipo '{tipo_var}'."
                )
                return None
            return 'ontie'

        # Nodo recursivo: expr_entera OP expr_entera
        izq = self._tipo_expr_entera(ctx.expr_entera(0))
        der = self._tipo_expr_entera(ctx.expr_entera(1))
        return 'ontie' if (izq == 'ontie' and der == 'ontie') else None

    def _tipo_expr_decimal(self, ctx):
        """
        Recorre un nodo expr_decimal y devuelve el tipo resultante,
        o None si hay un ID inválido (registrando el error).
        """
        if ctx.FLOAT_LIT():
            return 'flote'
        if ctx.INT():
            return 'ontie'
        if ctx.ID():
            nombre = ctx.ID().getText()
            if nombre not in self.tabla_simbolos:
                self.errores.append(
                    f"[Línea {ctx.start.line}] Error semántico: "
                    f"'{nombre}' no ha sido declarado."
                )
                return None
            return self.tabla_simbolos[nombre]

        # Nodo recursivo: expr_decimal OP expr_decimal
        izq = self._tipo_expr_decimal(ctx.expr_decimal(0))
        der = self._tipo_expr_decimal(ctx.expr_decimal(1))
        if izq is None or der is None:
            return None
        return 'flote' if ('flote' in (izq, der) or 'duble' in (izq, der)) else 'ontie'

    # ── listener ─────────────────────────────

    def enterDeclaracion(self, ctx: LenguajeParser.DeclaracionContext):
        nombre = ctx.ID().getText()
        linea  = ctx.start.line

        # Redeclaración
        if nombre in self.tabla_simbolos:
            self.errores.append(
                f"[Línea {linea}] Error semántico: "
                f"'{nombre}' ya fue declarado como '{self.tabla_simbolos[nombre]}'."
            )
            return

        # Determinar tipo declarado y validar expresión
        if ctx.ONTIE():
            tipo_decl = 'ontie'
            if self._tipo_expr_entera(ctx.expr_entera()) is None:
                return   # error ya registrado en _tipo_expr_entera

        elif ctx.FLOTE():
            tipo_decl = 'flote'
            if self._tipo_expr_decimal(ctx.expr_decimal()) is None:
                return

        else:  # DUBLE
            tipo_decl = 'duble'
            if self._tipo_expr_decimal(ctx.expr_decimal()) is None:
                return

        # Si llegó aquí, la declaración es válida → registrar en tabla
        self.tabla_simbolos[nombre] = tipo_decl

    # Los demás enterX son vacíos; el walker los necesita definidos
    def enterEveryRule(self, ctx): pass
    def exitEveryRule(self, ctx):  pass
    def visitTerminal(self, node): pass
    def visitErrorNode(self, node): pass


# ─────────────────────────────────────────────
#  TOKENIZADOR RECURSIVO
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    os.makedirs("reportes_html", exist_ok=True)

    # ── Fase 1: léxica (recolectar tokens y errores léxicos) ──
    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)

    tokens_lista    = []
    errores_lexicos = []

    primer_token = lexer.nextToken()
    procesar_tokens_recursivo(lexer, primer_token, tokens_lista, errores_lexicos)

    # ── Fase 2: sintáctica ──
    input_stream2 = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer2 = LenguajeLexer(input_stream2)
    stream = CommonTokenStream(lexer2)
    parser = LenguajeParser(stream)

    listener_error = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener_error)

    tree = parser.programa()

    # ── Reporte de error léxico ──
    if errores_lexicos:
        print("Error léxico detectado\n")

        for e in errores_lexicos:
            if e["sugerencia"]:
                print(f"Línea {e['linea']}: '{e['lexema']}' → ¿Quiso decir '{e['sugerencia']}'?")
            else:
                print(f"Línea {e['linea']}: símbolo no reconocido '{e['lexema']}'")

        return

    # ── Reporte de error sintáctico ──
    if listener_error.hay_error:
        print("Error sintáctico detectado")
        return

    # ── Fase 3: semántica ──
    semantico = AnalizadorSemantico()
    walker = ParseTreeWalker()
    walker.walk(semantico, tree)

    if semantico.errores:
        print("Error semántico detectado\n")
        for err in semantico.errores:
            print(f"  {err}")
        return

    # ── Sin errores: generar reporte HTML ──
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