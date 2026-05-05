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


# OPERADORES
OP_CPP = {
    'plu': '+',
    'moan': '-',
    'par': '*',
    'bag': '/',
    'minog': '<',
    'aye': '>',
    'compag': '==',
}

# TIPOS
TIPO_CPP = {
    'ontie': 'int',
    'flote': 'float',
    'duble': 'double',
    'shen':  'string'
}


# ERROR LISTENER
class ErrorSilencioso(ErrorListener):
    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


# TRADUCIR EXPRESIÓN
def traducir_expr(expr):
    for op_l, op_c in OP_CPP.items():
        expr = expr.replace(op_l, op_c)
    return expr


# TRADUCIR LÍNEA C3D  C++
def c3d_a_cpp(linea):
    l = linea.strip()

    if not l:
        return ''

    # etiqueta
    if l.endswith(':') and ' ' not in l:
        return f'    {l}'

    # print
    if l.startswith('print '):
        val = traducir_expr(l[6:])
        return f'    cout << {val} << endl;'

    # return
    if l.startswith('return'):
        val = l[6:].strip()
        return f'    return {val};' if val else '    return 0;'

    # if
    if l.startswith('if '):
        idx = l.rfind(' goto ')
        cond = traducir_expr(l[3:idx])
        label = l.split()[-1]
        return f'    if ({cond}) goto {label};'

    # goto
    if l.startswith('goto '):
        return f'    {l};'

    # asignación
    if '=' in l:
        dest, expr = l.split('=', 1)
        return f'    {dest.strip()} = {traducir_expr(expr.strip())};'

    return f'    // {l}'


# GENERAR C++
def generar_cpp(codigo_c3d, tabla):
    cpp = [
        '#include <iostream>',
        '#include <string>',
        'using namespace std;',
        '',
        'int main() {'
    ]

    # evitar duplicados reales
    variables_declaradas = set()

    for nombre, tipo in tabla.items():
        if nombre in variables_declaradas:
            continue

        variables_declaradas.add(nombre)

        if tipo == 'shen':
            cpp.append(f'    string {nombre} = "";')
        else:
            cpp.append(f'    {TIPO_CPP.get(tipo, "double")} {nombre} = 0;')

    # detectar temporales sin chocar con variables
    temps = sorted({
        l.split('=')[0].strip()
        for l in codigo_c3d
        if '=' in l
        and l.split('=')[0].strip().startswith('t')
        and l.split('=')[0].strip() not in variables_declaradas
    })

    for t in temps:
        cpp.append(f'    string {t};')  # temporales universales

    cpp.append('')

    for linea in codigo_c3d:
        cpp.append(c3d_a_cpp(linea))

    cpp += ['', '    return 0;', '}']
    return '\n'.join(cpp)


# MAIN
def main():

    ruta_html = os.path.join(ruta_raiz, 'reportes_html', 'c3d_base.html')
    ruta_salida = os.path.join(ruta_raiz, 'reportes_html', 'reporte_c3d.html')

    archivo = os.path.join(ruta_raiz, 'programa.leng')

    stream = FileStream(archivo, encoding='utf-8')
    lexer = LenguajeLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = LenguajeParser(tokens)

    err = ErrorSilencioso()
    parser.removeErrorListeners()
    parser.addErrorListener(err)

    tree = parser.programa()

    #  error sintáctico
    if err.hay_error:
        print("Errores sintácticos")
        return

    # semántico
    semantico = AnalizadorSemantico()
    semantico.visit(tree)

    if semantico.errores:
        print("Errores semánticos:")
        for e in semantico.errores:
            print(e)
        return

    # generar C3D
    generador = C3DGenerador(semantico.tabla_simbolos)
    generador.visit(tree)

    codigo_c3d = generador.codigo

    # generar C++
    cpp_texto = generar_cpp(codigo_c3d, semantico.tabla_simbolos)

    #  HTML 
    with open(ruta_html, 'r', encoding='utf-8') as f:
        html = f.read()

    # filas C3D
    filas = ''
    for i, linea in enumerate(codigo_c3d):
        if linea.strip():
            filas += f"<tr><td>{i+1}</td><td>{linea}</td><td></td></tr>"

    # reemplazo robusto tabla
    html = re.sub(
        r'<tbody id="tbody">.*?</tbody>',
        f'<tbody id="tbody">{filas}</tbody>',
        html,
        flags=re.DOTALL
    )

    # escapar C++
    cpp_escaped = cpp_texto.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

    # reemplazo robusto código
    html = re.sub(
        r'<pre id="cpp-code">.*?</pre>',
        f'<pre id="cpp-code">{cpp_escaped}</pre>',
        html,
        flags=re.DOTALL
    )

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Reporte generado correctamente")


if __name__ == "__main__":
    main()