from django.db import models
from django.db.models import Model

# Create your models here.
class Origen(models.Model):
    nombre_origen = models.TextField(max_length=100)
    
    def __str__(self):
        return str(self.nombre_origen)

class Tipo(models.Model):
    nombre_tipo = models.TextField(max_length=100)
    
    def __str__(self):
        return str(self.nombre_tipo)

class Juguete(models.Model):
    codigo = models.TextField(unique = True, max_length=50)
    nombre = models.TextField(max_length=50)
    precio = models.IntegerField(null=False)
    disponibilidad = models.TextField(max_length=2)
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    marca = models.TextField(max_length=50)

class Usuario(models.Model):
    nombre_usuario = models.TextField(max_length=15)
    password_usuario = models.TextField(max_length=20)
    
    def __str__(self):
        return str(self.nombre_usuario)

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion_historial = models.TextField(max_length=200)
    tabla_historial = models.TextField(max_length=100)
    fecha_hora_historial = models.DateTimeField()
    
    def __str__(self):
        return str(self.accion_historial)
    
