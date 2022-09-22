from django.db import models

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    logo = models.TextField(default="/static/master/img/logo.png")
    contacto = models.CharField(max_length=100, default="Sin Contacto")
    direccion = models.CharField(max_length=100, default="")
    telefono = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=100, default="")
    rut = models.CharField(max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.nombre