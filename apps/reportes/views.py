from django.contrib import messages
from django.db.models.aggregates import Sum
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.datos.models import Datos
import datetime,json


# Create your views here.
@login_required(login_url='/')
def index(request):
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')
    if not fecha_ini or not fecha_fin:
        date_ini = datetime.date.today()
        date_fin = datetime.date.today()
    else:
        date_ini = datetime.datetime.strptime(fecha_ini, '%Y-%m-%d').date()
        date_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    if date_ini > date_fin:
        messages.error(request, 'La fecha inicial no puede ser mayor a la fecha final.')
        return redirect('datos:index')
    #send values 1,2,3 by fecha between date_ini and date_fin and empresa = request.user.empresa
    datos = Datos.objects.filter(fecha__range=[date_ini, date_fin]).filter(empresa=request.user.empresa).aggregate(valor1=Sum('valor1'), valor2=Sum('valor2'), valor3=Sum('valor3'))

    #add fecha_ini and fecha_fin to datos with format %Y-%m-%d
    datos['fecha_ini'] = date_ini.strftime('%Y-%m-%d')
    datos['fecha_fin'] = date_fin.strftime('%Y-%m-%d')    
    datos = json.dumps(datos)
    context = {
        'appname' : "reportes",
        'datos' : datos,
        'fecha_ini' : fecha_ini,
        'fecha_fin' : fecha_fin,
    }
    return render(request, "reportes/grafico_datos.html", context)
