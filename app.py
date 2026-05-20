from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import zipfile
import sys

app = Flask(__name__)

RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))


# EJECUTAR SCRIPTS
def ejecutar(script):
    try:
        python_path = sys.executable

        resultado = subprocess.run(
            [python_path, '-B', script],
            capture_output=True,
            text=True,
            cwd=RUTA_PROYECTO
        )

        salida = resultado.stdout.strip()
        error = resultado.stderr.strip()

        if error:
            return f"ERROR:\n{error}"

        if salida:
            return salida

        return "Sin salida"

    except Exception as e:
        return f"Excepción: {str(e)}"


# VERIFICAR SI HAY ERRORES
def contiene_errores(texto):
    texto = texto.lower()

    if "errores encontrados" in texto:
        if "0 errores encontrados" not in texto and "sin errores" not in texto:
            return True

    if "errores semanticos encontrados" in texto:
        return True

    return False


# INDEX
@app.route('/')
def index():
    return render_template('index.html')


# ANALIZAR
@app.route('/analizar', methods=['POST'])
def analizar():

    codigo = request.json.get('codigo', '')

    ruta_archivo = os.path.join(RUTA_PROYECTO, 'programa.leng')

    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(codigo)

    print("Nuevo análisis ejecutado")

    # LIMPIAR REPORTES ANTERIORES

    rutas_reportes = [
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_tokens.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_semantico.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'tabla_simbolos.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_c3d.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida.cpp'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida.c3d'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida_opt.c3d')
    ]

    for ruta in rutas_reportes:
        if os.path.exists(ruta):
            os.remove(ruta)

    # RUTAS SCRIPTS

    ruta_tokens = os.path.join(
        RUTA_PROYECTO,
        'static',
        'reportes_html',
        'reporte_tokens.py'
    )

    ruta_errores = os.path.join(
        RUTA_PROYECTO,
        'static',
        'reportes_html',
        'reporte_errores.py'
    )

    ruta_rec = os.path.join(
        RUTA_PROYECTO,
        'static',
        'reportes_html',
        'reporte_recuperables.py'
    )

    ruta_semantico = os.path.join(
        RUTA_PROYECTO,
        'static',
        'reportes_html',
        'reporte_semantico.py'
    )

    ruta_tabla = os.path.join(
        RUTA_PROYECTO,
        'static',
        'reportes_html',
        'tabla_simbolos.py'
    )

    ruta_c3d = os.path.join(
        RUTA_PROYECTO,
        'static',
        'reportes_html',
        'generar_c3d.py'
    )

    # EJECUTAR ANALIZADORES

    salida_tokens = ejecutar(ruta_tokens)
    salida_errores = ejecutar(ruta_errores)
    salida_rec = ejecutar(ruta_rec)
    salida_semantico = ejecutar(ruta_semantico)
    salida_tabla = ejecutar(ruta_tabla)

    # VALIDAR SI HAY ERRORES

    hay_errores_lexicos = contiene_errores(salida_errores)
    hay_errores_semanticos = contiene_errores(salida_tabla)

    generar_c3d = not hay_errores_lexicos and not hay_errores_semanticos

    # GENERAR C3D SOLO SI NO HAY ERRORES

    if generar_c3d:
        salida_c3d = ejecutar(ruta_c3d)
    else:
        salida_c3d = (
            "C3D CANCELADO\n"
            "Existen errores léxicos/sintácticos o semánticos."
        )

        # borrar posibles archivos anteriores
        archivos_c3d = [
            os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida.cpp'),
            os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida.c3d'),
            os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida_opt.c3d'),
            os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_c3d.html')
        ]

        for archivo in archivos_c3d:
            if os.path.exists(archivo):
                os.remove(archivo)

    # SALIDA FINAL

    salida = f"""
================= ANALIZADOR =================

 TOKENS:
{salida_tokens}

 ERRORES:
{salida_errores}

 RECUPERABLES:
{salida_rec}

 SEMÁNTICO:
{salida_semantico}

 TABLA DE SÍMBOLOS:
{salida_tabla}

 CÓDIGO 3 DIRECCIONES:
{salida_c3d}

==============================================
"""

    return jsonify({"salida": salida})


# TOKENS
@app.route('/tokens')
def ver_tokens():

    ruta = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'reporte_tokens.html'
    )

    base = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'tokens_base.html'
    )

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


# ERRORES
@app.route('/errores')
def ver_errores():

    ruta = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'reporte_errores.html'
    )

    base = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'errores_base.html'
    )

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


# RECUPERABLES
@app.route('/recuperables')
def ver_recuperables():

    ruta = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'reporte_recuperables.html'
    )

    base = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'recuperables_base.html'
    )

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


# SEMANTICO
@app.route('/semantico')
def ver_semantico():

    ruta = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'reporte_semantico.html'
    )

    base = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'semantico_base.html'
    )

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


# TABLA DE SIMBOLOS
@app.route('/tabla_simbolos')
def ver_tabla_simbolos():

    ruta = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'tabla_simbolos.html'
    )

    base = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'tabla_simbolos_base.html'
    )

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


# C3D
@app.route('/c3d')
def ver_c3d():

    ruta = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'reporte_c3d.html'
    )

    base = os.path.join(
        RUTA_PROYECTO,
        'reportes_html',
        'c3d_base.html'
    )

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


# DESCARGAR ZIP
@app.route('/descargar')
def descargar_todo():

    ruta_zip = os.path.join(
        RUTA_PROYECTO,
        'compilador_resultado.zip'
    )

    with zipfile.ZipFile(ruta_zip, 'w') as zipf:

        ruta_codigo = os.path.join(
            RUTA_PROYECTO,
            'programa.leng'
        )

        if os.path.exists(ruta_codigo):
            zipf.write(ruta_codigo, 'programa.leng')

        archivos = {
            'reportes/reporte_tokens.html':
                'reportes_html/reporte_tokens.html',

            'reportes/reporte_errores.html':
                'reportes_html/reporte_errores.html',

            'reportes/reporte_recuperables.html':
                'reportes_html/reporte_recuperables.html',

            'reportes/reporte_semantico.html':
                'reportes_html/reporte_semantico.html',

            'reportes/tabla_simbolos.html':
                'reportes_html/tabla_simbolos.html',

            'reportes/reporte_c3d.html':
                'reportes_html/reporte_c3d.html',

            'reportes/salida.cpp':
                'reportes_html/salida.cpp',

            'reportes/salida.c3d':
                'reportes_html/salida.c3d',

            'reportes/salida_opt.c3d':
                'reportes_html/salida_opt.c3d'
        }

        for nombre_zip, archivo_real in archivos.items():

            ruta_real = os.path.join(
                RUTA_PROYECTO,
                archivo_real
            )

            if os.path.exists(ruta_real):
                zipf.write(ruta_real, nombre_zip)

    return send_file(ruta_zip, as_attachment=True)


# LIMPIAR
@app.route('/limpiar', methods=['POST'])
def limpiar():

    rutas = [
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_tokens.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_semantico.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'tabla_simbolos.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_c3d.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida.cpp'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida.c3d'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'salida_opt.c3d'),
        os.path.join(RUTA_PROYECTO, 'programa.leng')
    ]

    for ruta in rutas:
        if os.path.exists(ruta):
            os.remove(ruta)

    return jsonify({"mensaje": "Entorno limpio"})


# MAIN
if __name__ == '__main__':
    app.run(debug=True)