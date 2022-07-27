from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import PuntoMedicion
from .formularios import FormularioPuntoMedicion
from django.http.response import JsonResponse

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListPuntoMedicion(ListView):
    model = PuntoMedicion
    template_name = "puntos_medicion/puntos_medicion_list.html"

    def get_context_data(self, **kwargs):
        context = super(ListPuntoMedicion, self).get_context_data(**kwargs)
        context['appname'] = "puntos_medición"
        return context

    def get_queryset(self):
        return PuntoMedicion.objects.filter(empresa=self.request.user.empresa)

    def get(self, request):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class CreatePuntoMedicion(CreateView):
    model = PuntoMedicion
    form_class = FormularioPuntoMedicion
    template_name = "formularios/generico.html"
    success_url = reverse_lazy('puntos_medicion:index')

    def get_context_data(self, **kwargs):
        context = super(CreatePuntoMedicion, self).get_context_data(**kwargs)
        context['appname'] = "puntos_medición"
        return context

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def get(self, request):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class EditPuntoMedicion(UpdateView):
    model = PuntoMedicion
    form_class = FormularioPuntoMedicion
    template_name = "formularios/generico.html"
    success_url = reverse_lazy('puntos_medicion:index')

    def get_context_data(self, **kwargs):
        context = super(EditPuntoMedicion, self).get_context_data(**kwargs)
        context['appname'] = "puntos_medición"
        return context

    def get(self, request,pk):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            punto = PuntoMedicion.objects.get(id=pk)
        except:
            return redirect("puntos_medicion:index")
        context={
            'id' : punto.id,
            'nombre': punto.nombre,
            'descripcion': punto.descripcion,
        }
        return JsonResponse(context)
    return redirect("puntos_medicion:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        if request.user.is_staff:
            try:
                punto = PuntoMedicion.objects.get(id=pk)
            except:
                return redirect("puntos_medicion:index")
            punto.delete()
    return redirect("puntos_medicion:index")
