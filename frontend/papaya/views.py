from django.shortcuts import render,redirect
import requests
from django.views.decorators.csrf import csrf_exempt


#Declaro algunas variables globales
entrada = ""
salida = ""
subido=False

# Create your views here.
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

@csrf_exempt
def peticiones(request):
    global entrada,salida
    print (entrada)
    #print (salida)

    return render(request,"papaya/peticiones.html",{"entrada":entrada,"salida":salida})

@csrf_exempt
def home(request):
    return render(request,"papaya/home.html")

@csrf_exempt
def info(request):
    return render(request,"papaya/info.html")