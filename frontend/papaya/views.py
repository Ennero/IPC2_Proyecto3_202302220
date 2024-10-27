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
        salida = response.json()["salida"] #Obtengo la respuesta de la API
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

        if request.POST.get("subir"): #Verifica si se envió el valor de 'subir'

            response = requests.get('http://127.0.0.1:5000/procesar') #Consulto a la API
            

            return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida,"mensaje":response.json()["mensaje"]})

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

            #print(valores,label)
            return render(request,'papaya/resumenPorFecha.html',{
                'fechita':fechita,'empresas':empresas,'data':data})

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
                'fechita':fechita,'empresas':empresas,'data':data})

    #Si no se envió un POST solicita las fecha
    response = requests.get('http://127.0.0.1:5000/resumenPorFecha') #Consulto a la API

    fechas = response.json()["fechas"]#Obtengo las fechas
    return render(request,"papaya/resumenPorFecha.html",{"fechas":fechas})

@csrf_exempt
def resumenPorRangoTipo(request):





    return render(request,"papaya/resumenPorRangoTipo.html")

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