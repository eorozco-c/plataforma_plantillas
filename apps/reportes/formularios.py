from django import forms
from .models import Datos
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class FormularioDatos(forms.ModelForm):

    class Meta:
        model = Datos
        fields = ["valor1", "valor2", "valor3"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )