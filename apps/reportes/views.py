from django.contrib import messages
from django.db.models.aggregates import Sum
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from apps.datos.models import Datos
from apps.plantillas.models import Plantilla
from apps.puntos_medicion.models import PuntoMedicion
from apps.parametros.models import Parametro
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
    plantillas = Plantilla.objects.filter(empresa=request.user.empresa, activo=True)
    context = {
        'appname' : "reportes",
        'fecha_ini' : fecha_ini,
        'fecha_fin' : fecha_fin,
        'plantillas' : plantillas,
    }
    return render(request, "reportes/formulario_datos.html", context)

@login_required(login_url='/')
def get_form(request):
    if request.method == "GET":
        pk_plantilla = request.GET.get('plantilla')
        plantilla = Plantilla.objects.get(pk=pk_plantilla)
        puntos = PuntoMedicion.objects.filter(tipo=plantilla.tipo, empresa=request.user.empresa)
        parametros = Parametro.objects.filter(tipo=plantilla.tipo)
        datos_json = {}
        puntos_list = []
        parametros_list = []
        for punto in puntos:
            puntos_list.append({
                'nombre' : punto.nombre,
                'id' : punto.id,
            })
        for parametro in parametros:
            parametros_list.append({
                'nombre' : parametro.nombre,
                'id' : parametro.id,
            })
        datos_json['puntos'] = puntos_list
        datos_json['parametros'] = parametros_list

        return JsonResponse(datos_json, safe=False)
    return JsonResponse({})

@login_required(login_url='/')
def get_datos(request):
    if request.method == "POST":
        datos_json = {}
        fecha_ini = request.POST.get('fecha_ini')
        fecha_fin = request.POST.get('fecha_fin')
        plantilla = request.POST.get('plantilla')
        puntos = request.POST.getlist('puntos')
        parametros = request.POST.getlist('parametros')
        plantilla = Plantilla.objects.get(pk=plantilla)
        parametros_list = []
        puntos_list = []
        for p in puntos:
            puntos_list.append(PuntoMedicion.objects.get(pk=p))
        for parametro in parametros:
            parametro = Parametro.objects.get(pk=parametro)
            parametros_list.append(parametro)
            datos_json[parametro.id] = []
            for punto in puntos:

                punto = PuntoMedicion.objects.get(pk=punto)
                datos = Datos.objects.filter(punto_medicion=punto, parametro=parametro, fecha__range=[fecha_ini, fecha_fin],plantilla=plantilla)
                #order by fecha asc
                datos = datos.order_by('fecha')
                datos_json[parametro.id].append({
                    'id' : punto.id,
                    'punto' : punto.nombre,
                    'data' : [],
                })
                #append to punto.nombre  dato.fecha and dato.valor to datos_json
                for dato in datos:
                    datos_json[parametro.id][-1]['data'].append({
                        'fecha' : dato.fecha.strftime('%Y-%m-%d'),
                        'valor' : dato.valor,
                    })
        datos_json = json.dumps(datos_json)
        context = {
            'appname' : "reportes",
            'datos_json' : datos_json,
            'puntos' : puntos_list,
            'parametros' : parametros_list,
        }
        return render(request, "reportes/grafico_datos.html", context)
    return redirect('datos:index')