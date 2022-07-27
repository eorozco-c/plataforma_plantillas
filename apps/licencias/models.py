from django.db import models

# Create your models here.
class Licencia(models.Model):
    uuid = models.CharField(max_length=255, unique=True)
    empresas = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



