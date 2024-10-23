from flask import Flask, jsonify, request, redirect, url_for, flash
import backend2 as b2



app = Flask(__name__)


@app.route('/subir', methods=['POST'])  # Página de inicio
def subir():
    if request.method == "POST":
        archivo = request.files["archivo"]
        contenido=archivo.read().decode("utf-8")
        print(b2.crearArchivo(contenido))
        return jsonify({"status": "ok"}), 200








if __name__ == '__main__':
    app.run(debug=True)