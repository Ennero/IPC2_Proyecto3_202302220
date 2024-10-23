from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def Paula(request):
    if request.method == "POST":
        archivo = request.FILES["archivo"] #Obtengo el archivo

        response = requests.post('http://127.0.0.1:5000/subir', files={'archivo': (archivo.name,archivo,archivo.content_type)}) #Envio el archivo a la API

        print(response.json()) #Imprimo la respuesta de la API

        
        return render(request,"papaya/subir.html")




    return render(request,"papaya/subir.html")

@csrf_exempt
def peticiones(request):
    return render(request,"papaya/peticiones.html")

@csrf_exempt
def home(request):
    return render(request,"papaya/home.html")

@csrf_exempt
def info(request):
    return render(request,"papaya/info.html")