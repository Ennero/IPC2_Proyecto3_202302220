


#Clase para cada una de las empresas
class Empresa():
    def __init__(self, nombre, servicios):
        self.nombre = nombre
        self.servicios=servicios

#Clase para cada uno de los mensajes
class Mensaje():
    def __init__(self, mensaje, lugar,fecha,hora,usuario, redSocial, empresas,negativos, positivos):
        self.mensaje=mensaje
        self.lugar=lugar
        self.fecha=fecha
        self.hora=hora
        self.usuario=usuario
        self.redSocial=redSocial
        self.empresas=empresas
        self.negativos=negativos
        self.positivos=positivos

#Clase para cada uno de los servicios
class Servicio():
    def __init__(self, nombre, alias):
        self.nombre = nombre
        self.alias=alias