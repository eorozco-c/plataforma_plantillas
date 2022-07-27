from django.urls import  path
from . import views

app_name = "datos"

urlpatterns = [
    path('<int:pk_plantilla>/', views.ingreso_datos, name="ingreso_datos"),
    path('generar_informe/<int:pk_plantilla>/', views.generar_informe, name="generar_informe"),
    path('get_datos/<int:pk_plantilla>/', views.get_datos, name="get_datos"),
]