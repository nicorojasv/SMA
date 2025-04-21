from django import forms
from django.contrib.auth.forms import UserCreationForm
from plan.models import CustomUser, OrganismoSectorial

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creación de usuarios, extendiendo 
    el formulario estándar de Django `UserCreationForm`.

    Este formulario incluye campos adicionales como teléfono, RUT y 
    la asociación opcional a un organismo sectorial.

    Atributos:
        telefono (CharField): Campo obligatorio para ingresar el número de teléfono del usuario.
        rut (CharField): Campo obligatorio para ingresar el RUT del usuario.
        id_organismo_sectorial (ModelChoiceField): Campo opcional para seleccionar un organismo sectorial.
    
    Meta:
        model (CustomUser): Modelo personalizado de usuario.
        fields (list): Lista de campos a mostrar en el formulario.
        widgets (dict): Personalización de widgets para los campos de contraseña.
    """
    telefono = forms.CharField(max_length=15, required=True, label="Teléfono")
    rut = forms.CharField(max_length=12, required=True, label="RUT")
    id_organismo_sectorial = forms.ModelChoiceField(
        queryset=OrganismoSectorial.objects.all(),
        required=False,
        empty_label="Seleccione un Organismo",
        label="Organismo Sectorial"
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'telefono', 'rut', 'id_organismo_sectorial', 
            'password1', 'password2'
        ]
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
