from distutils.command.clean import clean
from django import forms
from .models import Parametro
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from apps.validaciones import validarLetras


class FormularioParametros(forms.ModelForm):

    class Meta:
        model = Parametro
        fields = ["nombre", "abreviado", "descripcion", "tipo"]

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_abreviado(self):
        abreviado = self.cleaned_data['abreviado']
        if abreviado is None:
            return None
        validarLetras(abreviado, "Abreviado")
        return abreviado

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )