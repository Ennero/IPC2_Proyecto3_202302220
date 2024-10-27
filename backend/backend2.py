import xml.etree.ElementTree as ET
import poo
import re
import os

#Variables globales
entrada = ""
salida = ""


#Listas globales
listaEmpresitas=[] #Lista de empresas
listaPositivos=[] #Lista de palabras positivas
listaNegativos=[] #Lista de palabras negativas
listaMensajes=[] #Lista de mensajes
listaFechas = [] #Lista de fechas

#             Lugar y fecha: (Guatemala),       (01/04/2022)         (15:43)      Usuario: (map0003@usac.edu) Red social:   (Twitter) ([todo el texto])
patron = r'\s*Lugar\s+y\s+fecha:\s+(\S+),\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})\s+Usuario:\s+(\w+@\w+\.\w+)\s+Red\s+social:\s+(\w+)\s+(.*)'

def limpiar(): #Función para limpiar las listas globales
    global listaEmpresitas,listaPositivos,listaNegativos,listaMensajes,listaFechas #Variables globales
    listaEmpresitas.clear() #Limpiamos la lista de empresas
    listaPositivos.clear() #Limpiamos la lista de palabras positivas
    listaNegativos.clear() #Limpiamos la lista de palabras negativas
    listaMensajes.clear() #Limpiamos la lista de mensajes
    listaFechas.clear() #Limpiamos la lista de fechas

    #Limpiamos el archivo de entrada
    if os.path.exists("data/archivo.xml"):
        os.remove("data/archivo.xml")
    else:
        print("El archivo no existe")

    #Limpiamos el archivo de salida
    if os.path.exists("data/salida.xml"):
        os.remove("data/salida.xml")
    else:
        print("La salida no existe")


def crearArchivo(entrada): #Función que crea el archivo de entrada
    archivo = open("data/archivo.xml", "w", encoding="utf-8")
    archivo.write(entrada) #Escribimos el contenido del archivo
    archivo.close() #Cerramos el archivo
    return "Archivo creado con éxito" #Retornamos un mensaje de éxito
#---------------------------------------------------------------------------------------------------
#Función para procesar el archivo XML de entrada
def procesar():
    global listaEmpresitas,listaPositivos,listaNegativos #Variables globales


    try:
        arbol = ET.parse("data/archivo.xml") #Creamos el arbol
        ramas=arbol.getroot() #Obtenemos la raíz del arbol

        for i in ramas.iter('diccionario'):

            for j in i.iter('sentimientos_positivos'): #Iteramos sobre los sentimientos positivos
                for k in j.iter('palabra'): #Iteramos sobre las palabras
                    repetido=False

                    #Verificación de que no esté repetido el valor
                    for l in listaPositivos: #Iteramos sobre las palabras positivas
                        if k.text==l: #Si la palabra ya está en la lista
                            repetido=True #La palabra está repetida
                    if repetido==False: #Si la palabra no está repetida
                        listaPositivos.append(k.text) #Agregamos la palabra a la lista de palabras positivas

            for j in i.iter('sentimientos_negativos'): #Iteramos sobre los sentimientos negativos
                for k in j.iter('palabra'): #Iteramos sobre las palabras
                    repetido=False #Variable para verificar si la palabra está repetida

                    #Verificación de que no esté repetido el valor
                    for l in listaNegativos: #Iteramos sobre las palabras negativas
                        if k.text==l: #Si la palabra ya está en la lista
                            repetido=True #La palabra está repetida
                    if repetido==False: #Si la palabra no está repetida
                        listaNegativos.append(k.text) #Agregamos la palabra a la lista de palabras negativas


            for j in i.iter('empresas_analizar'): #Iteramos sobre las empresas

                for k in j.iter('empresa'): #Iteramos sobre las empresas
                    servicios=[] #Lista de servicios
                    
                    for l in k.iter('nombre'): #Agrego el nombre de la empresa
                        nombre=l.text #Obtenemos el nombre de la empresa

                    for l in k.iter('servicio'): #Iteramos sobre los servicios

                        #Coloco el nombre del servicio
                        nombreS=l.get('nombre') #Obtenemos el nombre del servicio

                        alias=[] #Lista de alias
                        for m in l.iter('alias'): #Iteramos sobre los alias
                            alias.append(m.text) #Agregamos el alias a la lista de alias

                        servicio=poo.Servicio(nombreS,alias) #Creamos un objeto de la clase Servicio
                        servicios.append(servicio) #Agregamos el servicio a la lista de servicios
                    empresa=poo.Empresa(nombre,servicios) #Creamos un objeto de la clase Empresa con su nombre y la lista de servicios
                    listaEmpresitas.append(empresa) #Agregamos la empresa a la lista de empresas

            
        #Creación y almacenamiento de los mensajes
        for i in ramas.iter('lista_mensajes'): #Iteramos sobre la lista de mensajes
            for j in i.iter('mensaje'): #Iteramos sobre los mensajes
                texto=j.text #Obtenemos el texto del mensaje

                mensaje=analizarMensaje(texto) #Analizamos el mensaje con la subrutina analizarMensaje
            
                listaMensajes.append(mensaje) #Agregamos el mensaje a la lista de mensajes
                #print("lugar: ",mensaje.lugar,"fecha: ",mensaje.fecha,"hora: ",mensaje.hora,"usuario: ",mensaje.usuario,"red social: ",mensaje.redSocial,"empresas: ",mensaje.empresas,"negativos: ",mensaje.negativos,"positivos: ",mensaje.positivos)

    except Exception as e: #Manejo de excepciones
        return "Error al abrir el archivo", e 
    
#Quitar a futuro lo de limpiar para mantenerse con el tiempo

#Función para analizar los mensajes, encontrar sentimientos y empresas con sus servicios
def analizarMensaje(text):
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
        rege=r'\b' + i.replace(' ', r'\s*') + r'\b' #Expresión regular
        
        cuentaPositivos+=len(re.findall(rege,texto)) #Contamos las palabras positivas en el texto


    for i in listaNegativos: #Iteramos sobre las palabras negativas
        rege=r'\b' + i.replace(' ', r'\s*') + r'\b'
        cuentaNegativos+=len(re.findall(rege,texto)) #Contamos las palabras negativas en el texto

    empresitas=[] #Lista de empresas en el mensaje

#------------------------------------AQUI EMPIEZA EL ANALISIS DE EMPRESAS----------------------------------------------

    for i in listaEmpresitas: #Iteramos sobre las empresas
        empresaN=i.nombre

        #Buscamos la empresa en el texto
        empresaseta=len(re.findall(r'\b' +empresaN.replace(' ', r'\s*')+ r'\b',texto))


        if empresaseta>0: #Si la empresa está en el texto
            listaServicios=[] #Lista de servicios

            #-------------------------------------
            for j in i.servicios: #Iteramos sobre los servicios
                servicio=j.nombre #Obtenemos el nombre del servicio
                cuntaAlias=0 #Contador de alias

                #Buscamos el servicio en el texto y lo sumamos al contador
                cuntaAlias+=len(re.findall(r'\b' +servicio.replace(' ', r'\s*')+ r'\b',texto,re.S))

                #Iteramos sobre los alias
                for k in j.alias: 

                    #Buscamos el alias en el texto y lo sumamos al contador
                    rege = r'\b' + k.replace(' ', r'\s*') + r'\b'
                    #print(rege)

                    #Sumamos al contador el alies, si es que se encuentra
                    cuntaAlias=cuntaAlias+len(re.findall(str(rege),str(texto),re.DOTALL))
                
                #Creamos un objeto de la clase Servicinho y sus atributos
                servicinho=poo.Servicinho(servicio,cuntaAlias)

                #Agregamos el servicio a la lista de servicios
                listaServicios.append(servicinho)
            #------------------------------------

            #Creamos un objeto de la clase Empresinha y sus atributos
            empresa=poo.Empresinha(empresaN,listaServicios)
            
            #Agregamos la empresa a la lista de empresas
            empresitas.append(empresa)
            

    #Imprimimos los datos del mensaje para confirmar que lo haya hecho bien :)
    #print("Lugar: ",lugar,"\nFecha: ",fecha,"\nHora: ",hora,"\nUsuario: ",usuario,"\nRed social: ",redSocial,"\nTexto: ",texto,"\nEmpresas: ",len(empresitas),"\nCuenta negativos: ",cuentaNegativos,"\nCuenta positivos: ",cuentaPositivos)

    #Imprimimos las empresas y sus servicios para confirmar que lo haya hecho bien :)
    '''for i in empresitas:
        print(i.nombre)
        for j in i.servicios:
            print(j.nombre)
            print(j.cantidad)'''

    #Creamos un objeto de la clase Mensaje con sus atributos
    mensaje=poo.Mensaje(texto,lugar,fecha,hora,usuario,redSocial,empresitas,cuentaNegativos,cuentaPositivos) #Creamos un objeto de la clase Mensaje

    #print("lugar: ",mensaje.lugar,"fecha: ",mensaje.fecha,"hora: ",mensaje.hora,"usuario: ",mensaje.usuario,"red social: ",mensaje.redSocial,"empresas: ",mensaje.empresas,"negativos: ",mensaje.negativos,"positivos: ",mensaje.positivos)

    return mensaje #Retornamos el mensaje
#---------------------------------------------------------------------------------------------------
#Función para dividir los menajes en fechas
def dividirFechas():
    global listaMensajes,listaFechas


    for i in listaMensajes: #Iteramos sobre los mensajes
        fecha=i.fecha #Obtenemos la fecha del mensaje
        repetido=False #Variable para verificar si la fecha está repetida

        #Verificación de que no esté repetido el valor
        for j in listaFechas: #Iteramos sobre las fechas
            if fecha==j.fecha: #Si la fecha ya está en la lista
                repetido=True #La fecha está repetida
        if repetido==False: #Si la fecha no está repetida

            #Se crea el objeto fecha
            fecha=poo.fecha(fecha,[]) 
            fecha.listaMensajes.append(i) #Se agrega el mansaje a la lista de la primera fecha
            listaFechas.append(fecha) #Agregamos la fecha a la lista de fechas
        else:
            for j in listaFechas: #Iteramos sobre las fechas
                if fecha==j.fecha: #Si la fecha ya está en la lista
                    j.listaMensajes.append(i) #Se agrega el mensaje a la fecha ya existente

    #Imprimimos las fechas para confirmar que lo haya hecho bien :)
    '''for i in listaFechas:
        print(i.listaMensajes)'''
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# Función para indentar el archivo (solo lo copié y lo pegué xd)
def indent(elem, level=0, hor='\t', ver='\n'): 
    i = ver + level * hor
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + hor
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1, hor, ver)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

#Función para crear el archivo de salida XML
def crearArchivoSalida():
    global listaMensajes, listaEmpresitas, listaPositivos, listaNegativos  
    
    ruta="data/salida.xml" #Ruta del archivo de salida
    raiz=ET.Element("lista_respuestas") #Creamos la raíz del archivo de salida
    for fechita in listaFechas: #Iteramos sobre las fechas
        respuesta=ET.SubElement(raiz,"respuesta") #Creamos la rama de respuesta
        fecha=ET.SubElement(respuesta,"fecha") #Creamos la rama fecha
        fecha.text=fechita.fecha #Agregamos la fecha a la rama fecha


        cuentaMensajes=0 #Contador de mensajes
        cuentaMensajesPositivos=0 #Contador de mensajes positivos
        cuentaMensajesNegativos=0 #Contador de mensajes negativos
        cuentaMensajesNeutros=0 #Contador de mensajes neutrales
        mensajesT=ET.SubElement(respuesta,"mensajes")

        #ciclo para crear la rama mensajes
        for mensaje in fechita.listaMensajes: #Creamos la rama mensaje
            cuentaMensajes+=1 #Sumamos al contador de mensajes
            if mensaje.positivos>mensaje.negativos: #Si el mensaje es positivo
                cuentaMensajesPositivos+=1 #Sumamos al contador de mensajes positivos
            elif mensaje.negativos>mensaje.positivos: #Si el mensaje es negativo
                cuentaMensajesNegativos+=1 #Sumamos al contador de mensajes negativos
            else: #Si el mensaje es neutral
                cuentaMensajesNeutros+=1 #Sumamos al contador de mensajes neutrales

        #Creo las partes de mensaje
        total=ET.SubElement(mensajesT,"total") #Creamos la rama total
        total.text=str(cuentaMensajes) #Agregamos el total de mensajes
        positivos=ET.SubElement(mensajesT,"positivos") #Creamos la rama positivos
        positivos.text=str(cuentaMensajesPositivos) #Agregamos el total de mensajes positivos
        negativos=ET.SubElement(mensajesT,"negativos") #Creamos la rama negativos
        negativos.text=str(cuentaMensajesNegativos) #Agregamos el total de mensajes negativos
        neutros=ET.SubElement(mensajesT,"neutros") #Creamos la rama neutros
        neutros.text=str(cuentaMensajesNeutros) #Agregamos el total de mensajes neutrales

#-------------------------------------------------------------------------------------------------------

        analisis=ET.SubElement(respuesta,"analisis") #Creamos la rama analisis
        #Ciclo para crear cada mensaje del análisis
        for emprecita in listaEmpresitas: #Iteramos sobre los mensajes
            empresa=ET.SubElement(analisis,"empresa",nombre=emprecita.nombre) #Creamos la rama empresa
            
            #Inicializamos los contadores
            cuentaMensajes=0 #Contador de mensajes
            cuentaMensajesPositivos=0 #Contador de mensajes positivos
            cuentaMensajesNegativos=0 #Contador de mensajes negativos
            cuentaMensajesNeutros=0 #Contador de mensajes neutrales

            #Ciclo para buscar los mensajes de cada empresa
            for mensajeL in listaMensajes: #Iteramos sobre los mensajes
                
                if (mensajeL.fecha==fechita.fecha): #Si la fecha del mensaje es igual a la fecha actual
                    for empresaMensaje in mensajeL.empresas: #Iteramos sobre las empresas de los mensajes

                        if empresaMensaje.nombre==emprecita.nombre: #Si la empresa del mensaje es igual a la empresa actual
                            
                            cuentaMensajes+=1 #Sumamos al contador de mensajes
                            if mensajeL.positivos>mensajeL.negativos: #Si el mensaje es positivo
                                cuentaMensajesPositivos+=1 #Sumamos al contador de mensajes positivos
                            elif mensajeL.negativos>mensajeL.positivos: #Si el mensaje es negativo
                                cuentaMensajesNegativos+=1 #Sumamos al contador de mensajes negativos
                            else: #Si el mensaje es neutral
                                cuentaMensajesNeutros+=1 #Sumamos al contador de mensajes neutrales
            
            #Coloco las partes de mensajes de cada empresa
            mensajesE=ET.SubElement(empresa,"mensajes") #Creamos la rama mensajes
            total=ET.SubElement(mensajesE,"total") #Creamos la rama total
            total.text=str(cuentaMensajes) #Agregamos el total de mensajes
            positivos=ET.SubElement(mensajesE,"positivos") #Creamos la rama positivos
            positivos.text=str(cuentaMensajesPositivos) #Agregamos el total de mensajes positivos
            negativos=ET.SubElement(mensajesE,"negativos") #Creamos la rama negativos
            negativos.text=str(cuentaMensajesNegativos) #Agregamos el total de mensajes negativos
            neutros=ET.SubElement(mensajesE,"neutros") #Creamos la rama neutros
            neutros.text=str(cuentaMensajesNeutros) #Agregamos el total de mensajes neutrales

            #Ciclo para crear la rama de servicios
            servicios=ET.SubElement(empresa,"servicios")
            for servicinho in emprecita.servicios: #Iteramos sobre los servicios
                servicio=ET.SubElement(servicios,"servicio", nombre=servicinho.nombre) #Creamos la rama del servicio respectivo
                mensajesS=ET.SubElement(servicio,"mensajes") #Creamos la rama mensajes

                cuentaPositivos=0 #Contador de palabras positivas
                cuentaNegativos=0 #Contador de palabras negativas
                cuentaNeutros=0 #Contador de palabras neutras
                cuentaTotal=0  #Contador de palabras totales
                for mensajeLL in listaMensajes: #Iteramos sobre los mensajes

                    if (mensajeLL.fecha==fechita.fecha): #Si la fecha del mensaje es igual a la fecha actual
                        for empresaMensajito in mensajeLL.empresas: #Iteramos sobre las empresas de los mensajes

                            if empresaMensajito.nombre==emprecita.nombre: #Si la empresa del mensaje es igual a la empresa actual
                                for servicioMensajito in empresaMensajito.servicios: #Iteramos sobre los servicios de las empresas

                                    if servicioMensajito.nombre==servicinho.nombre: #Si el servicio del mensaje es igual al servicio actual
                                        print(servicioMensajito.nombre)
                                        print(cuentaTotal)
                                        if (servicioMensajito.cantidad>0): #Si la cantidad de mensajes del servicio es mayor a 0
                                            cuentaTotal+=1 #Sumamos al contador de palabras totales
                                            if mensajeLL.positivos>mensajeLL.negativos: #Si el mensaje es positivo
                                                cuentaPositivos+=1 #Sumamos al contador de palabras positivas
                                            elif mensajeLL.negativos>mensajeLL.positivos: #Si el mensaje es negativo
                                                cuentaNegativos+=1 #Sumamos al contador de palabras negativas
                                            else: #Si el mensaje es neutral
                                                cuentaNeutros+=1

                #Creamos las ramas de los servicios
                total=ET.SubElement(mensajesS,"total")
                total.text=str(cuentaTotal)
                positivos=ET.SubElement(mensajesS,"positivos")
                positivos.text=str(cuentaPositivos)
                negativos=ET.SubElement(mensajesS,"negativos")
                negativos.text=str(cuentaNegativos)
                neutros=ET.SubElement(mensajesS,"neutros")
                neutros.text=str(cuentaNeutros)

    #Aquí escribo mi archivo XML de salida
    salida=ET.ElementTree(raiz) #Creamos el árbol de salida
    ET.dump(raiz) #Imprimimos el árbol de salida
    indent(raiz) #Indentamos el archivo

    with open(ruta,"wb") as doc:
        salida.write(doc,encoding="utf-8",xml_declaration=True)
#---------------------------------------------------------------------------------------------------
#Función para obtener una lista de las fechas disponibles
def obtenerFechas():
    global listaFechas
    lista=[] #Lista de fechas
    for i in listaFechas: #Iteramos sobre las fechas
        lista.append(i.fecha) #Agregamos la fecha a la lista de fechas
    return lista #Retornamos la lista de fechas

#Función para obtener empresas de una fecha
def obtenerEmpresas(fecha):
    global listaFechas
    for i in listaFechas: #Iteramos sobre las fechas
        if i.fecha==fecha: #Si la fecha es igual a la fecha actual
            empresas=[] #Lista de empresas
            for j in i.listaMensajes: #Iteramos sobre los mensajes
                for k in j.empresas: #Iteramos sobre las empresas de los mensajes
                    repetido=False #Variable para verificar si la empresa está repetida

                    #Verificación de que no esté repetido el valor
                    for l in empresas: #Iteramos sobre las empresas
                        if k.nombre==l: #Si la empresa ya está en la lista
                            repetido=True #La empresa está repetida
                    if repetido==False: #Si la empresa no está repetida
                        empresas.append(k.nombre) #Agregamos la empresa a la lista de empresas
            return empresas #Retornamos la lista de empresas


def obtenerTodoFecha(fecha): #Función para obtener los mensajes de una fecha
    global listaFechas
    for i in listaFechas: #Iteramos sobre las fechas
        if i.fecha==fecha: #Si la fecha es igual a la fecha actual

            cuentaMensajes=0 #Contador de mensajes
            cuentaMensajesPositivos=0 #Contador de mensajes positivos
            cuentaMensajesNegativos=0 #Contador de mensajes negativos
            cuentaMensajesNeutros=0 #Contador de mensajes neutrales

        #ciclo para crear la rama mensajes
            for mensaje in i.listaMensajes: #Creamos la rama mensaje
                cuentaMensajes+=1 #Sumamos al contador de mensajes
                if mensaje.positivos>mensaje.negativos: #Si el mensaje es positivo
                    cuentaMensajesPositivos+=1 #Sumamos al contador de mensajes positivos
                elif mensaje.negativos>mensaje.positivos: #Si el mensaje es negativo
                    cuentaMensajesNegativos+=1 #Sumamos al contador de mensajes negativos
                else: #Si el mensaje es neutral
                    cuentaMensajesNeutros+=1 #Sumamos al contador de mensajes neutrales
    valores=[cuentaMensajes,cuentaMensajesPositivos,cuentaMensajesNegativos,cuentaMensajesNeutros]

    return valores #Retornamos la lista de empresas




#Función para obtener los servicios de una empresa

#dsjfhcdfmlkghdslckgsdhlfkfdlscghkml,cnhdsfckhdkjhgcsdfcnsdfkgvnhdsfnhvkdshcgklsdfhgvnsdkjfnhskdj PROBANDO

#procesar()

'''for mensaje in listaMensajes:
    print(mensaje.mensaje)
    print(mensaje.lugar)
    print(mensaje.fecha)
    print(mensaje.hora)
    print(mensaje.usuario)
    print(mensaje.redSocial)
    print(mensaje.empresas)
    print(mensaje.negativos)
    print(mensaje.positivos)
    print("\n\n\n")'''

'''dividirFechas()

crearArchivoSalida()
print(obtenerFechas())
i=0
print("-------------------")
print(obtenerEmpresas("05/04/2022"))'''
'''for mensajes in listaMensajes:
    i=i+1
    print("Mensaje:" + str(i))
    for empresas in mensajes.empresas:
        print(empresas.nombre)
        for servicios in empresas.servicios:
            print(servicios.nombre)
            print(servicios.cantidad)
'''




