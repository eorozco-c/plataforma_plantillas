from django.urls import  path
from . import views

app_name = "plantillas"

urlpatterns = [
    path('', views.ListPlantillas.as_view(), name="index"),
    path('agregar/', views.CreatePlantilla.as_view(), name="agregar"),
    path('editar/<int:pk>/', views.EditPlantilla.as_view(), name="editar"),
    path('tipos_plantillas/', views.ListTipoPlantilla.as_view(), name="tipos_plantillas"),
    path('tipos_plantillas/agregar/', views.CreateTipoPlantilla.as_view(), name="agregar_tipo_plantilla"),
    path('tipos_plantillas/editar/<int:pk>/', views.EditTipoPlantilla.as_view(), name="editar_tipo_plantilla"),
    path('predestroy_tipo_plantilla/<int:pk>/', views.predestroy_tipo_plantilla, name="predestroy_tipo_plantilla"),
    path('destroy_tipo_plantilla/<int:pk>/', views.destroy_tipo_plantilla, name="destroy_tipo_plantilla"),

]