from django.db import models
from apps.parametros.models import Parametro
from apps.puntos_medicion.models import PuntoMedicion
from apps.plantillas.models import Plantilla
from apps.usuarios.models import Usuario

# Create your models here.
class Datos(models.Model):
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE)
    punto_medicion = models.ForeignKey(PuntoMedicion, on_delete=models.CASCADE)
    parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.FloatField(null=True, blank=True)
    fecha = models.DateField()
    updated = models.DateTimeField(auto_now=True)

class NotasDatos(models.Model):
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE)
    fecha = models.DateField()
    nota = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    