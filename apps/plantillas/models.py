from django.db import models
from apps.empresas.models import Empresa

# Create your models here.
class TipoPlantilla(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Plantilla(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="plantillas_empresa")
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    tipo = models.ForeignKey(TipoPlantilla, on_delete=models.CASCADE, related_name="plantillas_tipo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)