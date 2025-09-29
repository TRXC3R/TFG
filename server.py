from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/subir', methods=['POST'])
def subir():
    file = request.files['imagen']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    # Guardar ruta en la base de datos...
    return 'OK'

@app.route('/imagenes')
def imagenes():
    imagenes = os.listdir(UPLOAD_FOLDER)  # Consulta la base de datos idealmente
    return render_template('listado.html', imagenes=imagenes)

@app.route('/uploads/<filename>')
def mostrar_imagen(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run()
