from django.db import models

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    logo = models.TextField(default="/static/master/img/logo.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.nombre