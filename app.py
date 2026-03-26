from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import zipfile

app = Flask(__name__)


RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))


def ejecutar(script):
    try:
        python_path = os.path.join(RUTA_PROYECTO, 'venv', 'Scripts', 'python.exe')

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
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html')
    ]

    for ruta in rutas_reportes:
        if os.path.exists(ruta):
            os.remove(ruta)

    # RUTAS DE LOS REPORTES
    ruta_tokens = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'reporte_tokens.py')
    ruta_errores = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'reporte_errores.py')
    ruta_rec = os.path.join(RUTA_PROYECTO, 'static', 'reportes_html', 'reporte_recuperables.py')

    salida_tokens = ejecutar(ruta_tokens)
    salida_errores = ejecutar(ruta_errores)
    salida_rec = ejecutar(ruta_rec)

    salida = f"""
================= ANALIZADOR =================

 TOKENS:
{salida_tokens}

 ERRORES:
{salida_errores}

 RECUPERABLES:
{salida_rec}

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

        if os.path.exists(ruta_tokens):
            zipf.write(ruta_tokens, 'reportes/reporte_tokens.html')

        if os.path.exists(ruta_errores):
            zipf.write(ruta_errores, 'reportes/reporte_errores.html')

        if os.path.exists(ruta_rec):
            zipf.write(ruta_rec, 'reportes/reporte_recuperables.html')

    return send_file(ruta_zip, as_attachment=True)

@app.route('/limpiar', methods=['POST'])
def limpiar():
    rutas = [
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_tokens.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html'),
        os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html'),
        os.path.join(RUTA_PROYECTO, 'programa.leng')
    ]

    for ruta in rutas:
        if os.path.exists(ruta):
            os.remove(ruta)

    return jsonify({"mensaje": "Entorno limpio"})


if __name__ == '__main__':
    app.run(debug=True)