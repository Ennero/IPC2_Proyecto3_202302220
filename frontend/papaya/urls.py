from django.contrib import admin
from django.urls import path, include
from papaya import views

urlpatterns = {

    path("peticiones", views.peticiones, name="peticiones"),
    path("subir", views.Paula, name="Paula"),
    path("", views.home, name="home"),
    path("info", views.info, name="info"),
    

}