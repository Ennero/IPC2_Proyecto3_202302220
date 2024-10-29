from flask import Flask, jsonify, request, redirect, url_for, flash
import backend2 as b2
from flask import redirect




app = Flask(__name__)

#---------------------------------------------------------------------------------
@app.route('/subir', methods=['POST'])  # Página de inicio
def subir():
    if request.method == "POST": # Si se envía un POST
        archivo = request.files["archivo"] #Obtengo el archivo
        contenido=archivo.read().decode("utf-8") #Obtengo el contenido del archivo en formato string

        #Procesando el archivo
        print(b2.crearArchivo(contenido)) #Creo el archivo de entrada e imprimo el retorno

        #print(contenido) #Imprimo el contenido del archivo para ver si se envió bien
        #print("Eso fue el contenido")
        
        return jsonify({"contenido": contenido}), 200
#---------------------------------------------------------------------------------
@app.route('/reset', methods=['POST'])  # Página de inicio
def reset():
    if request.method == "POST":
        b2.limpiar()
        return jsonify({"mensaje": "Reset exitoso"}), 200
    
@app.route('/procesar')#Dirección para procesar los datos
def procesar():

    b2.procesar() #Proceso el archivo
    b2.dividirFechas() #Divido todo lo procesado en las fechas
    b2.crearArchivoSalida() #Creo el archivo de salida

    with open("data/salida.xml", "r",encoding="utf-8") as f:
        salida = f.read() #Obtengo el contenido del archivo de salida

    #print(salida)

    #Retorno la salida y el contenido del archivo
    return jsonify({"salida": salida, "mensaje":"Procesado exitoso"}), 200
#---------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------
@app.route('/resumenPorFecha', methods=['POST','GET'])  # Página de inicio
def resumenPorFecha():
    if request.method == "POST":
        fechita = request.form["fechita"]
        print("-----------------------")
        #print(fechita)
        empresas=b2.obtenerEmpresas(fechita)
        #print(empresas)

        return jsonify({"empresas": empresas}), 200
    
    
    #print("Hola")
    fechas=b2.obtenerFechas()
    #print(fechas)
    return jsonify({"fechas": fechas}), 200

@app.route('/graficaTodo', methods=['POST','GET'])  # Página de inicio
def graficaTodo():
    if request.method == "POST":
        fechita = request.form["fechita"] #Obtiene la fecha en forma de string
        print("-----------------------")
        #print(fechita)
        todo=b2.obtenerTodoFecha(fechita)
        #print(todo)

        return jsonify({"todo": todo}), 200
    
    #print("Hola")
    fechas=b2.obtenerFechas()
    #print(fechas)
    return jsonify({"fechas": fechas}), 200

@app.route('/graficaEmpresa', methods=['POST','GET'])  # Página de inicio
def graficaEmpresa():
    if request.method == "POST":
        empresa = request.form["empresa"] #Obtiene la empresa en forma de string
        fechita = request.form["fechita"] #Obtiene la fecha en forma de string
        print("-----------------------")
        #print(fechita)
        todo=b2.obtenerEmpresaEspecifica(fechita,empresa)
        #print(todo)

        return jsonify({"todo": todo}), 200
    
    #print("Hola")
    empresas=b2.obtenerEmpresas()
    #print(fechas)
    return jsonify({"empresas": empresas}), 200
#---------------------------------------------------------------------------------
@app.route('/prueba', methods=['POST','GET'])  # Página de inicio   
def prueba():
    if request.method == "POST":

        archivo = request.files["archivo"]
        mensaje=archivo.read().decode("utf-8")
        
        print(mensaje)
        respuesta=b2.prueba(mensaje)

        return jsonify({"mensaje": respuesta}), 200
#---------------------------------------------------------------------------------
@app.route('/fecha1', methods=['POST','GET'])  # Página de inicio
def fecha1():
    if request.method == "POST":
        fecha1 = request.form["fecha1"]
        #print("-----------------------")
        #print(fecha1)
        fechas2=b2.obtenerFechas2(fecha1)
        return jsonify({"fechas2": fechas2}), 200

@app.route('/fecha2', methods=['POST','GET'])  # Página de inicio
def fecha2():
    if request.method == "POST":
        fecha2 = request.form["fecha2"]
        fecha1 = request.form["fecha1"]
        print("-----------------------")
        empresasR=b2.obtenerEmpresasEnRango(fecha1,fecha2)
        #print("En el backend : ",fecha1,fecha2,empresasR)

        return jsonify({"empresasR": empresasR}), 200
    
#En contrucciondkfnaskldflksdcfmlkadskfasmdklfjadsklkfjsjdfsdfsdf
@app.route('/graficaTodoEnRango', methods=['POST','GET'])  # Página de inicio
def graficaTodoEnRango():
    if request.method == "POST":
        fecha1 = request.form["fecha1"]
        fecha2= request.form["fecha2"]
        print("-----------------------")
        #print(fechita)
        todo=b2.obtenerTODOEnRango(fecha1,fecha2)
        fechonas=b2.obtenerListaFechasRango(fecha1,fecha2)
        #print(todo)
        #print(fechonas)

        return jsonify({"todo": todo,'fechonas':fechonas}), 200
    
@app.route('/graficaEmpresaEnRango1', methods=['POST','GET']) 
def graficaEmpresaEnRango1():
    if request.method == "POST":
        empresa = request.form["empresa"]
        fecha1 = request.form["fecha1"]
        fecha2 = request.form["fecha2"]
        #print("Proviniente del frontend")
        #print(empresa,fecha1,fecha2)
        #print("-----------------------")
        #print(fechita)
        todo=b2.obtenerEmpresaEspecificaEnRango1(fecha1,fecha2,empresa)
        print("lo que llegó al backend",todo)
        fechonas=b2.obtenerListaFechasRango(fecha1,fecha2)
        print("---------------------------------------------------")
        print(fechonas)
        return jsonify({"todo": todo,'fechonas':fechonas}), 200

@app.route('/pdf', methods=['POST','GET'])  # Página de inicio
def pdf():

    print(b2.crearPDF())

    return jsonify({"mensaje": "PDF generado"}), 200





# Página de inicio

if __name__ == '__main__':
    app.run(debug=True)