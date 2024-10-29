from django.shortcuts import render,redirect
import requests
from django.views.decorators.csrf import csrf_exempt


#Declaro algunas variables globales
entrada = ""
salida = ""
fechita = ""
empresas=[]

#para la empresa específica
empresa=""

#Variables temporales para el rango
entradaR=""
salidaR=""
fecha1=""
fecha2=""
empresasR=[]
fechas2=[]


#Esta es para la página de subir
@csrf_exempt
def Paula(request):
    global entrada,salida
    if request.method == "POST":

        archivo = request.FILES["archivo"] #Obtengo el archivo

        response = requests.post('http://127.0.0.1:5000/subir', files={'archivo': (archivo.name,archivo,archivo.content_type)}) #Envio el archivo a la API
        print("---------------------------------------------------")

        entrada = archivo.read().decode("utf-8")

        print(entrada)
        entrada = response.json()["contenido"] #Obtengo la respuesta de con el mismo contenido que se envió xd (aquí consumiendo recursos a lo loco)
        print("---------------------------------------------------")    
        #print(salida) #Imprimo la respuesta de la API
        #print(entrada)
        subido=True 
        return render(request,"papaya/subir.html",{"subido": subido}) #Redirijo a la página de peticiones

    #El predefinido siempres será get
    return render(request,"papaya/subir.html")

#Esta es para la página de peticiones ( la principal )
@csrf_exempt
def peticiones(request):
    global entrada,salida
    if request.method == "POST": #Verifica si se envió un POST

        if request.POST.get("reset"): #Verifica si se envió el valor de 'reset'

            #Borrará TODo
            salida = "" #Borro la salida
            entrada = "" #Borro la entrada
            print("Reset") #Imprimo que se hizo un reset

            #Envío el archivo reset (basicamente solo indico que se realice el reset)
            response = requests.post('http://127.0.0.1:5000/reset', files={'archivo': "reset"}) #Envio el archivo a la API
            return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida,"mensaje":response.json()["mensaje"]})

        if request.POST.get("enviar"): #Verifica si se envió el valor de 'subir'

            response = requests.get('http://127.0.0.1:5000/procesar') #Consulto a la API

            salida = response.json()["salida"] #Obtengo la respuesta de la API            
            return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida,"mensaje":response.json()["mensaje"]})

        if request.POST.get("pdf"):
            print("PDF")
            response = requests.get('http://127.0.0.1:5000/pdf') #(basicamente solo indico que se realice el pdf)

            return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida, "mensaje":response.json()["mensaje"]})


    #El predefinido siempres será get
    return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida})

#Esta es para la página de consulta en la base de datos
@csrf_exempt
def consulta(request):
    salida = ""
    response = requests.get('http://127.0.0.1:5000/consulta') #Consulto a la API

    salida = response.json()["salida"] #Obtengo la respuesta de la API

    print(salida)
    return render(request,"papaya/consulta.html",{"salida":salida})

#Función para el resumen por fecha
@csrf_exempt
def resumenPorFecha(request):
    global fechita,empresas,empresa

    if request.method == "POST": #Si se envió un POST

        #Si lo que se envió fue la fecha
        if request.POST.get("fecha"):

            fechita = request.POST.get("fecha") #Obtengo la fecha

            #Envio la fecha a la API
            response = requests.post("http://127.0.0.1:5000/resumenPorFecha",data={'fechita': fechita}) #Envio la fecha a la API

            empresas = response.json()["empresas"] #Obtengo la respuesta de la API

            #Retorno la plantilla con la fecha y las empresas
            return render(request,"papaya/resumenPorFecha.html",{"fechita":fechita,"empresas":empresas})
        
        #Si lo que se envió fue la señal de que se quiere ver todo
        if request.POST.get("todo"):

            #Envio la fecha a la API
            response = requests.post("http://127.0.0.1:5000/graficaTodo",data={'fechita': fechita}) #Envio la fecha a la API
            data=response.json()["todo"] #Obtengo la respuesta de la API

            print(data)
            todo=request.POST.get("todo") #Obtengo la señal de que se quiere ver todo
            #print(valores,label)
            return render(request,'papaya/resumenPorFecha.html',{
                'fechita':fechita,'empresas':empresas,'data':data,'todo':todo})

        #Si lo que se envió fue la señal de que se quiere ver una empresa específica
        if request.POST.get("empresa"):

            print("----------------------------------")
            empresa = request.POST.get("empresa") #Obtengo la empresa

            #Envio la fecha y la empresa que se quiere graficar a la api
            response=requests.post("http://127.0.0.1:5000/graficaEmpresa",data={'fechita': fechita, 'empresa':empresa}) #Envio la fecha a la API

            #Recibo la respuesta de la api con la lista de los valores
            data=response.json()["todo"]
            print(data)

            #Retorno la plantilla con la fecha, las empresas y los valores de la empresa
            return render(request,'papaya/resumenPorFecha.html',{
                'fechita':fechita,'empresas':empresas,'data':data,'empresi':empresa})

    #Si no se envió un POST solicita las fecha
    response = requests.get('http://127.0.0.1:5000/resumenPorFecha') #Consulto a la API

    fechas = response.json()["fechas"]#Obtengo las fechas
    return render(request,"papaya/resumenPorFecha.html",{"fechas":fechas})

#Función para el resumen por rango de fecha
@csrf_exempt
def resumenPorRangoTipo(request):
    global entradaR,salidaR,fecha2,fecha1,empresasR,fechas2

    if request.method == "POST": #Si se envió un POST
        #Si lo que se envió fue la fecha
        if request.POST.get("fecha1"):
            fecha1 = request.POST.get("fecha1") #Obtengo la fecha1

            #Envio la fecha a la API
            response = requests.post('http://127.0.0.1:5000/fecha1',data={'fecha1': fecha1})

            fechas2 = response.json()["fechas2"] #Obtengo la fecha2 de la API

            #print(fecha1,fechas2)

            if len(fechas2)==0:
                return render(request,"papaya/resumenPorRangoTipo.html",{"fecha1":fecha1,"aviso":"No hay fechas disponibles"})

            #Retorno la plantilla con la fecha y las fechas2
            return render(request,"papaya/resumenPorRangoTipo.html",{"fecha1":fecha1,"fechas2":fechas2})
        
        #Si lo que se envió fue la segunda fecha
        if request.POST.get("fecha2"):
            fecha2 = request.POST.get("fecha2") #Obtengo la fecha2

            #Envio la fecha a la API
            response = requests.post('http://127.0.0.1:5000/fecha2',data={'fecha2': fecha2,'fecha1':fecha1})

            empresasR = response.json()["empresasR"] #Obtengo las empresas de la API

            print(fecha1,fecha2,empresasR)
            #Retorno la plantilla con la fecha1, la fecha2 y las empresas
            return render(request,"papaya/resumenPorRangoTipo.html",{"fecha1":fecha1,"fecha2":fecha2,"empresasR":empresasR})

        #Si lo que se envió fue la señal de que se quiere ver todo
        if request.POST.get("todo"):
            todo = request.POST.get("todo") #Obtengo la señal de que se quiere ver todo
            #Envio la fecha a la API
            response = requests.post("http://127.0.0.1:5000/graficaTodoEnRango",data={'fecha1': fecha1, 'fecha2':fecha2}) #Envio la fecha a la API
            data=response.json()["todo"] #Obtengo la respuesta de la API
            fechonas=response.json()["fechonas"] #Obtengo la lista con las fechas
            dupla=list(zip(fechonas,data)) #Creo una dupla con ambas
            print("Esto llegó al frontend",dupla) #Imprimo la dupla
            return render(request,'papaya/resumenPorRangoTipo.html',{'fecha1':fecha1,'fecha2':fecha2,'data':dupla,'todo':todo})

        #Si lo que se envió fue la señal de que se quiere ver una empresa específica
        if request.POST.get("empresa"):
            
            empresa = request.POST.get("empresa") #Obtengo la empresa
            #Verificar lo nombres de lo que coloque en empresaR
            response=requests.post("http://127.0.0.1:5000/graficaEmpresaEnRango1",data={'fecha1': fecha1, 'fecha2':fecha2,'empresa':empresa})
            data=response.json()["todo"] #Tomo la lista de los valores
            fechonas=response.json()["fechonas"] #Tomo la lista de las fechas
            dupla=list(zip(fechonas,data)) #Creo una dupla con ambas
            
            #Lo que obtengo de la dupla
            print("Lo que llegó al frontend",dupla)

            #Lo mismo de siempre pero añadiendo la dupla
            return render(request,'papaya/resumenPorRangoTipo.html',{'fecha1':fecha1,'fecha2':fecha2,'empresa':empresa,'data':dupla})




    #Si no se envió un POST solicita las fechas [PARECE ERRROR PERO NO LO ES XD]
    response = requests.get('http://127.0.0.1:5000/resumenPorFecha') #Consulto a la API

    fechas = response.json()["fechas"]#Obtengo las fechas

    #print(fechas)
    return render(request,"papaya/resumenPorRangoTipo.html",{"fechas":fechas})



#Esta es la página para realizar al prueba de mensaje
@csrf_exempt
def pruebaMensaje(request):

    if request.method == "POST":
        archivo = request.FILES["archivo"] #Obtengo el archivo

        print("---------------------------------------------------")
        #contenido = archivo.read().decode("utf-8")

        #Envio el archivo a la API
        response = requests.post('http://127.0.0.1:5000/prueba', files={'archivo': (archivo.name,archivo,archivo.content_type)}) #Envio el archivo a la API

        salidita=response.json()["mensaje"] #Obtengo la respuesta de la API

        return render(request,"papaya/pruebaMensaje.html",{"salidita":salidita})

    return render(request,"papaya/pruebaMensaje.html")

#Esta es para el resumen por rango de fecha




#Esta es solo para redirigirmela a la página de peticiones
@csrf_exempt
def home(request):
    return redirect("peticiones")

#Esto es para la pagina de info
@csrf_exempt
def info(request):
    return render(request,"papaya/info.html")