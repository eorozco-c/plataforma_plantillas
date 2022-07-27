from webbrowser import get
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .formularios import FormularioNuevoUsuarioUpdate, FormularioRegistro, FormularioActualizarPass, FormularioEditarRegistro, FormularioNuevoUsuario
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.utils.decorators import method_decorator 
from django.contrib.auth.decorators import login_required
from .models import Usuario
# Create your views here.

class Login(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('master:index')
        
        

class Registrar(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioRegistro
    success_url = reverse_lazy("master:index")

    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario.username = usuario.email
        usuario.set_password(usuario.password)
        usuario.is_staff = True
        usuario.save()
        login(self.request, usuario)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Registrar, self).get_context_data(**kwargs)
        context['legend'] = "Registro de Usuario"
        return context

    def get(self, request):
        if self.request.user.is_superuser or Usuario.objects.count() == 0:
            return super().get(request)
        return redirect("master:index")

class Profile(UpdateView):
    template_name = "registration/perfil.html"
    model = Usuario
    form_class = FormularioEditarRegistro

    def post(self, request, *args, **kwargs):
        if "changePassword" in request.POST:
            change_pass = FormularioActualizarPass(request.POST,instance=self.request.user)
            formRegistro = FormularioEditarRegistro(instance=self.request.user)
            if change_pass.is_valid():
                usuario = change_pass.save(commit = False)
                usuario.set_password(usuario.password)
                usuario.save()
                login(request, usuario)
                messages.success(request,'Actualizado correctamente.')
                return redirect("usuarios:perfil", pk=self.request.user.id)
            else:
                context = {
                    "form" : formRegistro,
                    "change_pass" : change_pass,
                }
                return render(request,"registration/perfil.html",context)

        elif "editProfile" in request.POST:
            change_pass = FormularioActualizarPass()
            formRegistro = FormularioEditarRegistro(request.POST,instance=self.request.user)
            if formRegistro.is_valid():
                usuario = formRegistro.save()
                messages.success(request,'Actualizado correctamente.')
                return redirect("usuarios:perfil", pk=self.request.user.id)
            else:
                context = {
                    "form" : formRegistro,
                    "change_pass" : change_pass,
                }
                return render(request,"registration/perfil.html",context)

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context["change_pass"] = FormularioActualizarPass(instance=self.request.user)
        context["appname"] = "perfil"
        return context

    def get(self, request, pk):
        usuario = self.get_object()
        if self.request.user != usuario:
            return redirect("master:index")
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class ListUsuarios(ListView):
    model = Usuario
    template_name = "usuarios/usuarios_list.html"

    def get_queryset(self):
        queryset = Usuario.objects.filter(empresa=self.request.user.empresa)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListUsuarios, self).get_context_data(**kwargs)
        context['appname'] = "usuarios" 
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_staff:
            return super().get(*args, **kwargs)
        return redirect("master:index")


@method_decorator(login_required, name='dispatch')
class CreateUsuario(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioNuevoUsuario
    success_url = reverse_lazy("usuarios:index")

    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario.username = usuario.email
        usuario.set_password(usuario.password)
        usuario.empresa = self.request.user.empresa
        usuario.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateUsuario, self).get_context_data(**kwargs)
        context['legend'] = "Nuevo Usuario"
        context['appname'] = "usuarios"
        return context

    def get(self, request):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class EditUsuario(UpdateView):
    template_name = "formularios/generico.html"
    form_class = FormularioNuevoUsuarioUpdate
    model = Usuario
    success_url = reverse_lazy("usuarios:index")

    def get_context_data(self, **kwargs):
        context = super(EditUsuario, self).get_context_data(**kwargs) 
        context['legend'] = "Editar Usuario"
        context['appname'] = "usuarios"
        return context

    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario_instance = Usuario.objects.get(id=self.kwargs['pk'])
        if usuario.password != usuario_instance.password:
            usuario.set_password(usuario.password)
        usuario.save()
        return super().form_valid(form)
    
    def get(self, request,pk):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            usuario = Usuario.objects.get(id=pk)
        except:
            return redirect("usuarios:index")
        context={
            'id' : usuario.id,
            'nombre': usuario.first_name,
            'apellido' : usuario.last_name,
            'email' : usuario.email,
        }
        return JsonResponse(context)
    return redirect("usuarios:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        if request.user.is_staff:
            try:
                usuario = Usuario.objects.get(id=pk)
            except:
                return redirect("usuarios:index")
            if request.user.empresa != usuario.empresa:
                return redirect("master:index")
            usuario.delete()
    return redirect("usuarios:index")

