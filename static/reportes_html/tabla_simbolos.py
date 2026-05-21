import sys
import os

ruta_raiz = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)

sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer  import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr4 import ParseTreeVisitor


# 
# ERROR LISTENER
# 

class MiErrorListener(ErrorListener):

    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


# 
# TABLA DE SIMBOLOS VISITOR
# 

class TablaSimbolosVisitor(ParseTreeVisitor):

    def __init__(self):
        self.scopes   = [{}]
        self.historial = []
        self.errores   = []
        self.contexto  = ['global']

    #  helpers ─

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

    def declarar_variable(self, nombre, tipo, linea, col, valor='-'):
        scope = self.scope_actual()
        if nombre in scope:
            self.errores.append({
                'linea': linea, 'columna': col,
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

    def registrar_evento(self, nombre, evento, linea, col, valor='-'):
        simbolo = self.buscar_variable(nombre)
        if simbolo is None:
            self.historial.append({
                'nombre': nombre, 'tipo': '?',
                'scope': self.scope_legible(),
                'nivel': self.nivel_scope(),
                'evento': evento, 'valor': valor,
                'inicializado': False,
                'veces_asignada': 0, 'veces_usada': 0,
                'linea': linea, 'columna': col
            })
            return
        self.historial.append({
            'nombre': nombre,
            'tipo': simbolo['tipo'],
            'scope': simbolo['scope'],
            'nivel': simbolo['nivel'],
            'evento': evento, 'valor': valor,
            'inicializado': simbolo['inicializado'],
            'veces_asignada': simbolo['veces_asignada'],
            'veces_usada': simbolo['veces_usada'],
            'linea': linea, 'columna': col
        })

    #  visitors 

    def visitPrograma(self, ctx):
        return self.visitChildren(ctx)

    def visitBloque(self, ctx):
        self.entrar_scope('bloque')
        self.visitChildren(ctx)
        self.salir_scope()
        return None

    def visitFuncion_def(self, ctx):
        nombre = ctx.ID().getText()
        self.entrar_scope(f'funcion:{nombre}')
        if ctx.parametros():
            for p in ctx.parametros().parametro():
                pnombre = p.ID().getText()
                linea   = p.ID().getSymbol().line
                col     = p.ID().getSymbol().column
                if   p.ONTIE(): tipo = 'ontie'
                elif p.FLOTE(): tipo = 'flote'
                elif p.DUBLE(): tipo = 'duble'
                else:           tipo = 'shen'
                self.declarar_variable(pnombre, tipo, linea, col, 'parametro')
        self.visit(ctx.bloque())
        self.salir_scope()
        return None

    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column
        if   ctx.ONTIE(): tipo = 'ontie'
        elif ctx.FLOTE(): tipo = 'flote'
        elif ctx.DUBLE(): tipo = 'duble'
        else:             tipo = 'shen'
        valor = '-'
        if   ctx.expr_entera():  valor = ctx.expr_entera().getText()
        elif ctx.expr_decimal(): valor = ctx.expr_decimal().getText()
        elif ctx.expr_string():  valor = ctx.expr_string().getText()
        self.declarar_variable(nombre, tipo, linea, col, valor)
        return self.visitChildren(ctx)

    def visitPur_init(self, ctx):
        if not ctx.ID():
            return self.visitChildren(ctx)
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column
        if ctx.ONTIE() or ctx.FLOTE() or ctx.DUBLE() or ctx.SHEN():
            if   ctx.ONTIE(): tipo = 'ontie'
            elif ctx.FLOTE(): tipo = 'flote'
            elif ctx.DUBLE(): tipo = 'duble'
            else:             tipo = 'shen'
            valor = ctx.expr().getText() if ctx.expr() else '-'
            self.declarar_variable(nombre, tipo, linea, col, valor)
        else:
            sim = self.buscar_variable(nombre)
            if sim:
                sim['veces_asignada'] += 1
            self.registrar_evento(nombre, 'asignacion', linea, col)
        return self.visitChildren(ctx)

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column
        sim    = self.buscar_variable(nombre)
        if sim:
            sim['veces_asignada'] += 1
        self.registrar_evento(nombre, 'asignacion', linea, col,
                              ctx.expr().getText())
        return self.visitChildren(ctx)

    def visitExpr(self, ctx):
        if ctx.ID():
            nombre = ctx.ID().getText()
            sim    = self.buscar_variable(nombre)
            if sim:
                sim['veces_usada'] += 1
                linea = ctx.ID().getSymbol().line
                col   = ctx.ID().getSymbol().column
                self.registrar_evento(nombre, 'uso', linea, col)
        return self.visitChildren(ctx)

    def visitExpr_entera(self, ctx):
        return self.visitExpr(ctx)

    def visitExpr_decimal(self, ctx):
        return self.visitExpr(ctx)

    def visitExpr_string(self, ctx):
        return self.visitExpr(ctx)


# 
# GENERACION DE FILAS HTML
# 

EVENTO_COLOR = {
    'declaracion': '#22f08a',
    'asignacion':  '#4f8ef7',
    'uso':         '#00d4ff',
}

TIPO_COLOR = {
    'ontie': '#f5a623',
    'flote': '#a855f7',
    'duble': '#a855f7',
    'shen':  '#00d4ff',
    '?':     '#ff4d6a',
}


def construir_filas(historial):
    if not historial:
        return '<tr><td colspan="10" class="empty">Sin simbolos generados</td></tr>'

    filas = ''
    for i, h in enumerate(historial):
        bg         = '#0d1225' if i % 2 == 0 else '#090d1a'
        ec         = EVENTO_COLOR.get(h['evento'], '#c8d8f8')
        tc         = TIPO_COLOR.get(h['tipo'],   '#c8d8f8')
        init_color = '#22f08a' if h['inicializado'] else '#ff4d6a'
        init_txt   = 'Si' if h['inicializado'] else 'No'

        filas += (
            f'<tr style="background:{bg}">'
            f'<td style="color:#c8d8f8;font-weight:600">{h["nombre"]}</td>'
            f'<td style="color:{tc}">{h["tipo"]}</td>'
            f'<td style="color:#7a9cc8">{h["scope"]}</td>'
            f'<td style="color:{ec}">{h["evento"]}</td>'
            f'<td style="color:#c8d8f8">{h.get("valor", "-")}</td>'
            f'<td style="color:{init_color}">{init_txt}</td>'
            f'<td style="color:#4f8ef7">{h["veces_asignada"]}</td>'
            f'<td style="color:#00d4ff">{h["veces_usada"]}</td>'
            f'<td style="color:#7a9cc8">{h["linea"]}</td>'
            f'<td style="color:#7a9cc8">{h["columna"]}</td>'
            f'</tr>\n'
        )
    return filas


# 
# MAIN — CORREGIDO: ahora genera el HTML
# 


def main(ruta_fuente="programa.leng"):
    global ruta_raiz
    ruta_reportes = os.path.join(ruta_raiz, 'reportes_html')
    os.makedirs(ruta_reportes, exist_ok=True)

    input_stream = FileStream(os.path.join(ruta_raiz, ruta_fuente), encoding='utf-8')
    lexer = LenguajeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LenguajeParser(stream)
    listener = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    tree = parser.programa()

    if listener.hay_error:
        print("No se generó tabla de símbolos (error sintáctico)")
        return

    visitor = TablaSimbolosVisitor()
    visitor.visit(tree)

    # Leer template (mejor usar marcador {{FILAS}})
    ruta_template = os.path.join(ruta_reportes, 'tabla_simbolos_base.html')
    if not os.path.exists(ruta_template):
        ruta_template = os.path.join(ruta_reportes, 'tabla_simbolos.html')
    with open(ruta_template, 'r', encoding='utf-8') as f:
        html = f.read()

    filas = construir_filas(visitor.historial)
    html = html.replace('{{FILAS}}', filas)   # Cambia el marcador en tu HTML

    total = len(visitor.historial)
    badge = f'{total} evento{"s" if total != 1 else ""}'
    html = html.replace('{{BADGE}}', badge)

    with open(os.path.join(ruta_reportes, 'tabla_simbolos.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"{total} evento(s) registrado(s)")

if __name__ == '__main__':
    import sys
    fuente = sys.argv[1] if len(sys.argv) > 1 else "programa.leng"
    main(fuente)