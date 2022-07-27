from django.urls import  path
from . import views

app_name = "empresas"

urlpatterns = [
    path('', views.ListEmpresas.as_view(), name="index"),
    path('crear', views.CrearEmpresa.as_view(), name="crear"),
    path('editar/<int:pk>', views.EditEmpresa.as_view(), name="editar"),
    path('predestroy/<int:pk>',views.predestroy, name="predestroy"),
    path('destroy/<int:pk>',views.destroy, name="destroy"),
    # path('cargaLogo/<int:pk>',views.CargaLogo, name="cargaLogo"),
    path('cambiar-empresa/<int:pk>',views.cambiarEmpresa, name="cambiarEmpresa"),
]