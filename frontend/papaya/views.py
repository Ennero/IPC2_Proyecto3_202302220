from django.shortcuts import render,redirect
import requests
from django.views.decorators.csrf import csrf_exempt


#Declaro algunas variables globales
entrada = ""
salida = ""

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
        entrada = response.json()["contenido"]
        print("---------------------------------------------------")    
        #print(salida) #Imprimo la respuesta de la API
        print(entrada)
        subido=True
        return render(request,"papaya/subir.html",{"subido": subido}) #Redirijo a la página de peticiones

    return render(request,"papaya/subir.html")

#Esta es para la página de peticiones ( la principal )
@csrf_exempt
def peticiones(request):
    global entrada,salida

    if request.method == "POST": #Verifica si se envió un POST

        if request.POST.get("reset"): #Verifica si se envió el valor de 'reset'

            #Borrará TODo
            salida = ""
            entrada = ""
            print("Reset")
            response = requests.post('http://127.0.0.1:5000/reset', files={'archivo': "reset"}) #Envio el archivo a la API
            return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida,"mensaje":response.json()["mensaje"]})

    #El predefinido siempres será get
    return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida})

@csrf_exempt
def consulta(request):
    salida = ""
    response = requests.get('http://127.0.0.1:5000/consulta') #Consulto a la API

    salida = response.json()["salida"] #Obtengo la respuesta de la API

    print(salida)
    return render(request,"papaya/consulta.html",{"salida":salida})

@csrf_exempt
def resumenPorFecha(request):

    if request.method == "POST":

        #Si lo que se envió fue la fecha
        if request.POST.get("fecha"):

            fechita = request.POST.get("fecha")
            response = requests.post("http://127.0.0.1:5000/resumenPorFecha",data={'fechita': fechita}) #Envio la fecha a la API

            #print(fechita)

            empresas = response.json()["empresas"] #Obtengo la respuesta de la API
            return render(request,"papaya/resumenPorFecha.html",{"fechita":fechita,"empresas":empresas})
        
        if request.POST.get("empresa"):

            tipo = request.POST.get("empresa")

    response = requests.get('http://127.0.0.1:5000/resumenPorFecha') #Consulto a la API

    fechas = response.json()["fechas"]
    return render(request,"papaya/resumenPorFecha.html",{"fechas":fechas})

@csrf_exempt
def resumenPorTipo(request):
    return render(request,"papaya/resumenPorTipo.html")

@csrf_exempt
def pruebaMensaje(request):
    return render(request,"papaya/pruebaMensaje.html")


#Esta es solo para redirigirmela a la página de peticiones
@csrf_exempt
def home(request):
    return redirect("peticiones")

#Esto es para la pagina de info
@csrf_exempt
def info(request):
    return render(request,"papaya/info.html")