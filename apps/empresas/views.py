import os
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Empresa
from apps.usuarios.models import Usuario
from .formularios import FormularioEmpresa
from apps.licencias.models import Licencia

# Create your views here.

@method_decorator(login_required, name='dispatch')
class ListEmpresas(ListView):
    model = Empresa
    template_name = "empresas/empresas_list.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_staff:
            return super().get(*args, **kwargs)
        return redirect("master:index")

    def get_context_data(self, **kwargs):
        context = super(ListEmpresas, self).get_context_data(**kwargs)
        context['appname'] = "empresas" 
        context['licencia'] = Licencia.objects.get(id=1)
        return context

class CrearEmpresa(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioEmpresa
    success_url = reverse_lazy("empresas:index")

    def get_context_data(self, **kwargs):
        context = super(CrearEmpresa, self).get_context_data(**kwargs)
        context['legend'] = "Registro empresa"
        context['appname'] = "empresas"
        return context

    # def get(self, *args, **kwargs):
    #     objeto = Empresa.objects.all().count()
    #     if self.request.user.is_staff or Empresa.objects.count() == 0:
    #         if Licencia.objects.get(id=1).empresas > objeto.count():
    #             return super().get(*args, **kwargs)
    #     return redirect("master:index")

    def form_valid(self,form):
        empresa = form.save()
        #create folder in media/ with name same to empresa:
        os.mkdir(os.path.join("media",str(empresa.nombre)))
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditEmpresa(UpdateView):
    template_name = "formularios/generico.html"
    model = Empresa
    form_class = FormularioEmpresa
    success_url = reverse_lazy("empresas:index")

    def get_context_data(self, **kwargs):
        context = super(EditEmpresa, self).get_context_data(**kwargs)
        context['legend'] = "Editar Empresa"
        context['appname'] = "empresas"
        return context
        
    def get(self, *args, **kwargs):
        if self.request.user.is_staff:
            return super().get(*args, **kwargs)
        return redirect("master:index")

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            empresa = Empresa.objects.get(id=pk)
        except:
            return redirect("empresas:index")
        context={
            'id' : empresa.id,
            'nombre': empresa.nombre,
        }
        return JsonResponse(context)
    return redirect("empresas:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        if request.user.is_staff:
            try:
                empresa = Empresa.objects.get(id=pk)
            except:
                return redirect("empresas:index")
            try:
                empresa.delete()
            except:
                messages.success(request,f'No se puede eliminar empresa ya que tiene elementos asignados',extra_tags='danger')
                return redirect("empresas:index")
    return redirect("empresas:index")

@login_required(login_url="/")
def cambiarEmpresa(request, pk):
    if request.method == "GET":
        if request.user.is_staff:
            empresa = Empresa.objects.get(id=pk)
            usuario = Usuario.objects.get(id=request.user.id)
            usuario.empresa = empresa
            usuario.save()
    return redirect("empresas:index")