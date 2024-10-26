from flask import Flask, jsonify, request, redirect, url_for, flash
import backend2 as b2
from flask import redirect



app = Flask(__name__)


@app.route('/subir', methods=['POST'])  # Página de inicio
def subir():
    if request.method == "POST":
        archivo = request.files["archivo"]
        contenido=archivo.read().decode("utf-8")

        #Procesando el archivo
        print(b2.crearArchivo(contenido))

        print(contenido)
        print("Eso fue el contenido")
        b2.procesar()
        b2.dividirFechas()
        b2.crearArchivoSalida()

        with open("data/salida.xml", "r",encoding="utf-8") as f:
            salida = f.read()

        #print(contenido)

        return jsonify({"salida": salida, "contenido": contenido}), 200
    










if __name__ == '__main__':
    app.run(debug=True)