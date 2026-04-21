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


# ─────────────────────────────────────────────────────────────
#  Visitor completo de tabla de símbolos
#
#  Registra por cada evento:
#    nombre, tipo, scope, evento, valor_inicial,
#    inicializado, veces_asignada, veces_usada, linea, columna
# ─────────────────────────────────────────────────────────────
class TablaSimbolosVisitor(ParseTreeVisitor):

    def __init__(self):
        # variables declaradas: nombre -> dict con toda la info
        self.tabla = {}

        # historial de eventos en orden de aparición
        self.historial = []

        # pila de scopes: 'global' es el nivel 0
        # cada bloque anidado agrega un nivel
        self._scope_stack = ['global']

        # contexto actual para saber si estamos dentro de if/while
        self._contexto = []

        self.errores = []

    # ── helpers ──────────────────────────────────────────────

    def _scope_actual(self):
        return ' > '.join(self._scope_stack)

    def _nivel_scope(self):
        # 0 = global, 1+ = local/bloque
        return len(self._scope_stack) - 1

    def _scope_legible(self):
        nivel = self._nivel_scope()
        if nivel == 0:
            return 'global'
        ctx = self._contexto[-1] if self._contexto else 'bloque'
        return f'local ({ctx})'

    def _agregar_evento(self, nombre, evento, linea, col, valor=None):
        info = self.tabla.get(nombre, {})
        self.historial.append({
            'nombre':        nombre,
            'tipo':          info.get('tipo', '?'),
            'scope':         info.get('scope', self._scope_legible()),
            'nivel':         info.get('nivel', self._nivel_scope()),
            'evento':        evento,
            'valor':         valor if valor is not None else '—',
            'inicializado':  info.get('inicializado', False),
            'veces_asignada':info.get('veces_asignada', 0),
            'veces_usada':   info.get('veces_usada', 0),
            'linea':         linea,
            'columna':       col,
        })

    # ── programa (nivel raíz) ─────────────────────────────────
    def visitPrograma(self, ctx):
        return self.visitChildren(ctx)

    # ── bloque: empuja y saca scope ───────────────────────────
    def visitBloque(self, ctx):
        ctx_nombre = self._contexto[-1] if self._contexto else 'bloque'
        self._scope_stack.append(ctx_nombre)
        self.visitChildren(ctx)
        self._scope_stack.pop()
        return None

    # ── declaración: ontie/flote/duble x iyal expr ───────────
    def visitDeclaracion(self, ctx: LenguajeParser.DeclaracionContext):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column

        if ctx.ONTIE():
            tipo = 'ontie'
        elif ctx.FLOTE():
            tipo = 'flote'
        else:
            tipo = 'duble'

        # extraer valor inicial como texto
        if ctx.expr_entera():
            valor_txt = ctx.expr_entera().getText()
        else:
            valor_txt = ctx.expr_decimal().getText()

        if nombre in self.tabla:
            self.errores.append({
                'linea': linea, 'columna': col,
                'mensaje': f"Variable '{nombre}' ya fue declarada",
                'tipo': 'Semantico'
            })
            return self.visitChildren(ctx)

        scope   = self._scope_legible()
        nivel   = self._nivel_scope()

        self.tabla[nombre] = {
            'tipo':           tipo,
            'scope':          scope,
            'nivel':          nivel,
            'inicializado':   True,
            'valor_inicial':  valor_txt,
            'veces_asignada': 1,
            'veces_usada':    0,
            'linea_decl':     linea,
        }

        self._agregar_evento(nombre, 'declaracion', linea, col, valor=valor_txt)

        # visitar la expresión para registrar usos dentro del valor inicial
        return self.visitChildren(ctx)

    # ── asignación: x iyal expr ───────────────────────────────
    def visitAsignacion(self, ctx: LenguajeParser.AsignacionContext):
        nombre = ctx.ID().getText()
        linea  = ctx.ID().getSymbol().line
        col    = ctx.ID().getSymbol().column

        valor_txt = ctx.expr().getText()

        if nombre in self.tabla:
            self.tabla[nombre]['veces_asignada'] += 1
            self._agregar_evento(nombre, 'asignacion', linea, col, valor=valor_txt)
        else:
            # variable no declarada — el semántico ya lo reporta
            self._agregar_evento(nombre, 'asignacion (no declarada)', linea, col, valor=valor_txt)

        return self.visitChildren(ctx)

    # ── condición if ─────────────────────────────────────────
    def visitCondicion_if(self, ctx: LenguajeParser.Condicion_ifContext):
        self._contexto.append('if')
        self.visitChildren(ctx)
        self._contexto.pop()
        return None

    # ── ciclo while ──────────────────────────────────────────
    def visitCiclo_while(self, ctx: LenguajeParser.Ciclo_whileContext):
        self._contexto.append('while')
        self.visitChildren(ctx)
        self._contexto.pop()
        return None

    # ── impresión: amprimi(expr) ──────────────────────────────
    def visitImpresion(self, ctx: LenguajeParser.ImpresionContext):
        return self.visitChildren(ctx)

    # ── retorno ───────────────────────────────────────────────
    def visitRetorno(self, ctx: LenguajeParser.RetornoContext):
        return self.visitChildren(ctx)

    # ── uso en expr general ───────────────────────────────────
    def visitExpr(self, ctx: LenguajeParser.ExprContext):
        if ctx.ID():
            nombre = ctx.ID().getText()
            linea  = ctx.ID().getSymbol().line
            col    = ctx.ID().getSymbol().column
            if nombre in self.tabla:
                self.tabla[nombre]['veces_usada'] += 1
                self._agregar_evento(nombre, 'uso', linea, col)
        return self.visitChildren(ctx)

    # ── uso en expr_entera ────────────────────────────────────
    def visitExpr_entera(self, ctx: LenguajeParser.Expr_enteraContext):
        if ctx.ID():
            nombre = ctx.ID().getText()
            linea  = ctx.ID().getSymbol().line
            col    = ctx.ID().getSymbol().column
            if nombre in self.tabla:
                self.tabla[nombre]['veces_usada'] += 1
                self._agregar_evento(nombre, 'uso', linea, col)
        return self.visitChildren(ctx)

    # ── uso en expr_decimal ───────────────────────────────────
    def visitExpr_decimal(self, ctx: LenguajeParser.Expr_decimalContext):
        if ctx.ID():
            nombre = ctx.ID().getText()
            linea  = ctx.ID().getSymbol().line
            col    = ctx.ID().getSymbol().column
            if nombre in self.tabla:
                self.tabla[nombre]['veces_usada'] += 1
                self._agregar_evento(nombre, 'uso', linea, col)
        return self.visitChildren(ctx)


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────
def main():
    os.makedirs(os.path.join(ruta_raiz, 'reportes_html'), exist_ok=True)

    ruta_salida = os.path.join(ruta_raiz, 'reportes_html', 'tabla_simbolos.html')
    ruta_base   = os.path.join(ruta_raiz, 'reportes_html', 'tabla_simbolos_base.html')

    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    input_stream = FileStream(os.path.join(ruta_raiz, 'programa.leng'))
    lexer  = LenguajeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LenguajeParser(stream)

    listener_error = MiErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(listener_error)
    tree = parser.programa()

    if listener_error.hay_error:
        print("No se genero tabla de simbolos (error sintactico)")
        return

    visitor = TablaSimbolosVisitor()
    visitor.visit(tree)

    if visitor.errores:
        print("Errores semanticos encontrados")
        for e in visitor.errores:
            print(f"Linea {e['linea']}, Col {e['columna']}: {e['mensaje']}")
        return

    if not os.path.exists(ruta_base):
        print("ERROR: No existe tabla_simbolos_base.html")
        return

    with open(ruta_base, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── colores y estilos por evento ──────────────────────────
    EVENTO_STYLE = {
        'declaracion':            ('#22f08a', '▶'),
        'asignacion':             ('#00d4ff', '✎'),
        'uso':                    ('#f5a623', '◈'),
        'asignacion (no declarada)': ('#ff4d6a', '⚠'),
    }

    SCOPE_COLOR = {
        'global': '#a855f7',
    }

    TIPO_COLOR = {
        'ontie': '#4f8ef7',
        'flote': '#00d4ff',
        'duble': '#22f08a',
    }

    filas = ''
    for i, h in enumerate(visitor.historial):
        color_ev, icono = EVENTO_STYLE.get(h['evento'], ('#c8d8f8', '·'))
        color_tipo  = TIPO_COLOR.get(h['tipo'], '#c8d8f8')
        color_scope = '#a855f7' if h['nivel'] == 0 else '#f5a623'
        bg = '#0d1225' if i % 2 == 0 else '#090d1a'

        # indicador de inicialización
        init_icon = '✓' if h['inicializado'] else '✗'
        init_color = '#22f08a' if h['inicializado'] else '#ff4d6a'

        filas += f"""
        <tr style="background:{bg}">
            <td style="color:#22f08a;font-weight:600">{h['nombre']}</td>
            <td><span style="color:{color_tipo};background:rgba(79,142,247,0.08);padding:1px 7px;border-radius:3px;font-size:11px">{h['tipo']}</span></td>
            <td><span style="color:{color_scope};font-size:10px;letter-spacing:.05em">{h['scope']}</span></td>
            <td><span style="color:{color_ev}">{icono}</span> <span style="color:{color_ev};font-size:10px;letter-spacing:.06em;text-transform:uppercase">{h['evento']}</span></td>
            <td style="color:#7a9cc8;font-size:11px;font-family:'JetBrains Mono',monospace">{h['valor']}</td>
            <td style="color:{init_color};text-align:center;font-size:12px">{init_icon}</td>
            <td style="color:#4a5a7a;font-size:11px;text-align:center">{h['veces_asignada']}</td>
            <td style="color:#4a5a7a;font-size:11px;text-align:center">{h['veces_usada']}</td>
            <td style="color:#7a9cc8;font-size:11px;text-align:center">{h['linea']}</td>
            <td style="color:#7a9cc8;font-size:11px;text-align:center">{h['columna']}</td>
        </tr>"""

    html = html.replace('<tbody id="tbody">', f'<tbody id="tbody">{filas}')

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)

    total_vars   = len(visitor.tabla)
    total_eventos = len(visitor.historial)

    if total_vars == 0:
        print("Sin simbolos")
    else:
        print(f"{total_vars} variable(s) - {total_eventos} evento(s) registrado(s)")


if __name__ == '__main__':
    main()