from django.urls import  path
from . import views

app_name = "datos"

urlpatterns = [
    path('<int:pk_plantilla>/<str:get_fecha>', views.ingreso_datos, name="ingreso_datos"),
    path('generar_informe/<int:pk_plantilla>/', views.generar_informe, name="generar_informe"),
    path('get_datos/<int:pk_plantilla>/', views.get_datos, name="get_datos"),
    path('agregar_nota/<int:pk_plantilla>/', views.agregar_nota, name="agregar_nota"),
    path('borrar_nota/<int:pk_nota>/', views.borrar_nota, name="borrar_nota"),
    path('borrar_fecha/<int:pk_plantilla>/', views.borrar_fecha, name="borrar_fecha"),
]