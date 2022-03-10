from django import forms
from apps.users.models import User
from django.contrib.auth.forms  import UserCreationForm
from apps.budgets.models import *

class UserForm(UserCreationForm):

	class Meta:
		model = User
		CHOICES = [('Cédula de Ciudadanía', 'Cédula de Ciudadanía'), ('Cédula Extranjeria', 'Cédula Extrangeria'), ('Pasaporte', 'Pasaporte')]
		CHOICES2 = [('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('Otro', 'Otro')]

		
		fields = [
				'username',
				'first_name',
				'last_name',
				'email',
				'password1',
				'password2',
				'typeIdentification',
                'identification',
                'genre',
				'typeUser',
                'address',
				'title',
                'observation',
		]
		labels = {
				'username': 'Nombre de Usuario',
				'first_name': 'Nombre',
				'last_name': 'Apellidos',
				'email': 'Correo Electrónico',
				'password1': 'Contraseña',
				'password2': 'Confirmación de Contraseña',
				'typeIdentification': 'Tipo Identificación',
                'identification': 'Número de Identificación',
                'genre': 'Sexo',
				'typeUser': 'Tipo de usuario',
                'address': 'Dirección',
				'title': 'Título',
                'observation': 'Observación',
		}
		widgets = {
				'username':forms.TextInput(),
				'first_name':forms.TextInput(),
				'last_name':forms.TextInput(),
				'email':forms.TextInput(),
				'password1':forms.CharField(widget=forms.PasswordInput()),
				'password2':forms.CharField(widget=forms.PasswordInput()),
				'typeIdentification':forms.Select(choices=CHOICES),
                'identification':forms.TextInput(),
                'genre':forms.Select(choices=CHOICES2),
                'typeUser':forms.TextInput(),
                'address':forms.TextInput(),
				'title':forms.TextInput(),
                'observation':forms.TextInput(),

		}


class ByBussinesForms(forms.Form):

    bussines = forms.ModelChoiceField(Bussines.objects.all() , required=True)
    accountsP = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ByBussinesForms, self).__init__(*args, **kwargs)
        
        self.fields['bussines'].label = 'Seleccione la empresa a trabajar'
        self.fields['accountsP'].label = 'Seleccione el período contable'
