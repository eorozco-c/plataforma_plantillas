from django.db import models
from apps.empresas.models import Empresa
from apps.plantillas.models import TipoPlantilla

# Create your models here.

class PuntoMedicion(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="puntos_medicion_empresa")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    activo = models.BooleanField(default=True)
    tipo = models.ForeignKey(TipoPlantilla, on_delete=models.CASCADE, related_name="puntos_medicion_tipo")
        
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)
