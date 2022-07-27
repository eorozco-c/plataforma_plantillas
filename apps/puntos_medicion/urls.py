from django.urls import  path
from . import views

app_name = "puntos_medicion"

urlpatterns = [
    path('', views.ListPuntoMedicion.as_view(), name="index"),
    path('agregar/', views.CreatePuntoMedicion.as_view(), name="agregar"),
    path('editar/<int:pk>/', views.EditPuntoMedicion.as_view(), name="editar"),
    path('predestroy/<int:pk>/', views.predestroy, name="predestroy"),
    path('destroy/<int:pk>/', views.destroy, name="destroy"),
]