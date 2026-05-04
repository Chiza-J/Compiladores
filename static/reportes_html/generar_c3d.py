import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr_todo.AnalizadorSemantico import AnalizadorSemantico
from antlr_todo.C3D_generador import C3DGenerador


# ── mapeo operadores del lenguaje → C++ ─────────────────────
OP_CPP = {
    'plu':    '+',
    'moan':   '-',
    'par':    '*',
    'bag':    '/',
    'minog':  '<',
    'aye':    '>',
    'compag': '==',
}

# ── tipos del lenguaje → C++ ─────────────────────────────────
TIPO_CPP = {
    'ontie': 'int',
    'flote': 'float',
    'duble': 'double',
    'shen':  'const char*',        # NUEVO
}


# ── listener silencioso ──────────────────────────────────────
class ErrorSilencioso(ErrorListener):
    def __init__(self):
        self.hay_error = False
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


# ── detecta el "tipo" de instrucción para la tercera columna ─
def tipo_instruccion(linea):
    l = linea.strip()
    if not l:
        return ''
    if l.endswith(':'):
        return 'etiqueta'
    if l.startswith('if '):
        return 'condicional'
    if l.startswith('goto '):
        return 'salto'
    if l.startswith('print '):
        return 'impresión'
    if l.startswith('return'):
        return 'retorno'
    if '=' in l:
        dest = l.split('=')[0].strip()
        if dest.startswith('t') and dest[1:].isdigit():
            return 'temporal'
        return 'asignación'
    return ''


# ── color por tipo de instrucción ────────────────────────────
COLORES = {
    'etiqueta':   '#a855f7',
    'condicional':'#f5a623',
    'salto':      '#f5a623',
    'impresión':  '#00d4ff',
    'retorno':    '#ff4d6a',
    'temporal':   '#4f8ef7',
    'asignación': '#22f08a',
}


# ── traducir expr reemplazando operadores ────────────────────
def traducir_expr(expr):
    for op_l, op_c in OP_CPP.items():
        expr = expr.replace(op_l, op_c)
    return expr


# ── detecta si un valor es un literal string ─────────────────
def es_string_val(val):
    return val.strip().startswith('"')


# ── traducir una línea C3D a C++ ─────────────────────────────
def c3d_a_cpp(linea, tabla=None):
    if tabla is None:
        tabla = {}

    l = linea.strip()
    if not l:
        return ''

    # Etiqueta
    if l.endswith(':') and ' ' not in l:
        return f'    {l}'

    # print — mismo keyword para números y strings
    if l.startswith('print '):
        val = traducir_expr(l[6:].strip())
        if es_string_val(val):                          # literal "..."
            return f'    printf("%s\\n", {val});'
        if val in tabla and tabla[val] == 'shen':       # variable shen
            return f'    printf("%s\\n", {val});'
        return f'    printf("%g\\n", (double)({val}));' # número / temporal

    if l.startswith('return'):
        resto = l[6:].strip()
        return f'    return (int)({traducir_expr(resto)});' if resto else '    return 0;'

    if l.startswith('if '):
        idx = l.rfind(' goto ')
        cond  = traducir_expr(l[3:idx].strip())
        label = l.split()[-1]
        return f'    if ({cond}) goto {label};'

    if l.startswith('goto '):
        return f'    goto {l.split()[1]};'

    if '=' in l:
        dest, resto = l.split('=', 1)
        return f'    {dest.strip()} = {traducir_expr(resto.strip())};'

    return f'    // {l}'


# ── generar el .cpp completo ─────────────────────────────────
def generar_cpp(codigo_c3d, tabla):
    cpp = [
        '#include <stdio.h>',
        '#include <string.h>',    # NUEVO para strings
        '',
        'int main() {'
    ]

    # Declaraciones de variables del usuario
    for nombre, tipo in tabla.items():
        if tipo == 'shen':
            cpp.append(f'    const char* {nombre} = "";')   # NUEVO
        else:
            cpp.append(f'    {TIPO_CPP.get(tipo, "double")} {nombre} = 0;')

    # Temporales numéricos inferidos del C3D
    temps = sorted(
        {l.split('=')[0].strip() for l in codigo_c3d
         if '=' in l and not l.strip().endswith(':')
         and l.split('=')[0].strip().startswith('t')
         and l.split('=')[0].strip()[1:].isdigit()},
        key=lambda x: int(x[1:])
    )
    for t in temps:
        cpp.append(f'    double {t};')

    if tabla or temps:
        cpp.append('')

    # Cuerpo — pasamos tabla para que print distinga shen
    for linea in codigo_c3d:
        cpp.append(c3d_a_cpp(linea, tabla))

    cpp += ['', '    return 0;', '}']
    return '\n'.join(cpp)


# ── MAIN ─────────────────────────────────────────────────────
def main():
    ruta_reportes = os.path.join(ruta_raiz, 'reportes_html')
    ruta_base     = os.path.join(ruta_reportes, 'c3d_base.html')
    ruta_salida   = os.path.join(ruta_reportes, 'reporte_c3d.html')

    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    archivo = os.path.join(ruta_raiz, 'programa.leng')

    stream = FileStream(archivo, encoding='utf-8')
    lexer  = LenguajeLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = LenguajeParser(tokens)

    err = ErrorSilencioso()
    parser.removeErrorListeners()
    parser.addErrorListener(err)
    tree = parser.programa()

    if err.hay_error:
        print("No se puede generar C3D (errores sintácticos)")
        return

    semantico = AnalizadorSemantico()
    semantico.visit(tree)

    if semantico.errores:
        print("No se puede generar C3D (errores semánticos)")
        return

    generador = C3DGenerador(semantico.tabla_simbolos)
    generador.visit(tree)

    codigo_c3d = generador.codigo

    with open(os.path.join(ruta_reportes, 'salida.c3d'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(codigo_c3d))

    cpp_texto = generar_cpp(codigo_c3d, semantico.tabla_simbolos)
    with open(os.path.join(ruta_reportes, 'salida.cpp'), 'w', encoding='utf-8') as f:
        f.write(cpp_texto)

    if not os.path.exists(ruta_base):
        print("ERROR: No existe c3d_base.html")
        return

    with open(ruta_base, 'r', encoding='utf-8') as f:
        html = f.read()

    filas = ''
    for i, linea in enumerate(codigo_c3d):
        if not linea.strip():
            continue
        tipo  = tipo_instruccion(linea)
        color = COLORES.get(tipo, '#c8d8f8')
        bg    = '#0d1225' if i % 2 == 0 else '#090d1a'
        badge_color = {
            'etiqueta':   '#a855f7',
            'condicional':'#f5a623',
            'salto':      '#f5a623',
            'impresión':  '#00d4ff',
            'retorno':    '#ff4d6a',
            'temporal':   '#4f8ef7',
            'asignación': '#22f08a',
        }.get(tipo, '#3a4a6a')

        filas += f"""
        <tr style="background:{bg}">
            <td>{i + 1}</td>
            <td style="color:{color};font-weight:500">{linea}</td>
            <td><span style="color:{badge_color};font-size:10px;letter-spacing:.06em">{tipo}</span></td>
        </tr>"""

    html = html.replace(
        '<tbody id="tbody">',
        f'<tbody id="tbody">{filas}'
    )

    cpp_escaped = cpp_texto.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    html = html.replace(
        '— analiza primero tu código —',
        cpp_escaped
    )

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)

    total = len([l for l in codigo_c3d if l.strip()])
    print(f"{total} instrucciones C3D generadas - salida.cpp lista")


if __name__ == '__main__':
    main()