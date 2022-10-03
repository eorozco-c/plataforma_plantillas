from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.empresas.models import Empresa
from apps.usuarios.models import Usuario

import psutil
# Create your views here.
def index(request):
    if request.method == "GET":
        if Empresa.objects.count() == 0:
            return redirect("empresas:crear")
        if Usuario.objects.count() == 0:
            return redirect("usuarios:registrar")
        if request.user.is_authenticated:
            return redirect("plantillas:index")
    return redirect("usuarios:login")

@login_required(login_url='/')
def menu(request):
    return redirect("plantillas:index")
    ramUsage = round(psutil.virtual_memory().percent)
    ramAvailable = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
    hdd = psutil.disk_usage('/')
    hddUsage = round(hdd.used / (2**30))
    hddAvailable = round(hdd.free / (2**30))
    usuarios = Usuario.objects.filter(empresa=request.user.empresa).count()
    context = {
        'appname' : "dashboard",
        'ramUsage' : ramUsage,
        'ramAvailable' : ramAvailable,
        'hddUsage' : hddUsage,
        'hddAvailable' : hddAvailable,
        'usuarios' : usuarios,
    }
    return render(request, "menu.html", context)

@login_required(login_url='/')
def cpu(request):
    cpu = psutil.cpu_percent(interval=None)
    context = {
        'cpu' : cpu,
    }
    return JsonResponse(context)