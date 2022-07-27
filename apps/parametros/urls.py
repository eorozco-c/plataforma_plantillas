from django.urls import  path
from . import views

app_name = "parametros"

urlpatterns = [
    path('', views.ListParametros.as_view(), name="index"),
    path('agregar/', views.CreateParametros.as_view(), name="agregar"),
    path('editar/<int:pk>/', views.EditParametros.as_view(), name="editar"),
    path('predestroy/<int:pk>/', views.predestroy, name="predestroy"),
    path('destroy/<int:pk>/', views.destroy, name="destroy"),
]