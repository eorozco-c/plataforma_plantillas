from django import forms
from .models import Empresa
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from apps.validaciones import validarLongitud
class FormularioEmpresa(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ["nombre"]

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        validarLongitud(nombre,"nombre",2,15)
        return nombre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )
