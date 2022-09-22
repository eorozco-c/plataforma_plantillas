from django import forms
from .models import Plantilla, TipoPlantilla
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class FormularioPlantilla(forms.ModelForm):

    class Meta:
        model = Plantilla
        fields = ["nombre","tipo","activo"]

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        # element_exist = TipoPlantilla.objects.filter(plantillas_tipo__empresa=self.request.user.empresa)
        # self.fields['tipo'].queryset = TipoPlantilla.objects.exclude(id__in=element_exist)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )



class FormularioTipoPlantilla(forms.ModelForm):

    class Meta:
        model = TipoPlantilla
        fields = ["nombre","descripcion"]

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        if nombre.isalpha():
            return nombre
        else:
            raise forms.ValidationError("El nombre debe contener solo letras")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )