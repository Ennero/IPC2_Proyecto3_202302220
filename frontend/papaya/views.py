from django.shortcuts import render

# Create your views here.

def Paula(request):
    return render(request,"papaya/subir.html")

def peticiones(request):
    return render(request,"papaya/peticiones.html")

def home(request):
    return render(request,"papaya/home.html")

def info(request):
    return render(request,"papaya/info.html")