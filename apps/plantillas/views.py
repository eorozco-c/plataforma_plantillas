from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Plantilla, TipoPlantilla
from .formularios import FormularioPlantilla,FormularioTipoPlantilla
from datetime import date, datetime
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class ListPlantillas(ListView):
    model = Plantilla
    template_name = "plantillas/plantillas_list.html"

    def get_queryset(self):
        queryset = Plantilla.objects.filter(empresa=self.request.user.empresa)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListPlantillas, self).get_context_data(**kwargs)
        context['appname'] = "plantillas"
        return context

        
@method_decorator(login_required, name='dispatch')
class CreatePlantilla(CreateView):
    model = Plantilla
    form_class = FormularioPlantilla
    template_name = "formularios/generico.html"
    success_url = reverse_lazy('plantillas:index')

    def get_context_data(self, **kwargs):
        context = super(CreatePlantilla, self).get_context_data(**kwargs)
        context['appname'] = "plantillas"
        return context

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super(CreatePlantilla, self).form_valid(form)


    def get_form_kwargs(self):
        kwargs = super(CreatePlantilla, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, *args, **kwargs):
        if self.request.user.is_staff:
            return super().get(*args, **kwargs)
        return redirect("master:index")

        
@method_decorator(login_required, name='dispatch')
class EditPlantilla(UpdateView):
    template_name = "formularios/generico.html"
    model = Plantilla
    form_class = FormularioPlantilla
    success_url = reverse_lazy("plantillas:index")

    def get_context_data(self, **kwargs):
        context = super(EditPlantilla, self).get_context_data(**kwargs)
        context['legend'] = f"Editar Plantilla"
        context['appname'] = "plantillas"
        return context
    
    def get_form_kwargs(self):
        kwargs = super(EditPlantilla, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, pk):
        objeto = self.get_object()
        if self.request.user.empresa != objeto.empresa:
            return redirect("master:index")
        elif not self.request.user.is_staff:
            return redirect("master:index")
        return super().get(request)


# @login_required(login_url="/")
# def predestroy(request, pk):
#     if request.user.has_perm('asterisk.delete_siptrunk'):
#         if request.method == "GET":
#             try:
#                 siptrunk = SipTrunk.objects.get(id=pk)
#             except:
#                 return redirect("siptrunk:index")
#             context={
#                 'id' : siptrunk.id,
#                 'troncal': siptrunk.troncal,
#                 'host': siptrunk.host,
#             }
#             return JsonResponse(context)
#     return redirect("siptrunk:index")

# @login_required(login_url="/")
# def destroy(request,pk):
#     if request.user.has_perm('asterisk.delete_siptrunk'):
#         if request.method == "GET":
#             try:
#                 siptrunk = SipTrunk.objects.get(id=pk)
#             except:
#                 return redirect("siptrunk:index")
#             if request.user.empresa == siptrunk.empresa:
#                 try:
#                     config = configparser.ConfigParser()
#                     with open(sip_custom, 'r+') as s:
#                         config.read_file(s)
#                         config.remove_section(siptrunk.troncal)
#                         s.seek(0)
#                         config.write(s)
#                         s.truncate()
#                     siptrunk.delete()
#                     cmd = "rasterisk -x \"sip reload\""
#                     os.system(cmd)
#                 except:
#                     messages.success(request,f'No se puede eliminar elemento ya que tiene elementos asignados',extra_tags='danger')
#     return redirect("siptrunk:index")

@method_decorator(login_required, name='dispatch')
class ListTipoPlantilla(ListView):
    model = TipoPlantilla
    template_name = "plantillas/tipo_plantilla_list.html"

    def get_context_data(self, **kwargs):
        context = super(ListTipoPlantilla, self).get_context_data(**kwargs)
        context['appname'] = "plantillas"
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class CreateTipoPlantilla(CreateView):
    model = TipoPlantilla
    form_class = FormularioTipoPlantilla
    template_name = "formularios/generico.html"
    success_url = reverse_lazy('plantillas:tipos_plantillas')

    def get_context_data(self, **kwargs):
        context = super(CreateTipoPlantilla, self).get_context_data(**kwargs)
        context['appname'] = "plantillas"
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class EditTipoPlantilla(UpdateView):
    model = TipoPlantilla
    form_class = FormularioTipoPlantilla
    template_name = "formularios/generico.html"
    success_url = reverse_lazy("plantillas:tipos_plantillas")

    def get_context_data(self, **kwargs):
        context = super(EditTipoPlantilla, self).get_context_data(**kwargs)
        context['appname'] = "plantillas"
        return context

    def get(self, request, pk):
        if self.request.user.is_superuser:
            return super().get(request)
        return redirect("master:index")

@login_required(login_url="/")
def predestroy_tipo_plantilla(request, pk):
    if request.method == "GET":
        try:
            tipo_plantilla = TipoPlantilla.objects.get(id=pk)
        except:
            return redirect("plantillas:tipos_plantillas")
        context={
            'id' : tipo_plantilla.id,
            'nombre': tipo_plantilla.nombre,
        }
        return JsonResponse(context)
    return redirect("plantillas:tipos_plantillas")

@login_required(login_url="/")
def destroy_tipo_plantilla(request,pk):
    if request.method == "GET":
        try:
            tipo_plantilla = TipoPlantilla.objects.get(id=pk)
        except:
            return redirect("plantillas:tipos_plantillas")
        if request.user.is_superuser:
            tipo_plantilla.delete()
    return redirect("plantillas:tipos_plantillas")