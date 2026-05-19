import sys
import os
import re

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer import LenguajeLexer
from antlr_todo.LenguajeParser import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr_todo.AnalizadorSemantico import AnalizadorSemantico
from antlr_todo.C3D_generador import C3DGenerador
from antlr_todo.C3d_optimizador import C3DOptimizador


OP_CPP = {
    'plu':    '+',
    'moan':   '-',
    'par':    '*',
    'bag':    '/',
    'minog':  '<',
    'aye':    '>',
    'compag': '==',
}

TIPO_CPP = {
    'ontie': 'int',
    'flote': 'float',
    'duble': 'double',
    'shen':  'const char*',
}


class ErrorSilencioso(ErrorListener):
    def __init__(self):
        self.hay_error = False
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


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
        return 'impresion'
    if l.startswith('read '):
        return 'entrada'
    if l.startswith('return'):
        return 'retorno'
    if l.startswith('param'):
        return 'parametro'
    if 'call ' in l:
        return 'llamada'
    if '=' in l:
        dest = l.split('=')[0].strip()
        if re.match(r'^t\d+$', dest):
            return 'temporal'
        return 'asignacion'
    return ''


COLORES = {
    'etiqueta':   '#a855f7',
    'condicional':'#f5a623',
    'salto':      '#f5a623',
    'impresion':  '#00d4ff',
    'entrada':    '#00d4ff',
    'retorno':    '#ff4d6a',
    'temporal':   '#4f8ef7',
    'asignacion': '#22f08a',
    'parametro':  '#a855f7',
    'llamada':    '#22f08a',
}


def traducir_expr(expr):
    for op_l, op_c in OP_CPP.items():
        expr = expr.replace(op_l, op_c)
    return expr


def es_string_val(val):
    return val.strip().startswith('"')


def c3d_a_cpp(linea, tabla=None):
    if tabla is None:
        tabla = {}
    l = linea.strip()
    if not l:
        return ''

    if l.endswith(':') and ' ' not in l:
        return f'    {l}'

    if l.startswith('print '):
        val = traducir_expr(l[6:].strip())
        if es_string_val(val):
            return f'    printf("%s\\n", {val});'
        if val in tabla and tabla[val] == 'shen':
            return f'    printf("%s\\n", {val});'
        return f'    printf("%g\\n", (double)({val}));'

    if l.startswith('read '):
        var  = l[5:].strip()
        tipo = tabla.get(var, 'ontie')
        fmt  = {'ontie': '%d', 'flote': '%f', 'duble': '%lf', 'shen': '%s'}.get(tipo, '%d')
        return f'    scanf("{fmt}", &{var});'

    if l.startswith('param ') and not l.startswith('param_get'):
        val = traducir_expr(l[6:].strip())
        return f'    // push {val}'

    if l.startswith('param_get '):
        return f'    // param_get {l[10:].strip()}'

    if '= call ' in l:
        dest, resto = l.split('=', 1)
        nombre = resto.replace('call', '').strip()
        return f'    {dest.strip()} = {nombre}();'

    if l.startswith('return'):
        resto = l[6:].strip()
        return f'    return (int)({traducir_expr(resto)});' if resto else '    return 0;'

    if l.startswith('if '):
        idx   = l.rfind(' goto ')
        cond  = traducir_expr(l[3:idx].strip())
        label = l.split()[-1]
        return f'    if ({cond}) goto {label};'

    if l.startswith('goto '):
        return f'    goto {l.split()[1]};'

    if '=' in l:
        dest, resto = l.split('=', 1)
        return f'    {dest.strip()} = {traducir_expr(resto.strip())};'

    return f'    // {l}'


def generar_cpp(codigo_c3d, tabla):
    cpp = [
        '#include <stdio.h>',
        '#include <string.h>',
        '',
        'int main() {'
    ]

    for nombre, tipo in tabla.items():
        if tipo == 'shen':
            cpp.append(f'    const char* {nombre} = "";')
        else:
            cpp.append(f'    {TIPO_CPP.get(tipo, "double")} {nombre} = 0;')

    temps = sorted(
        {l.split('=')[0].strip() for l in codigo_c3d
         if '=' in l and not l.strip().endswith(':')
         and re.match(r'^t\d+$', l.split('=')[0].strip())},
        key=lambda x: int(x[1:])
    )
    for t in temps:
        cpp.append(f'    double {t};')

    if tabla or temps:
        cpp.append('')

    for linea in codigo_c3d:
        cpp.append(c3d_a_cpp(linea, tabla))

    cpp += ['', '    return 0;', '}']
    return '\n'.join(cpp)


def construir_filas(codigo, prefijo_id):
    filas = ''
    for i, linea in enumerate(codigo):
        if not linea.strip():
            continue
        tipo  = tipo_instruccion(linea)
        color = COLORES.get(tipo, '#c8d8f8')
        bg    = '#0d1225' if i % 2 == 0 else '#090d1a'
        badge_color = COLORES.get(tipo, '#3a4a6a')
        filas += f"""
        <tr style="background:{bg}">
            <td>{i + 1}</td>
            <td style="color:{color};font-weight:500">{linea}</td>
            <td><span style="color:{badge_color};font-size:10px;letter-spacing:.06em">{tipo}</span></td>
        </tr>"""
    return filas


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
        print("Errores sintacticos")
        return

    semantico = AnalizadorSemantico()
    semantico.visit(tree)

    if semantico.errores:
        print("Errores semanticos")
        return

    # C3D crudo
    generador = C3DGenerador(semantico.tabla_simbolos)
    generador.visit(tree)
    codigo_crudo = generador.codigo

    # C3D optimizado
    opt = C3DOptimizador(codigo_crudo, semantico.tabla_simbolos)
    codigo_opt = opt.optimizar()

    # guardar archivos planos
    with open(os.path.join(ruta_reportes, 'salida.c3d'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(codigo_crudo))

    with open(os.path.join(ruta_reportes, 'salida_opt.c3d'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(codigo_opt))

    # C++ desde el codigo optimizado
    cpp_texto = generar_cpp(codigo_opt, semantico.tabla_simbolos)
    with open(os.path.join(ruta_reportes, 'salida.cpp'), 'w', encoding='utf-8') as f:
        f.write(cpp_texto)

    if not os.path.exists(ruta_base):
        print("ERROR: No existe c3d_base.html")
        return

    with open(ruta_base, 'r', encoding='utf-8') as f:
        html = f.read()

    # inyectar filas tabla cruda
    filas_crudas = construir_filas(codigo_crudo, 'crudo')
    html = html.replace(
        '<tbody id="tbody">',
        f'<tbody id="tbody">{filas_crudas}'
    )

    # inyectar filas tabla optimizada
    filas_opt = construir_filas(codigo_opt, 'opt')
    html = html.replace(
        '<tbody id="tbody-opt">',
        f'<tbody id="tbody-opt">{filas_opt}'
    )

    # inyectar cpp
    cpp_escaped = cpp_texto.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    html = re.sub(
        r'<pre id="cpp-code">.*?</pre>',
        f'<pre id="cpp-code">{cpp_escaped}</pre>',
        html,
        flags=re.DOTALL
    )

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)

    total_crudo = len([l for l in codigo_crudo if l.strip()])
    total_opt   = len([l for l in codigo_opt   if l.strip()])
    reduccion   = total_crudo - total_opt

    print(f"C3D crudo: {total_crudo} instrucciones | Optimizado: {total_opt} | Reduccion: {reduccion}")


if __name__ == '__main__':
    main()