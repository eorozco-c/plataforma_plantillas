from django import forms
from .models import Licencia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from apps.validaciones import  validarLongitud

class FormularioLicencia(forms.ModelForm):

    class Meta:
        model = Licencia
        fields = ["empresas"]

        widgets = {
            "empresas" : forms.NumberInput(attrs={"min":0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto')
        )
