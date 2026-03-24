from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

# Ruta base del proyecto
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

    # Guardar código en archivo
    ruta_archivo = os.path.join(RUTA_PROYECTO, 'programa.leng')
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(codigo)

    print("Nuevo análisis ejecutado")

    # Rutas ABSOLUTAS (clave)
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
    if os.path.exists(ruta):
        return send_file(ruta)
    return "Primero debes analizar el código"


@app.route('/errores')
def ver_errores():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_errores.html')
    if os.path.exists(ruta):
        return send_file(ruta)
    return "Primero debes analizar el código"


@app.route('/recuperables')
def ver_recuperables():
    ruta = os.path.join(RUTA_PROYECTO, 'reportes_html', 'reporte_recuperables.html')
    if os.path.exists(ruta):
        return send_file(ruta)
    return "Primero debes analizar el código"


if __name__ == '__main__':
    app.run(debug=True)