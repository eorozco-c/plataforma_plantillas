from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Parametro
from .formularios import FormularioParametros
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
