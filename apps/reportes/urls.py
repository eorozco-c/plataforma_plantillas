from django.urls import  path
from . import views

app_name = "reportes"

urlpatterns = [
    path('', views.index, name="index"),
    path('get_form/', views.get_form, name="get_form"),
    path('get_datos/', views.get_datos, name="get_datos"),
]