import sys
import os

ruta_raiz = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)

sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr4 import ParseTreeVisitor


# =========================================================
# ERROR LISTENER
# =========================================================

class MiErrorListener(ErrorListener):

    def __init__(self):
        self.hay_error = False

    def syntaxError(
        self,
        recognizer,
        offendingSymbol,
        line,
        column,
        msg,
        e
    ):
        self.hay_error = True


# =========================================================
# TABLA DE SIMBOLOS VISITOR
# =========================================================

class TablaSimbolosVisitor(ParseTreeVisitor):

    def __init__(self):

        # scopes apilados
        self.scopes = [{}]

        self.historial = []

        self.errores = []

        self.contexto = ['global']

    # HELPERS

    def scope_actual(self):
        return self.scopes[-1]

    def entrar_scope(self, nombre='local'):
        self.scopes.append({})
        self.contexto.append(nombre)

    def salir_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

        if len(self.contexto) > 1:
            self.contexto.pop()

    def nivel_scope(self):
        return len(self.scopes) - 1

    def scope_legible(self):

        if self.nivel_scope() == 0:
            return 'global'

        return self.contexto[-1]

    def buscar_variable(self, nombre):

        for scope in reversed(self.scopes):

            if nombre in scope:
                return scope[nombre]

        return None

    def declarar_variable(
        self,
        nombre,
        tipo,
        linea,
        col,
        valor='-'
    ):

        scope = self.scope_actual()

        # SOLO valida redeclaracion en el MISMO scope
        if nombre in scope:

            self.errores.append({
                'linea': linea,
                'columna': col,
                'mensaje': f"Variable '{nombre}' ya fue declarada",
                'tipo': 'Semantico'
            })

            return

        scope[nombre] = {
            'tipo': tipo,
            'scope': self.scope_legible(),
            'nivel': self.nivel_scope(),
            'inicializado': True,
            'valor_inicial': valor,
            'veces_asignada': 1,
            'veces_usada': 0,
            'linea_decl': linea
        }

        self.historial.append({
            'nombre': nombre,
            'tipo': tipo,
            'scope': self.scope_legible(),
            'nivel': self.nivel_scope(),
            'evento': 'declaracion',
            'valor': valor,
            'inicializado': True,
            'veces_asignada': 1,
            'veces_usada': 0,
            'linea': linea,
            'columna': col
        })

    def registrar_evento(
        self,
        nombre,
        evento,
        linea,
        col,
        valor='-'
    ):

        simbolo = self.buscar_variable(nombre)

        if simbolo is None:

            self.historial.append({
                'nombre': nombre,
                'tipo': '?',
                'scope': self.scope_legible(),
                'nivel': self.nivel_scope(),
                'evento': evento,
                'valor': valor,
                'inicializado': False,
                'veces_asignada': 0,
                'veces_usada': 0,
                'linea': linea,
                'columna': col
            })

            return

        self.historial.append({
            'nombre': nombre,
            'tipo': simbolo['tipo'],
            'scope': simbolo['scope'],
            'nivel': simbolo['nivel'],
            'evento': evento,
            'valor': valor,
            'inicializado': simbolo['inicializado'],
            'veces_asignada': simbolo['veces_asignada'],
            'veces_usada': simbolo['veces_usada'],
            'linea': linea,
            'columna': col
        })

    # PROGRAMA

    def visitPrograma(self, ctx):
        return self.visitChildren(ctx)

    # BLOQUES

    def visitBloque(self, ctx):

        self.entrar_scope('bloque')

        self.visitChildren(ctx)

        self.salir_scope()

        return None

    # FUNCIONES

    def visitFuncion_def(self, ctx):

        nombre = ctx.ID().getText()

        self.entrar_scope(f'funcion:{nombre}')

        # parametros
        if ctx.parametros():

            for p in ctx.parametros().parametro():

                param_nombre = p.ID().getText()

                linea = p.ID().getSymbol().line
                col = p.ID().getSymbol().column

                if p.ONTIE():
                    tipo = 'ontie'
                elif p.FLOTE():
                    tipo = 'flote'
                elif p.DUBLE():
                    tipo = 'duble'
                else:
                    tipo = 'shen'

                self.declarar_variable(
                    param_nombre,
                    tipo,
                    linea,
                    col,
                    'parametro'
                )

        self.visit(ctx.bloque())

        self.salir_scope()

        return None

    # DECLARACION

    def visitDeclaracion(self, ctx):

        nombre = ctx.ID().getText()

        linea = ctx.ID().getSymbol().line
        col = ctx.ID().getSymbol().column

        if ctx.ONTIE():
            tipo = 'ontie'

        elif ctx.FLOTE():
            tipo = 'flote'

        elif ctx.DUBLE():
            tipo = 'duble'

        else:
            tipo = 'shen'

        valor = '-'

        if ctx.expr_entera():
            valor = ctx.expr_entera().getText()

        elif ctx.expr_decimal():
            valor = ctx.expr_decimal().getText()

        elif ctx.expr_string():
            valor = ctx.expr_string().getText()

        self.declarar_variable(
            nombre,
            tipo,
            linea,
            col,
            valor
        )

        return self.visitChildren(ctx)

    # FOR INIT

    def visitPur_init(self, ctx):

        if not ctx.ID():
            return self.visitChildren(ctx)

        nombre = ctx.ID().getText()

        linea = ctx.ID().getSymbol().line
        col = ctx.ID().getSymbol().column

        # DECLARACION
        if (
            ctx.ONTIE()
            or ctx.FLOTE()
            or ctx.DUBLE()
            or ctx.SHEN()
        ):

            if ctx.ONTIE():
                tipo = 'ontie'

            elif ctx.FLOTE():
                tipo = 'flote'

            elif ctx.DUBLE():
                tipo = 'duble'

            else:
                tipo = 'shen'

            valor = '-'

            if ctx.expr():
                valor = ctx.expr().getText()

            self.declarar_variable(
                nombre,
                tipo,
                linea,
                col,
                valor
            )

        else:

            simbolo = self.buscar_variable(nombre)

            if simbolo:

                simbolo['veces_asignada'] += 1

            self.registrar_evento(
                nombre,
                'asignacion',
                linea,
                col
            )

        return self.visitChildren(ctx)

    # ASIGNACION

    def visitAsignacion(self, ctx):

        nombre = ctx.ID().getText()

        linea = ctx.ID().getSymbol().line
        col = ctx.ID().getSymbol().column

        simbolo = self.buscar_variable(nombre)

        if simbolo:

            simbolo['veces_asignada'] += 1

        self.registrar_evento(
            nombre,
            'asignacion',
            linea,
            col,
            ctx.expr().getText()
        )

        return self.visitChildren(ctx)

    # USO VARIABLES

    def visitExpr(self, ctx):

        if ctx.ID():

            nombre = ctx.ID().getText()

            simbolo = self.buscar_variable(nombre)

            if simbolo:

                simbolo['veces_usada'] += 1

                linea = ctx.ID().getSymbol().line
                col = ctx.ID().getSymbol().column

                self.registrar_evento(
                    nombre,
                    'uso',
                    linea,
                    col
                )

        return self.visitChildren(ctx)

    def visitExpr_entera(self, ctx):
        return self.visitExpr(ctx)

    def visitExpr_decimal(self, ctx):
        return self.visitExpr(ctx)

    def visitExpr_string(self, ctx):
        return self.visitExpr(ctx)


# =========================================================
# MAIN
# =========================================================

def main():

    os.makedirs(
        os.path.join(ruta_raiz, 'reportes_html'),
        exist_ok=True
    )

    input_stream = FileStream(
        os.path.join(ruta_raiz, 'programa.leng'),
        encoding='utf-8'
    )

    lexer = LenguajeLexer(input_stream)

    stream = CommonTokenStream(lexer)

    parser = LenguajeParser(stream)

    listener = MiErrorListener()

    parser.removeErrorListeners()

    parser.addErrorListener(listener)

    tree = parser.programa()

    if listener.hay_error:

        print("No se genero tabla de simbolos (error sintactico)")

        return

    visitor = TablaSimbolosVisitor()

    visitor.visit(tree)

    # SI HAY ERRORES

    if visitor.errores:

        print("Errores semanticos encontrados")

        for e in visitor.errores:

            print(
                f"Linea {e['linea']}, "
                f"Col {e['columna']}: "
                f"{e['mensaje']}"
            )

        return

    # SIN ERRORES

    print(
        f"{len(visitor.historial)} "
        f"evento(s) registrado(s)"
    )


if __name__ == '__main__':
    main()