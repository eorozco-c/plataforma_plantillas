from django.urls import  path
from . import views

app_name = "licencias"

urlpatterns = [
    path('', views.ListLicencia.as_view(), name='index'),
    path('generar_licencia/', views.generar_licencia, name='generar_licencia'),
    path('import/', views.licenciaImport, name='import'),
]