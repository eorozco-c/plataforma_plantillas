from django.db import models
from apps.plantillas.models import TipoPlantilla

# Create your models here.
class Parametro(models.Model):
    nombre = models.CharField(max_length=50)
    abreviado = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=240, null=True, blank=True)
    tipo = models.ForeignKey(TipoPlantilla, on_delete=models.CASCADE, related_name="parametros_tipo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    