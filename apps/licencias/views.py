from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.empresas.models import Empresa
from apps.licencias.formularios import FormularioLicencia
from .models import Licencia
from django.contrib import messages
from cryptography.fernet import Fernet

# # Create your views here.
@method_decorator(login_required, name='dispatch')
class ListLicencia(ListView):
    model = Licencia
    template_name = "licencias/licencias_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(ListLicencia, self).get_context_data(**kwargs)
        context['appname'] = "licencias"
        #count anexos,colas,ivr,epa,agentes,campanas by empresa and send in list
        empresas = Empresa.objects.all().count()
        lista = {
            'empresas': empresas,
        }
        context['lista'] = lista
        return context
    
    def get_queryset(self):
        try:
            licencia = Licencia.objects.get(id=1)
        except:
            licencia = Licencia.objects.create(id=1,empresas=1,uuid='-1')
        return licencia

    def get(self, request):
        if self.request.user.is_staff:
            return super().get(request)
        return redirect("master:index")

#create def with form FormularioLicencia
@login_required(login_url="/")
def generar_licencia(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            empresas = request.POST.get('empresas')
            #create  licencia
            licencia = f"empresas:{empresas}"
            #encrypt licencia 
            key = Fernet.generate_key()
            try:
                objeto = Licencia.objects.get(id=1)
                objeto.uuid = key.decode()
                objeto.save()
            except:
                objeto = Licencia.objects.create(
                    uuid=key.decode(),
                    id=1,
                )
            cipher_suite = Fernet(key)
            licencia_encriptada = cipher_suite.encrypt(licencia.encode())
            with open(f"media/licence.key", "wb") as f:
                f.write(licencia_encriptada)
            return redirect('licencias:generar_licencia')         
        else:
            form = FormularioLicencia()
            context = {
                'form':form,
                'appname':'generar_licencia',
                'legend':'Generar licencia',
            }
            return render(request, 'licencias/generico.html', context)
    else:
        return redirect('master:index')


@login_required(login_url="/")
def licenciaImport(request):
    if request.user.is_staff:
        if request.method == 'POST':
            if request.FILES:
                licence_file = request.FILES["archivo"]
                #print content of file
                licencia = Licencia.objects.get(id=1)
                key = licencia.uuid
                cipher_suite = Fernet(key.encode())
                empresas = Empresa.objects.all().count()
                try:
                    licencia_desencriptada = cipher_suite.decrypt(licence_file.read()).decode()
                    #split by ,
                    licencia_desencriptada = licencia_desencriptada.split(',')
                    #create list of objects
                    lista = {
                        'empresas':licencia_desencriptada[0].split(':')[1],
                    }
                    # print(int(lista['anexos']) - int(anexos))
                    if int(lista['empresas']) - int(empresas) < 0:
                        messages.success(request, 'No se puede importar la licencia, hay demasiadas empresas.',extra_tags='danger')
                        return redirect('licencias:index')
                    
                    #update licencia with lista:
                    licencia.empresas = lista['empresas']
                    licencia.save()
                    messages.success(request,f'Licencia creada correctamente.',extra_tags='success')
                except:
                    messages.success(request,f'Error al importar licencia.',extra_tags='danger')
    return redirect("licencias:index")