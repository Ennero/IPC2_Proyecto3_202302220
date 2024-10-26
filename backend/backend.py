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
    
@app.route('/reset', methods=['POST'])  # Página de inicio
def reset():
    if request.method == "POST":
        b2.limpiar()
        return jsonify({"mensaje": "Reset exitoso"}), 200

@app.route('/consulta', methods=['GET'])  # Página de inicio
def consulta():
    if request.method == "GET":
        try:
            with open("data/salida.xml", "r",encoding="utf-8") as f:
                salida = f.read()
            print(salida)
            return jsonify({"salida": salida}), 200
        except:
            return jsonify({"salida": ""}), 200


@app.route('/resumenPorFecha', methods=['POST','GET'])  # Página de inicio
def resumenPorFecha():
    if request.method == "POST":
        fechita = request.form["fechita"]
        print("-----------------------")
        #print(fechita)
        empresas=b2.obtenerEmpresas(fechita)
        #print(empresas)

        return jsonify({"empresas": empresas}), 200
    
    
    print("Hola")
    fechas=b2.obtenerFechas()
    #print(fechas)
    return jsonify({"fechas": fechas}), 200




if __name__ == '__main__':
    app.run(debug=True)