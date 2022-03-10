from django import forms
from apps.budgets.models import *
from django.forms.fields import DateField

class OriginFormSetting(forms.ModelForm):
        

    class Meta:
        model = Origin
        fields = [
                'codeOrigin',
                'nameOrigin',
                'descriptionOrigin',
                'orderOrigin',
                'pattern',
                             
        ]
        
        labels = {
                'codeOrigin': 'Código',
                'nameOrigin': 'Nombre',
                'descriptionOrigin': 'Descripción',    
                'orderOrigin': 'Orden',
                'pattern': 'Patrón',
                
        }

        widgets = { 				

                'Código':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Orden':forms.TextInput(),
                'Patrón':forms.TextInput(),
                
        }

class TypeAgreementForm(forms.ModelForm):
        

    class Meta:
        model = TypeAgreement
        fields = [
                'codeTA',
                'nameTA',
                'descriptionTA',
                'ordenTA',
        ]
        
        labels = {
                'codeTA': 'Código',
                'nameTA': 'Nombre',
                'descriptionTA': 'Descripción',
                'ordenTA': 'Orden',                
        }

        widgets = { 				
                'Código':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Orden':forms.TextInput(),                
        }


class InformForm(forms.ModelForm):
        
        class Meta:
                
                CHOICES = [('I','Informe'),('R', 'Registro')]
                model = Inform
                fields = [
                        'nameI',
                        'category',
                ]
                
                labels = {
                        'nameI': 'Nombre',
                        'category': 'Categoría',         
                }

                widgets = { 
                        			
                        'Nombre':forms.TextInput(),
                        'Categoría':forms.ChoiceField(choices=CHOICES),	    
                }


class InformFormDetall(forms.ModelForm):
        

    class Meta:
        model = InformDetall
        fields = [
                'codeInfD',
                'descriptionInfD',
        ]
        
        labels = {
                'codeInfD': 'Código',
                'descriptionInfD': 'Descripción de detalles',
        }

        widgets = { 				
                'Código':forms.TextInput(),
                'Descripción de detalles':forms.TextInput(),
        }

class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = [
                'code',
                'description',
                'nature',
                'typeAccount',
                'level',
                'state',
                'corriente'
        ]
        
        labels = {
                'code': 'Código',
                'description': 'Descripción',
                'typeAccount': 'Tipo de cuenta',
                'nature': 'Natural',
                'level': 'Nivel',
                'state': 'Estado',
                'corriente': 'Corriente'               
        }

        widgets = { 				
                'Código':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Tipo de cuenta':forms.TextInput(),
                'Naturaleza':forms.TextInput(),
                'Nivel':forms.TextInput(),  
                'Estado':forms.TextInput(),
                'Corriente':forms.TextInput(),               
        }

class DiscountForm(forms.ModelForm):
        

    class Meta:
        model = Discount
        fields = [
                'name',
                'account',
                'typeDiscount',
                'state',
                'baseCalculate',
                'average',
                'initialValue',
                'finalValue'
        ]
        
        labels = {
                'name': 'Nombre',
                'account': 'Cuenta',
                'typeDiscount': 'Tipo de descuento',
                'state': 'Estado',
                'baseCalculate': 'Base calculo',
                'average': 'Porcentaje',
                'initialValue': 'Valor inicial',
                'finalValue': 'Valor final'               
        }

        widgets = { 				
                'Nombre':forms.TextInput(),
                'Cuenta':forms.TextInput(),
                'Tipo de descuento':forms.TextInput(),
                'Estado':forms.TextInput(),
                'Base calculo':forms.TextInput(),
                'Porcentaje':forms.TextInput(),  
                'Valor inicial':forms.TextInput(),
                'Valor final':forms.TextInput(),               
        }

class ByAccountUpdate(forms.Form):

        CHOICES = [('ACTIVO','Activo'),('INACTIVO', 'Inactivo')]

        nameUpdate = forms.CharField()
        stateUpdate = forms.ChoiceField(choices=CHOICES)
        initialDateUAC = forms.DateField()
        finalDatenUAC = forms.DateField()

        def __init__(self, *args, **kwargs):
                super(ByAccountUpdate, self).__init__(*args, **kwargs)
                
                self.fields['nameUpdate'].label = 'Nombre'
                self.fields['stateUpdate'].label = 'Estado'
                self.fields['initialDateUAC'].label = 'Fecha inicial'
                self.fields['finalDatenUAC'].label = 'Fecha final'

class ByInformUpdate(forms.Form):

        nameIUpdate = forms.CharField()
        categoryUpdate = forms.CharField()          
        digitIUpdate= forms.CharField()
        
        def __init__(self, *args, **kwargs):
                super(ByInformUpdate, self).__init__(*args, **kwargs)
                
                self.fields['nameIUpdate'].label = 'Nombre'
                self.fields['categoryUpdate'].label = 'Categoría'
                self.fields['digitIUpdate'].label = 'Dígito'

class ByTypeAgreementUpdate(forms.Form):

        codeTAUpdate = forms.CharField()
        nameTAUpdate = forms.CharField()
        descriptionTAUpdate = forms.CharField()          
        ordenTAUpdate= forms.CharField()
        
        def __init__(self, *args, **kwargs):
                super(ByTypeAgreementUpdate, self).__init__(*args, **kwargs)
                
                self.fields['codeTAUpdate'].label = 'Código'
                self.fields['nameTAUpdate'].label = 'Nombre'
                self.fields['descriptionTAUpdate'].label = 'Descripción'
                self.fields['ordenTAUpdate'].label = 'Orden'

class ContraOperationForm(forms.Form):

        origen = forms.ChoiceField()
        contraoperation = forms.ChoiceField()
        
        def __init__(self, *args, **kwargs):
                super(ContraOperationForm, self).__init__(*args, **kwargs)
                
                self.fields['origen'].label = 'Seleccione su origen'
                self.fields['contraoperation'].label = 'Seleccione su contraoperación'

class OperationUpdateForm(forms.Form):

        CHOICES = [('+','+'),('-', '-'),('*', '*'),('/', '/')]
        codeOpUpdate = forms.CharField()
        nameOpUpdate = forms.CharField()
        operationOpUpdate = forms.ChoiceField(choices=CHOICES)
        orderOpUpdate = forms.CharField()
    
        def __init__(self, *args, **kwargs):
                super(OperationUpdateForm, self).__init__(*args, **kwargs)
        
                self.fields['codeOpUpdate'].label = 'Código'
                self.fields['nameOpUpdate'].label = 'Nombre'
                self.fields['operationOpUpdate'].label = 'Operación'
                self.fields['orderOpUpdate'].label = 'Orden'
                
class ByBudgetOriginForm(forms.Form):

        originSelectO = forms.ChoiceField()

        def __init__(self, *args, **kwargs):
                super(ByBudgetOriginForm, self).__init__(*args, **kwargs)
                
                self.fields['originSelectO'].label = 'Seleccione el origen'

class AccountUpdate(forms.Form):

        CHOICES = [('ACTIVO','ACTIVO'),('INACTIVO', 'INACTIVO')]
        CHOICES2 = [('M','M'),('A', 'A')]

        codeAccountUpdate = forms.CharField()
        descriptionAccountUpdate = forms.CharField()
        natureAccountUpdate = forms.CharField(widget=forms.TextInput(attrs={'disabled':'disabled'}))
        typeAccountUpdate = forms.ChoiceField(choices=CHOICES2)                
        levelAccountUpdate= forms.CharField(widget=forms.TextInput(attrs={'disabled':'disabled'})) 
        stateAccountUpdate = forms.ChoiceField(choices=CHOICES)
        corrienteAccountUpdate = forms.CharField(widget=forms.TextInput(attrs={'disabled':'disabled'}))          
        
        def __init__(self, *args, **kwargs):
                super(AccountUpdate, self).__init__(*args, **kwargs)
                
                self.fields['codeAccountUpdate'].label = 'Código'
                self.fields['descriptionAccountUpdate'].label = 'Descripción'
                self.fields['natureAccountUpdate'].label = 'Natural' 
                self.fields['typeAccountUpdate'].label = 'Tipo de cuenta'             
                self.fields['levelAccountUpdate'].label = 'Nivel'
                self.fields['stateAccountUpdate'].label = 'Estado'
                self.fields['corrienteAccountUpdate'].label = 'Corriente'
               

