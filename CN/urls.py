"""cn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler400,handler404,handler403,handler500
import debug_toolbar

handler400 = 'CN.views.bad_request'
handler403 = 'CN.views.permission_denied'
handler404 = 'CN.views.page_not_found'
handler500 = 'CN.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.master.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('empresas/', include('apps.empresas.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('datos/', include('apps.datos.urls')),
    path('reportes/', include('apps.reportes.urls')),
    path('parametros/', include('apps.parametros.urls')),
    path('puntos_medicion/', include('apps.puntos_medicion.urls')),
    path('plantillas/', include('apps.plantillas.urls')),
    path('licencias/', include('apps.licencias.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)