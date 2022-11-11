from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Parametro, Limite
from .formularios import FormularioParametros
from apps.puntos_medicion.models import PuntoMedicion
from django.http.response import JsonResponse

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListParametros(ListView):
    model = Parametro
    template_name = "parametros/parametros_list.html"

    def get_context_data(self, **kwargs):
        context = super(ListParametros, self).get_context_data(**kwargs)
        context['appname'] = "parámetros"
        return context

    def get(self, request):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class CreateParametros(CreateView):
    model = Parametro
    form_class = FormularioParametros
    template_name = "formularios/generico.html"
    success_url = reverse_lazy('parametros:index')

    def get_context_data(self, **kwargs):
        context = super(CreateParametros, self).get_context_data(**kwargs)
        context['appname'] = "parámetros"
        return context

    def get(self, request):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class EditParametros(UpdateView):
    model = Parametro
    form_class = FormularioParametros
    template_name = "formularios/generico.html"
    success_url = reverse_lazy('parametros:index')

    def get_context_data(self, **kwargs):
        context = super(EditParametros, self).get_context_data(**kwargs)
        context['appname'] = "parámetros"
        return context

    def get(self, request,pk):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            parametro = Parametro.objects.get(id=pk)
        except:
            return redirect("parametros:index")
        context={
            'id' : parametro.id,
            'nombre': parametro.nombre,
            'descripcion': parametro.descripcion,
        }
        return JsonResponse(context)
    return redirect("parametros:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        if request.user.is_staff:
            try:
                parametro = Parametro.objects.get(id=pk)
            except:
                return redirect("parametros:index")
            parametro.delete()
    return redirect("parametros:index")

#add template that add limite to parametro and punto_medicion
@login_required(login_url="/")
def agregar_limite(request, pk):
    if request.method == "GET":
        if request.user.is_staff:
            try:
                parametro = Parametro.objects.get(id=pk)
            except:
                return redirect("parametros:index")
            puntos_medicion = PuntoMedicion.objects.filter(empresa=request.user.empresa)
            #limite by punto_medicion
            limites = Limite.objects.filter(parametro=parametro)
            context={
                'parametro': parametro,
                'puntos_medicion': puntos_medicion,
                'limites': limites,
                'appname': "parámetros",
            }
            return render(request, "parametros/parametros_limite.html", context)
    elif request.method == "POST":
        if request.user.is_staff:
            try:
                parametro = Parametro.objects.get(id=pk)
                punto_medicion = PuntoMedicion.objects.get(id=request.POST['punto_medicion'])
            except:
                return redirect("parametros:index")
            limite = request.POST['limite']
            if limite == "":
                limite = None
            #if exist limite for this parametro and punto_medicion update it else create new
            valor = Limite.objects.filter(parametro=parametro, punto_medicion=punto_medicion)
            if valor:
                valor = valor[0]
                valor.limite = limite
                valor.save()
            else:
                Limite.objects.create(parametro=parametro, punto_medicion=punto_medicion, limite=limite)
            return redirect("parametros:agregar_limite", pk=pk)
    return redirect("parametros:index")
