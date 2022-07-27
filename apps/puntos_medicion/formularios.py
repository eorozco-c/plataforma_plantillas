from distutils.command.clean import clean
from django import forms
from .models import PuntoMedicion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from apps.validaciones import validarLetras


class FormularioPuntoMedicion(forms.ModelForm):

    class Meta:
        model = PuntoMedicion
        fields = ["nombre", "descripcion", "activo"]

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'activo': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )