from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Datos
from apps.plantillas.models import Plantilla
from apps.parametros.models import Parametro
from apps.puntos_medicion.models import PuntoMedicion
from datetime import datetime
from apps.utils import html_to_pdf
from django.http import HttpResponse,JsonResponse
from django.template.loader import render_to_string
import matplotlib.pyplot as plt
import os,json

##############################################################################
@login_required(login_url='/')
def get_datos(request, pk_plantilla):
    """
    Obtiene los datos de una plantilla y los devuelve en formato JSON.
    """
    fecha = request.GET.get('fecha')
    plantilla = Plantilla.objects.get(pk=pk_plantilla)
    datos = Datos.objects.filter(plantilla=plantilla, fecha=fecha)
    datos_json = []
    for dato in datos:
        datos_json.append({
            'id': dato.id,
            'fecha': dato.fecha.strftime('%Y-%m-%d'),
            'valor': dato.valor,
            'punto_medicion': dato.punto_medicion.id,
            'parametro': dato.parametro.id,
            'usuario': dato.usuario.username,
        })
    return JsonResponse(datos_json, safe=False)


# Create your views here.
@login_required(login_url="/")
def ingreso_datos(request, pk_plantilla):
    if request.method == "GET":
        plantilla = Plantilla.objects.get(id=pk_plantilla)
        parametros = Parametro.objects.filter(tipo=plantilla.tipo)
        puntos_medicion = PuntoMedicion.objects.filter(empresa=request.user.empresa,tipo=plantilla.tipo)
        datos = Datos.objects.filter(fecha=datetime.now().date(), plantilla=plantilla)
        fechas_existentes = Datos.objects.filter(plantilla=plantilla).values('fecha').distinct().order_by('fecha')
        context = {
            'plantilla': plantilla,
            'parametros': parametros,
            'puntos_medicion': puntos_medicion,
            'datos': datos,
            'appname': 'Ingreso de datos',
            'fecha' : datetime.now().date().strftime('%Y-%m-%d'),
            'fechas_existentes': fechas_existentes,
        }
        return render(request, "datos/ingreso_datos.html", context)
    elif request.method == "POST":
        plantilla = Plantilla.objects.get(id=pk_plantilla)
        #request.post csrf_token + punto_medicion.id_parametro.id_parametro destructured
        fecha_dato = request.POST['fecha']
        for values in request.POST:
            #skip ['csrfmiddlewaretoken'] and ['']
            if 'csrfmiddlewaretoken' not in values and 'fecha' not in values:
                #separate id_parametro and id_punto_medicion by underscore
                list = values.split("_")
                id_punto_medicion = list[0]
                id_parametro  = list[1]
                # print(id_punto_medicion, id_parametro)
                #get id_punto_medicion and id_parametro
                punto_medicion = PuntoMedicion.objects.get(id=id_punto_medicion)
                parametro = Parametro.objects.get(id=id_parametro)
                #get value 
                valor = request.POST[str(punto_medicion.id) + "_" + str(parametro.id)]
                if valor == "":
                    valor = 0
                #if valor format is 20,0 then convert to float
                try:
                    if valor.count(",") == 1:
                        valor = valor.replace(",", ".")
                        valor = float(valor)
                except:
                    pass
                #update or create datos if exist data with date and plantilla
                try:
                    datos = Datos.objects.get(fecha=fecha_dato, plantilla=plantilla, punto_medicion=punto_medicion, parametro=parametro)
                except Datos.DoesNotExist:
                    datos = Datos.objects.create(punto_medicion=punto_medicion, parametro=parametro, valor=valor, plantilla=plantilla, usuario=request.user, fecha=fecha_dato)
                #if valor of datos is equal to valor then do nothing, else update datos and user
                if float(datos.valor) == valor:
                    pass
                else:
                    datos.valor = valor
                    datos.usuario = request.user
                    datos.save()
        messages.success(request, "Datos ingresados correctamente")            
        return redirect('datos:ingreso_datos', pk_plantilla=plantilla.id)
    else:
        return redirect('datos:ingreso_datos', pk_plantilla=plantilla.id)

@login_required(login_url="/")
def generar_informe(request, pk_plantilla):
    if request.method == "GET":
        plantilla = Plantilla.objects.get(id=pk_plantilla)
        puntos = PuntoMedicion.objects.filter(tipo=plantilla.tipo, empresa=request.user.empresa)
        parametros = Parametro.objects.filter(tipo=plantilla.tipo)
        #obtain group by fecha, parametros and puntos of datos of plantilla
        fechas_existentes = Datos.objects.filter(plantilla=plantilla).values('fecha').distinct().order_by('fecha')
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
        #convert all datos to float
        context = {
            'plantilla': plantilla,
            'appname': 'Generar informe',
            'puntos': puntos_list,
            'parametros': parametros_list,
            'fechas_existentes': fechas_existentes,
        }
        return render(request, "datos/generar_informe.html", context)
    elif request.method == "POST":
        fecha_ini_tabla = request.POST['fecha_ini_tabla']
        fecha_ini = request.POST['fecha_ini']
        fecha_fin = request.POST['fecha_fin']
        plantilla = Plantilla.objects.get(id=pk_plantilla)
        puntos_form = request.POST.getlist('puntos')
        parametros_form = request.POST.getlist('parametros')
        if plantilla.tipo.nombre == "caldera":
            #obtain all datos with plantilla
            datos = Datos.objects.filter(plantilla=plantilla,fecha=fecha_ini_tabla)
            if datos.count() == 0:
                messages.success(request, 'No hay datos para la fecha seleccionada.',extra_tags='danger')
                return redirect('datos:generar_informe', pk_plantilla=plantilla.id)
            json_data = []
            #obtain all valores from datos when parametro contains "conductividad"
            conductividad = datos.filter(parametro__nombre__icontains="conductividad")
            #count all puntos_medicion from conductividad when nombre contains "caldera"
            calderas = conductividad.filter(punto_medicion__nombre__icontains="caldera")
            alimentacion = conductividad.get(punto_medicion__nombre__icontains="alimentacion")
            factor_conductividad = {"name": "Factor de conductividad", "data": []}
            for caldera in calderas:
                factor_conductividad["data"].append({"name": caldera.punto_medicion.nombre, "valor": round(caldera.valor/alimentacion.valor, 2)})
            json_data.append(factor_conductividad)
            cloruros = datos.filter(parametro__nombre__icontains="cloruros")
            calderas = cloruros.filter(punto_medicion__nombre__icontains="caldera")
            alimentacion = cloruros.get(punto_medicion__nombre__icontains="alimentacion")
            factor_clorus = {"name": "Factor de cloruros", "data": []}
            for caldera in calderas:
                factor_clorus["data"].append({"name": caldera.punto_medicion.nombre, "valor": round(caldera.valor/alimentacion.valor, 2)})
            json_data.append(factor_clorus)
            silice = datos.filter(parametro__nombre__icontains="silice")
            calderas = silice.filter(punto_medicion__nombre__icontains="caldera")
            alimentacion = silice.get(punto_medicion__nombre__icontains="alimentacion")
            factor_silice = {"name": "Factor de silice", "data": []}
            for caldera in calderas:
                factor_silice["data"].append({"name": caldera.punto_medicion.nombre, "valor": round(caldera.valor/alimentacion.valor, 2)})
            json_data.append(factor_silice)
            dureza_total = datos.filter(parametro__nombre__icontains="dureza total")
            alimentacion_dureza = dureza_total.get(punto_medicion__nombre__icontains="alimentacion")
            hierro = datos.filter(parametro__nombre__icontains="hierro")
            alimentacion_hierro = hierro.get(punto_medicion__nombre__icontains="alimentacion")
            silice = datos.filter(parametro__nombre__icontains="silice")
            alimentacion_silice = silice.get(punto_medicion__nombre__icontains="alimentacion")
            fc_conductividad = {
                "name": "FC conductividad", 
                "data": [
                    {"name": "dureza_total", "data": []}, 
                    {"name": "hierro_teorico", "data": []}, 
                    {"name": "silice_teorico", "data": []}
                ]}
            #iterate valor of factor_conductividad
            for valor in factor_conductividad["data"]:
                # multiplicate valor of factor_conductividad by valor of alimentacion_dureza and append to fc_conductividad
                fc_conductividad["data"][0]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_dureza.valor, 2)})
                #multiplicate valor of factor_conductividad by valor of alimentacion_hierro and append to fc_conductividad
                fc_conductividad["data"][1]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_hierro.valor, 2)})
                #multiplicate valor of factor_conductividad by valor of alimentacion_silice and append to fc_conductividad
                fc_conductividad["data"][2]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_silice.valor, 2)})
            dureza_caldera = dureza_total.filter(punto_medicion__nombre__icontains="caldera")
            #iterate valor of dureza_caldera
            for valor_dureza in dureza_caldera:
                # print(valor_dureza.punto_medicion.nombre, valor_dureza.valor)
                for fc in fc_conductividad["data"]:
                    # print(fc)
                    #iterate on fc["data"] when name is dureza_total
                    if fc["name"] == "dureza_total":
                        for fc_valor in fc["data"]:
                            if fc_valor["name"] == valor_dureza.punto_medicion.nombre:
                                #if fc_valor["valor"] < valor_dureza.valor add status ok to fc_valor
                                if fc_valor["valor"] < valor_dureza.valor:
                                    fc_valor["status"] = "ok"
                                else:
                                    fc_valor["status"] = "alerta"
            hierro_caldera = hierro.filter(punto_medicion__nombre__icontains="caldera")
            #iterate valor of hierro_caldera
            for valor_hierro in hierro_caldera:
                # print(valor_hierro.punto_medicion.nombre, valor_hierro.valor)
                for fc in fc_conductividad["data"]:
                    # print(fc)
                    #iterate on fc["data"] when name is hierro_teorico
                    if fc["name"] == "hierro_teorico":
                        for fc_valor in fc["data"]:
                            if fc_valor["name"] == valor_hierro.punto_medicion.nombre:
                                #if fc_valor["valor"] > valor_hierro.valor add status ok to fc_valor
                                if fc_valor["valor"] > valor_hierro.valor:
                                    fc_valor["status"] = "ok"
                                else:
                                    fc_valor["status"] = "alerta"
            silice_caldera = silice.filter(punto_medicion__nombre__icontains="caldera")
            #iterate valor of silice_caldera
            for valor_silice in silice_caldera:
                # print(valor_silice.punto_medicion.nombre, valor_silice.valor)
                for fc in fc_conductividad["data"]:
                    # print(fc)
                    #iterate on fc["data"] when name is silice_teorico
                    if fc["name"] == "silice_teorico":
                        for fc_valor in fc["data"]:
                            if fc_valor["name"] == valor_silice.punto_medicion.nombre:
                                #if fc_valor["valor"] > valor_silice.valor add status ok to fc_valor
                                if fc_valor["valor"] > valor_silice.valor:
                                    fc_valor["status"] = "ok"
                                else:
                                    fc_valor["status"] = "alerta"
            json_data.append(fc_conductividad)
            fc_cloruros = {
                "name": "FC CLORUROS", 
                "data": [
                    {"name": "dureza_total", "data": []}, 
                    {"name": "hierro_teorico", "data": []}, 
                    {"name": "silice_teorico", "data": []}
                ]}
            #iterate valor of factor_clorus
            for valor in factor_clorus["data"]:
                # multiplicate valor of factor_clorus by valor of alimentacion_dureza and append to fc_cloruros
                fc_cloruros["data"][0]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_dureza.valor, 2), "status": "ok"})
                #multiplicate valor of factor_clorus by valor of alimentacion_hierro and append to fc_cloruros
                fc_cloruros["data"][1]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_hierro.valor, 2), "status": "ok"})
                #multiplicate valor of factor_clorus by valor of alimentacion_silice and append to fc_cloruros
                fc_cloruros["data"][2]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_silice.valor, 2), "status": "ok"})


            json_data.append(fc_cloruros)
            fc_silice = {
                "name": "FC SILICE",
                "data": [
                    {"name": "dureza_total", "data": []},
                    {"name": "hierro_teorico", "data": []},
                    {"name": "silice_teorico", "data": []}
                ]}
            #iterate valor of factor_silice
            for valor in factor_silice["data"]:
                # multiplicate valor of factor_silice by valor of alimentacion_dureza and append to fc_silice
                fc_silice["data"][0]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_dureza.valor, 2), "status": "ok"})
                #multiplicate valor of factor_silice by valor of alimentacion_hierro and append to fc_silice
                fc_silice["data"][1]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_hierro.valor, 2), "status": "ok"})
                #multiplicate valor of factor_silice by valor of alimentacion_silice and append to fc_silice
                fc_silice["data"][2]["data"].append({"name": valor["name"], "valor": round(valor["valor"]*alimentacion_silice.valor, 2), "status": "ok"})
            json_data.append(fc_silice)
            #generate pdf file
            plantilla = Plantilla.objects.get(id=pk_plantilla)
            parametros = Parametro.objects.filter(tipo=plantilla.tipo)
            puntos_medicion = PuntoMedicion.objects.filter(empresa=request.user.empresa, tipo=plantilla.tipo)
            datos_n = Datos.objects.filter(fecha=fecha_ini_tabla,plantilla=plantilla)
            datos_json = {}
            parametros_list = []
            puntos_list = []
            for p in puntos_form:
                puntos_list.append(PuntoMedicion.objects.get(pk=p))
            for parametro in parametros_form:
                parametro = Parametro.objects.get(pk=parametro)
                parametros_list.append(parametro)
                datos_json[parametro.id] = []
                for punto in puntos_form:

                    punto = PuntoMedicion.objects.get(pk=punto)
                    datos_n = Datos.objects.filter(punto_medicion=punto, parametro=parametro, fecha__range=[fecha_ini, fecha_fin],plantilla=plantilla)
                    #order by fecha asc
                    datos_n = datos_n.order_by('fecha')
                    datos_json[parametro.id].append({
                        'id' : punto.id,
                        'punto' : punto.nombre,
                        'data' : [],
                    })
                    #append to punto.nombre  dato.fecha and dato.valor to datos_json
                    for dato in datos_n:
                        datos_json[parametro.id][-1]['data'].append({
                            'fecha' : dato.fecha.strftime('%Y-%m-%d'),
                            'valor' : dato.valor,
                        })
            datos_json = json.dumps(datos_json)
            #send json data
            context = {
                "plantilla": plantilla,
                "parametros": parametros,
                "puntos_medicion": puntos_medicion,
                "puntos_list": puntos_list,
                "parametros_list": parametros_list,
                "datos": datos,
                "json_data": json_data,
                "fecha": datetime.now().date(),
                "fecha_ini_tabla": fecha_ini_tabla,
                "fecha_ini": fecha_ini,
                "fecha_fin": fecha_fin,
                "user": request.user,
                "datos_json": datos_json,
            }
            #print(json_data)
            return render(request, "pdf_template.html", context)
            open('pdf_template.html', 'w').write(render_to_string('result.html', context))
            pdf = html_to_pdf("pdf_template.html",context)
            return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('plantillas:index')
