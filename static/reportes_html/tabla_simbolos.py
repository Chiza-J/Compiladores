import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr4 import ParseTreeVisitor


class MiErrorListener(ErrorListener):
    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


# 🔹 VISITOR PARA TABLA DE SÍMBOLOS
class TablaSimbolosVisitor(ParseTreeVisitor):
    def __init__(self):
        self.tabla_simbolos = {}
        self.errores = []
        self.scope = "global"

    # 🔹 DECLARACIÓN
    def visitDeclaracion(self, ctx: LenguajeParser.DeclaracionContext):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column

        if ctx.ONTIE():
            tipo = 'int'
        elif ctx.FLOTE():
            tipo = 'float'
        else:
            tipo = 'double'

        valor = None
        if ctx.expr_entera():
            valor = ctx.expr_entera().getText()
        elif ctx.expr_decimal():
            valor = ctx.expr_decimal().getText()

        if nombre in self.tabla_simbolos:
            self.errores.append({
                "linea": linea,
                "columna": col,
                "mensaje": f"Variable '{nombre}' ya fue declarada",
                "tipo": "Semántico"
            })
        else:
            self.tabla_simbolos[nombre] = {
                "tipo": tipo,
                "categoria": "Variable",
                "ambito": self.scope,
                "valor": valor,
                "linea": linea,
                "columna": col,
                "usos": []
            }

        return self.visitChildren(ctx)

    # 🔹 ASIGNACIÓN (uso)
    def visitAsignacion(self, ctx: LenguajeParser.AsignacionContext):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column

        if nombre not in self.tabla_simbolos:
            self.errores.append({
                "linea": linea,
                "columna": col,
                "mensaje": f"Variable '{nombre}' no declarada",
                "tipo": "Semántico"
            })
        else:
            self.tabla_simbolos[nombre]["usos"].append({
                "linea": linea,
                "columna": col
            })

        return self.visitChildren(ctx)

    # 🔹 USO EN EXPRESIONES 
    def visitExpr(self, ctx: LenguajeParser.ExprContext):
        if ctx.ID():
            nombre = ctx.ID().getText()
            linea  = ctx.ID().getSymbol().line
            col    = ctx.ID().getSymbol().column

            if nombre in self.tabla_simbolos:
                self.tabla_simbolos[nombre]["usos"].append({
                    "linea": linea,
                    "columna": col
                })
            else:
                self.errores.append({
                    "linea": linea,
                    "columna": col,
                    "mensaje": f"Variable '{nombre}' no declarada",
                    "tipo": "Semántico"
                })

        return self.visitChildren(ctx)


def main():
    os.makedirs(os.path.join(ruta_raiz, "reportes_html"), exist_ok=True)

    ruta_salida = os.path.join(ruta_raiz, "reportes_html", "tabla_simbolos.html")

    # BORRAR HTML ANTERIOR
    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    # LECTURA ARCHIVO
    input_stream = FileStream(os.path.join(ruta_raiz, "programa.leng"))
    lexer = LenguajeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LenguajeParser(stream)

    listener_error = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener_error)

    tree = parser.programa()

    # VALIDAR ERRORES SINTÁCTICOS
    if listener_error.hay_error:
        print("No se generó tabla de símbolos (error sintáctico)")
        return

    # 🔹 VISITAR ÁRBOL
    visitor = TablaSimbolosVisitor()
    visitor.visit(tree)

    # SI HAY ERRORES SEMÁNTICOS
    if visitor.errores:
        print("Errores semánticos encontrados")
        for e in visitor.errores:
            print(f"Línea {e['linea']}, Col {e['columna']}: {e['mensaje']}")
        return

    # GENERAR HTML
    ruta_base = os.path.join(ruta_raiz, "reportes_html", "tabla_simbolos_base.html")

    if not os.path.exists(ruta_base):
        print("ERROR: No existe tabla_simbolos_base.html")
        return

    with open(ruta_base, "r", encoding="utf-8") as f:
        html = f.read()

    filas = ""

    for nombre, datos in visitor.tabla_simbolos.items():
        usos = ", ".join([f"(L{u['linea']},C{u['columna']})" for u in datos['usos']])
        filas += f"""
        <tr>
            <td>{nombre}</td>
            <td>{datos['tipo']}</td>
            <td>{datos['categoria']}</td>
            <td>{datos['ambito']}</td>
            <td>{datos['valor']}</td>
            <td>{datos['linea']}</td>
            <td>{datos['columna']}</td>
            <td>{usos}</td>
        </tr>
        """

    html = html.replace(
        '<tbody id="tbody">',
        f'<tbody id="tbody">{filas}'
    )

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html)

    # MENSAJE FINAL
    cantidad = len(visitor.tabla_simbolos)

    if cantidad == 0:
        print("Sin símbolos")
    elif cantidad == 1:
        print("1 símbolo registrado")
    else:
        print(f"{cantidad} símbolos registrados")


if __name__ == "__main__":
    main()