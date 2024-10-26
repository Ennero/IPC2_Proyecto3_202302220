from django.contrib import admin
from django.urls import path, include
from papaya import views

urlpatterns = [

    path("peticiones", views.peticiones, name="peticiones"),
    path("subir", views.Paula, name="Paula"),
    path("", views.home, name="home"),
    path("info", views.info, name="info"),
    path("consulta", views.consulta, name="consulta"),
    path("resumenPorFecha", views.resumenPorFecha, name="resumenPorFecha"),
    path("resumenPorRangoTipo", views.resumenPorTipo, name="resumenPorTipo"),
    path("pruebaMensaje", views.pruebaMensaje, name="pruebaMensaje"),

]