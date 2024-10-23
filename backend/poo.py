class Diccionario():
    def __init__(self, sentimientos,nombre,servicios):
        self.diccionario = {}
    
    def agregar(self, key, value):
        self.diccionario[key] = value
    
    def obtener(self, key):
        return self.diccionario[key]