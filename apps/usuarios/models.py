from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.empresas.models import Empresa

class Usuario(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    empresa = models.ForeignKey(Empresa, related_name="usuario_empresa", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        for field_name in ['first_name','last_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Usuario, self).save(*args, **kwargs)