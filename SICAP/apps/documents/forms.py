from django import forms
from apps.budgets.models import *
from django.forms.fields import DateField

class VoucherForm(forms.ModelForm):

    class Meta:
        model = Voucher
        fields = [
                'code',
                'name',
                'description',
                'order',
                'number',
                'category',                             
        ]
        
        labels = {
                'code': 'Código',
                'name': 'Nombre',
                'description': 'Descripción',    
                'order': 'Orden',
                'number': 'Número',
                'category': 'Categoría',          
        }

        widgets = { 				

                'Código':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Orden':forms.TextInput(),
                'Número':forms.TextInput(),
                'Categoría':forms.TextInput(),
        }
class ThirdForm(forms.ModelForm):

    class Meta:
        model = Third
        
        fields = [
                'typeIdentification',
                'identification',
                'name',
                'surnames',
                'reason',
                'phone',
                'city',                             
        ]
        
        labels = {

                'typeIdentification': 'Tipo de Identificación',
                'identification': 'Identificación',
                'name': 'Nombre',
                'surnames': 'Apellidos',    
                'reason': 'Razón',
                'phone': 'Teléfono',
                'city': 'Ciudad',          
        }

        widgets = {

                'Tipo de Identificación':forms.TextInput(),
                'Identificación':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Apellidos':forms.TextInput(),
                'Razón':forms.TextInput(),
                'Teléfono':forms.TextInput(),
                'Ciudad':forms.TextInput(),
        }

class TypeContractForm(forms.ModelForm):

    class Meta:
        model = TypeContract
        fields = [
                'nameTC',
                'description',
                
                                            
        ]
        
        labels = {
                   
                'nameTC': 'Nombre',
                'description': 'Descripción',   
        }

        widgets = { 		
                		
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
        }

class TypeContractDetailForm(forms.ModelForm):

    class Meta:
        model = TypeContractDetail
        fields = [
                'codeTypeC',
                'descriptionTypeC',
        ]
        
        labels = {
                'codeTypeC': 'Nombre',
                'descriptionTypeC': 'Descripción de detalles',
        }

        widgets = { 				
                'Nombre':forms.TextInput(),
                'Descripción de detalles':forms.TextInput(),
        }

class ByVoucherUpdate(forms.Form):

    codeUpdate = forms.CharField()
    nameUpdate = forms.CharField()
    descriptionUpdate = forms.CharField(widget=forms.Textarea)
    orderUpdate = forms.CharField()
    numberUpdate = forms.CharField()
    categoryUpdate = forms.CharField()
    

    def __init__(self, *args, **kwargs):
        super(ByVoucherUpdate, self).__init__(*args, **kwargs)
        
        self.fields['codeUpdate'].label = 'Código'
        self.fields['nameUpdate'].label = 'Nombre'
        self.fields['descriptionUpdate'].label = 'Descripción'
        self.fields['orderUpdate'].label = 'Orden'
        self.fields['numberUpdate'].label = 'Número'
        self.fields['categoryUpdate'].label = 'Categoría'
        

class ByThirdUpdate(forms.Form):
        
    CHOICES = [('Cédula de Ciudadanía', 'Cédula de Ciudadanía'), ('Cédula Extranjeria', 'Cédula Extrangeria'), ('Pasaporte', 'Pasaporte')]
    typeIdentificationUpdate = forms.ChoiceField(choices=CHOICES)
    identificationUpdate = forms.CharField()
    nameUpdate = forms.CharField()
    surnamesUpdate = forms.CharField()
    reasonUpdate = forms.CharField()
    phoneUpdate = forms.CharField()
    cityUpdate = forms.CharField()
    

    def __init__(self, *args, **kwargs):
        super(ByThirdUpdate, self).__init__(*args, **kwargs)
        
        self.fields['typeIdentificationUpdate'].label = 'Tipo de Identificación' 
        self.fields['identificationUpdate'].label = 'Identificación'
        self.fields['nameUpdate'].label = 'Nombres'
        self.fields['surnamesUpdate'].label = 'Apellidos'
        self.fields['reasonUpdate'].label = 'Razón'
        self.fields['phoneUpdate'].label = 'Teléfono'
        self.fields['cityUpdate'].label = 'Ciudad'

class ByTypeContractUpdate(forms.Form):
    
    digitsTCUpdate = forms.CharField()
    nameTCUpdate = forms.CharField()
    descriptionUpdate = forms.CharField(widget=forms.Textarea)
    categoryTCUpdate = forms.CharField()
    
    

    def __init__(self, *args, **kwargs):
        super(ByTypeContractUpdate, self).__init__(*args, **kwargs)
        
        self.fields['nameTCUpdate'].label = 'Nombre' 
        self.fields['descriptionUpdate'].label = 'Descripción'


