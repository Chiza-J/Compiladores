from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import zipfile
import sys

app = Flask(__name__)


RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))


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
        elif salida:
            return salida
        else:
            return "Sin salida"

    except Exception as e:
        return f"Excepción: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analizar', methods=['POST'])
def analizar():
    codigo = request.json.get('codigo', '')

    ruta_archivo = os.path.join(RUTA_PROYECTO, 'programa.leng')
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(codigo)

    print("Nuevo análisis ejecutado")

    rutas_reportes = [
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_tokens.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'tabla_simbolos.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_c3d.html')
    ]

    for ruta in rutas_reportes:
        if os.path.exists(ruta):
            os.remove(ruta)

    # RUTAS DE LOS REPORTES
    ruta_tokens = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'reporte_tokens.py')
    ruta_errores = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'reporte_errores.py')
    ruta_rec = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'reporte_recuperables.py')
    ruta_semantico = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'reporte_semantico.py')
    ruta_tabla = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'tabla_simbolos.py')
    ruta_c3d = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'generar_c3d.py')


    salida_tokens = ejecutar(ruta_tokens)
    salida_errores = ejecutar(ruta_errores)
    salida_rec = ejecutar(ruta_rec)
    salida_semantico = ejecutar(ruta_semantico)
    salida_tabla = ejecutar(ruta_tabla)
    salida_c3d  = ejecutar(ruta_c3d)

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


@app.route('/tokens')
def ver_tokens():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_tokens.html')
    base = os.path.join(RUTA_PROYECTO, 'reportes_html', 'tokens_base.html')

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


@app.route('/errores')
def ver_errores():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html')
    base = os.path.join(RUTA_PROYECTO, 'reportes_html', 'errores_base.html')

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)


@app.route('/recuperables')
def ver_recuperables():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html')
    base = os.path.join(RUTA_PROYECTO, 'reportes_html', 'recuperables_base.html')

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)

#FUNCION DE DESCARGA
@app.route('/descargar')
def descargar_todo():
    ruta_zip = os.path.join(RUTA_PROYECTO, 'compilador_resultado.zip')

    with zipfile.ZipFile(ruta_zip, 'w') as zipf:

        ruta_codigo = os.path.join(RUTA_PROYECTO, 'programa.leng')
        if os.path.exists(ruta_codigo):
            zipf.write(ruta_codigo, 'programa.leng')

        #SE CREA CARPETA PARA GUARDAR LOS REPORTES
        ruta_tokens = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_tokens.html')
        ruta_errores = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html')
        ruta_rec = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html')
        ruta_tabla = os.path.join(RUTA_PROYECTO, 'reportes_html', 'tabla_simbolos.html')

        if os.path.exists(ruta_tokens):
            zipf.write(ruta_tokens, 'reportes/reporte_tokens.html')

        if os.path.exists(ruta_errores):
            zipf.write(ruta_errores, 'reportes/reporte_errores.html')

        if os.path.exists(ruta_rec):
            zipf.write(ruta_rec, 'reportes/reporte_recuperables.html')
        
        if os.path.exists(ruta_tabla):
            zipf.write(ruta_tabla, 'reportes/tabla_simbolos.html')

    return send_file(ruta_zip, as_attachment=True)

@app.route('/limpiar', methods=['POST'])
def limpiar():
    rutas = [
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_tokens.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html'),
        os.path.join(RUTA_PROYECTO, 'programa.leng'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'tabla_simbolos.html'),
    ]

    for ruta in rutas:
        if os.path.exists(ruta):
            os.remove(ruta)

    return jsonify({"mensaje": "Entorno limpio"})

@app.route('/semantico')
def ver_semantico():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_semantico.html')
    base = os.path.join(RUTA_PROYECTO, 'reportes_html', 'semantico_base.html')
    if os.path.exists(ruta):
        return send_file(ruta)
    return send_file(base)

@app.route('/tabla_simbolos')
def ver_tabla_simbolos():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'tabla_simbolos.html')
    base = os.path.join(RUTA_PROYECTO, 'reportes_html', 'tabla_simbolos_base.html')

    if os.path.exists(ruta):
        return send_file(ruta)

    return send_file(base)

@app.route('/c3d')
def ver_c3d():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_c3d.html')
    base = os.path.join(RUTA_PROYECTO, 'reportes_html', 'c3d_base.html')
    if os.path.exists(ruta):
        return send_file(ruta)
    return send_file(base)

if __name__ == '__main__':
    app.run(debug=True)
