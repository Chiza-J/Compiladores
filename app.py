from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))

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

    salida = ""

    try:
        # Ejecutar tus scripts
        resultado1 = subprocess.run(
            ['python', 'reportes_html/reporte_tokens.py'],
            capture_output=True, text=True
        )

        resultado2 = subprocess.run(
            ['python', 'reportes_html/reporte_errores.py'],
            capture_output=True, text=True
        )

        resultado3 = subprocess.run(
            ['python', 'reportes_html/reporte_recuperables.py'],
            capture_output=True, text=True
        )

        salida = resultado1.stdout + resultado2.stdout + resultado3.stdout

    except Exception as e:
        salida = str(e)

    return jsonify({"salida": salida})


if __name__ == '__main__':
    app.run(debug=True)