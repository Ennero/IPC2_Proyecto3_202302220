import xml.etree.ElementTree as ET



def crearArchivo(entrada): #Función que crea el archivo de entrada
    archivo = open("data/archivo.xml", "w", encoding="utf-8")
    archivo.write(entrada) #Escribimos el contenido del archivo
    archivo.close() #Cerramos el archivo
    return "Archivo creado con éxito" #Retornamos un mensaje de éxito





def crearSalida(entrada): #Función que crea el archivo de salida
    try:
        arbol = ET.parse("data/archivo.xml") #Creamos el arbol
        ramas=arbol.getroot() #Obtenemos la raíz del arbol
        for i in ramas.iter('diccionario'):
            for j in i.iter('sentimientos_positivos'):
                






    except Exception as e:
        return "Error al abrir el archivo", e #Retornamos un mensaje de error si no se pudo abrir el archivo