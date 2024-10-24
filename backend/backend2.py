import xml.etree.ElementTree as ET
import poo
import re


#Variables globales
listaEmpresitas=[] #Lista de empresas
listaPositivos=[] #Lista de palabras positivas
listaNegativos=[] #Lista de palabras negativas
listaMensajes=[] #Lista de mensajes

#             Lugar y fecha: (Guatemala),       (01/04/2022)         (15:43)      Usuario: (map0003@usac.edu) Red social:   (Twitter) ([todo el texto])
patron = r'\s*Lugar\s+y\s+fecha:\s+(\S+),\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})\s+Usuario:\s+(\w+@\w+\.\w+)\s+Red\s+social:\s+(\w+)\s+(.*)'


def crearArchivo(entrada): #Función que crea el archivo de entrada
    archivo = open("data/archivo.xml", "w", encoding="utf-8")
    archivo.write(entrada) #Escribimos el contenido del archivo
    archivo.close() #Cerramos el archivo
    return "Archivo creado con éxito" #Retornamos un mensaje de éxito





def crearSalida(): #Función que crea el archivo de salida
    global listaEmpresitas,listaPositivos,listaNegativos #Variables globales

    try:
        arbol = ET.parse("data/archivo.xml") #Creamos el arbol
        ramas=arbol.getroot() #Obtenemos la raíz del arbol

        for i in ramas.iter('diccionario'):

            for j in i.iter('sentimientos_positivos'): #Iteramos sobre los sentimientos positivos
                for k in j.iter('palabra'): #Iteramos sobre las palabras
                    listaPositivos.append(k.text)

            for j in i.iter('sentimientos_negativos'): #Iteramos sobre los sentimientos negativos
                for k in j.iter('palabra'):
                    listaNegativos.append(k.text)


            for j in i.iter('empresas_analizar'): #Iteramos sobre las empresas

                for k in j.iter('empresa'): #Iteramos sobre las empresas
                    empresa=poo.Empresa
                    servicios=[]
                    
                    for l in k.iter('nombre'): #Agrego el nombre de la empresa
                        nombre=l.text
                        empresa.nombre=nombre

                    for l in k.iter('servicio'): #Iteramos sobre los servicios
                        servicio=poo.Servicio

                        #Coloco el nombre del servicio
                        nombre=l.get('nombre')
                        servicio.nombre=nombre

                        alias=[]
                        for m in l.iter('alias'): #Iteramos sobre los alias
                            alias.append(m.text)

                        servicio.alias=alias
                        servicios.append(servicio)
                    empresa.servicios=servicios      
                    listaEmpresitas.append(empresa) 
            
            
        for i in ramas.iter('lista_mensajes'):
            for j in i.iter('mensaje'): #Iteramos sobre los mensajes
                texto=j.text

                #print(texto)

                mensaje=analizar(texto) #Analizamos el mensaje
            listaMensajes.append(mensaje) #Agregamos el mensaje a la lista de mensajes


    except Exception as e:
        return "Error al abrir el archivo", e #Retornamos un mensaje de error si no se pudo abrir el archivo
    


#Función para analizar los mensajes, encontrar sentimientos y empresas
def analizar(text):
    global listaEmpresitas,listaPositivos,listaNegativos,patron

    #Buscamos el patrón en el texto
    resultado=re.search(patron,text,re.S)

    if resultado: #primer analisis para separar todo en el mensaje
        lugar=resultado.group(1) #Obtenemos el lugar
        fecha=resultado.group(2) #Obtenemos la fecha
        hora=resultado.group(3) #Obtenemos la hora
        usuario=resultado.group(4) #Obtenemos el usuario
        redSocial=resultado.group(5) #Obtenemos la red social
        texto=resultado.group(6) #Obtenemos el texto

    else:
        print ("No se encontraron coincidencias")

    cuentaPositivos=0 #Contador de palabras positivas
    cuentaNegativos=0 #Contador de palabras negativas

    for i in listaPositivos: #Iteramos sobre las palabras positivas
        rege=i #Expresión regular

        cuentaPositivos+=len(re.findall(rege,texto))


    for i in listaNegativos: #Iteramos sobre las palabras negativas
        rege=i
        cuentaNegativos+=len(re.findall(rege,texto))

    empresitas=[] #Lista de empresas en el mensaje

    print(listaEmpresitas[0].nombre)
    print("sdcfksdmhfkcshdfl")
    for i in listaEmpresitas: #Iteramos sobre las empresas
        empresa=i.nombre

        print(empresa)

        empresitas.append(empresa)

    #print("Lugar: ",lugar,"\nFecha: ",fecha,"\nHora: ",hora,"\nUsuario: ",usuario,"\nRed social: ",redSocial,"\nTexto: ",texto,"\nEmpresas: ",empresitas,"\nCuenta negativos: ",cuentaNegativos,"\nCuenta positivos: ",cuentaPositivos)


    mensaje=poo.Mensaje(texto,lugar,fecha,hora,usuario,redSocial,empresitas,cuentaNegativos,cuentaPositivos) #Creamos un objeto de la clase Mensaje
    return mensaje #Retornamos el mensaje




#dsjfhcdfmlkghdslckgsdhlfkfdlscghkml,cnhdsfckhdkjhgcsdfcnsdfkgvnhdsfnhvkdshcgklsdfhgvnsdkjfnhskdj PROBANDO


crearSalida()


