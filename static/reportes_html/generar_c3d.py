import sys
import os
import re

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ruta_raiz)

from antlr4 import *
from antlr_todo.LenguajeLexer   import LenguajeLexer
from antlr_todo.LenguajeParser  import LenguajeParser
from antlr4.error.ErrorListener import ErrorListener
from antlr_todo.AnalizadorSemantico import AnalizadorSemantico
from antlr_todo.C3D_generador       import C3DGenerador, C3DAC_Traductor
from antlr_todo.C3d_optimizador     import C3DOptimizador


class ErrorSilencioso(ErrorListener):
    def __init__(self):
        self.hay_error = False
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True


def tipo_instruccion(linea):
    l = linea.strip()
    if not l:
        return ''
    if l.endswith(':') and ' ' not in l:
        return 'etiqueta'
    if l.startswith('func_begin'):  return 'func_inicio'
    if l.startswith('func_end'):    return 'func_fin'
    if l.startswith('param_decl'):  return 'parametro'
    if l.startswith('arg '):        return 'argumento'
    if l.startswith('if '):         return 'condicional'
    if l.startswith('goto '):       return 'salto'
    if l.startswith('print '):      return 'impresion'
    if l.startswith('read '):       return 'entrada'
    if l.startswith('return'):      return 'retorno'
    if 'call ' in l:                return 'llamada'
    if '=' in l:
        dest = l.split('=')[0].strip()
        if re.match(r'^t\d+$', dest):
            return 'temporal'
        return 'asignacion'
    return ''


COLORES = {
    'etiqueta':   '#a855f7',
    'func_inicio':'#a855f7',
    'func_fin':   '#a855f7',
    'parametro':  '#a855f7',
    'argumento':  '#7a9cc8',
    'condicional':'#f5a623',
    'salto':      '#f5a623',
    'impresion':  '#00d4ff',
    'entrada':    '#00d4ff',
    'retorno':    '#ff4d6a',
    'temporal':   '#4f8ef7',
    'asignacion': '#22f08a',
    'llamada':    '#22f08a',
}


def construir_filas(codigo):
    filas = ''
    for i, linea in enumerate(codigo):
        if not linea.strip():
            continue
        tipo        = tipo_instruccion(linea)
        color       = COLORES.get(tipo, '#c8d8f8')
        badge_color = COLORES.get(tipo, '#3a4a6a')
        bg          = '#0d1225' if i % 2 == 0 else '#090d1a'
        filas += (
            f'\n        <tr style="background:{bg}">'
            f'<td>{i + 1}</td>'
            f'<td style="color:{color};font-weight:500">{linea}</td>'
            f'<td><span style="color:{badge_color};font-size:10px;'
            f'letter-spacing:.06em">{tipo}</span></td>'
            f'</tr>'
        )
    return filas


def main():
    ruta_reportes = os.path.join(ruta_raiz, 'reportes_html')
    ruta_base     = os.path.join(ruta_reportes, 'c3d_base.html')
    ruta_salida   = os.path.join(ruta_reportes, 'reporte_c3d.html')

    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    archivo = os.path.join(ruta_raiz, 'programa.leng')

    # fase sintactica silenciosa
    stream = FileStream(archivo, encoding='utf-8')
    lexer  = LenguajeLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = LenguajeParser(tokens)

    err = ErrorSilencioso()
    parser.removeErrorListeners()
    parser.addErrorListener(err)
    tree = parser.programa()

    if err.hay_error:
        print("Errores sintacticos - no se puede generar C3D")
        return

    # fase semantica
    semantico = AnalizadorSemantico()
    semantico.visit(tree)

    if semantico.errores:
        print("Errores semanticos - no se puede generar C3D")
        return

    # C3D crudo
    # CORREGIDO: pasamos tabla_simbolos del semantico al generador
    generador = C3DGenerador(semantico.tabla_simbolos)
    generador.visit(tree)
    codigo_crudo = generador.codigo

    # C3D optimizado
    opt        = C3DOptimizador(codigo_crudo, semantico.tabla_simbolos)
    codigo_opt = opt.optimizar()

    # guardar archivos planos
    os.makedirs(ruta_reportes, exist_ok=True)
    with open(os.path.join(ruta_reportes, 'salida.c3d'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(codigo_crudo))

    with open(os.path.join(ruta_reportes, 'salida_opt.c3d'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(codigo_opt))

    # C++ desde el codigo optimizado
    # CORREGIDO: pasamos locals_por_funcion del generador al traductor
    traductor = C3DAC_Traductor(
        codigo_opt,
        generador.tabla,                    # tabla con vars locales incluidas
        semantico.tabla_funciones,
        locals_por_funcion=generador._locals_por_funcion,  # ← NUEVO
    )
    cpp_texto = traductor.generar_cpp()

    with open(os.path.join(ruta_reportes, 'salida.cpp'), 'w', encoding='utf-8') as f:
        f.write(cpp_texto)

    # generar HTML del reporte
    if not os.path.exists(ruta_base):
        print("ERROR: No existe c3d_base.html")
        return

    with open(ruta_base, 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace(
        '<tbody id="tbody">',
        f'<tbody id="tbody">{construir_filas(codigo_crudo)}'
    )
    html = html.replace(
        '<tbody id="tbody-opt">',
        f'<tbody id="tbody-opt">{construir_filas(codigo_opt)}'
    )

    cpp_escaped = (cpp_texto
                   .replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;'))
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
    print(f"C3D: {total_crudo} instrucciones | Optimizado: {total_opt} | Reduccion: {reduccion}")


if __name__ == '__main__':
    main()