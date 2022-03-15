from django import forms
from apps.budgets.models import *
from django.forms.fields import DateField

class BussinesForm(forms.ModelForm):

    class Meta:
        model = Bussines
        fields = [
                'name',
                'nit',
                'description',
                'address',
                'phone',
                'representative',
                'rubroPattern',
                'accountPattern',               
        ]
        
        labels = {

                'name': 'Nombre',
                'nit': 'NIT',
                'description': 'Descripción',
                'address': 'Dirección',
                'phone': 'Teléfono',
                'representative': 'Representación',
                'rubroPattern': 'Patrón rubro',
                'accountPattern': 'Patrón cuenta',
                
        }

        widgets = {
                'Nombre':forms.TextInput(),
                'NIT':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Dirección':forms.TextInput(),
                'Teléfono':forms.TextInput(),
                'Representación':forms.TextInput(),
                'Patrón rubro':forms.TextInput(),
                'Patrón cuenta':forms.TextInput(),
                
        }

class AccountPeriodForm(forms.ModelForm):

    class Meta:
        model = AccountPeriod

        fields = [
                'name',
                'state',
                'initialDate',
                'finalDate',           
        ]     
        labels = {

                'name': 'Nombre',
                'state': 'Estado',
                'initialDate': 'Fecha inicial',
                'finalDate': 'Fecha final',
                
        }

        widgets = {
                'Nombre':forms.TextInput(),
                'Estado':forms.TextInput(),
                'Fecha inicial':forms.DateInput(attrs={'class':'form-control  form-control-user', 'type':'date','id':'myDate','value':'aaaa-mm-dd'}),
                'Fecha final':forms.DateInput(attrs={'class':'form-control  form-control-user', 'type':'date','id':'myDate','value':'aaaa-mm-dd'}),
                
        }



class OperationForm(forms.ModelForm):

    class Meta:
        model = Operation
        fields = [
                'origin',
                'codeOp',
                'nameOp',
                'descriptionOp',
                'operation',
                'orderOp',
                'orderOp',
                             
        ]
        
        labels = {
                'origin': 'Origen',
                'codeOp': 'Código',
                'nameOp': 'Nombre',
                'descriptionOp': 'Descripción',
                'operation': 'Operación',
                'orderOp': 'Orden',
                
        }

        widgets = {
                'Origen':forms.TextInput(),
                'Código':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Operación':forms.TextInput(),
                'Orden':forms.TextInput(),
                
        }
      
class OriginForm(forms.ModelForm):
        

    class Meta:
        model = Origin
        fields = [
                'accountPeriod',
                'codeOrigin',
                'nameOrigin',
                'descriptionOrigin',
                'orderOrigin',
                'pattern',
                             
        ]
        
        labels = {
                'accountPeriodOrigin': 'Período contable',
                'codeOrigin': 'Código',
                'nameOrigin': 'Nombre',
                'descriptionOrigin': 'Descripción',    
                'orderOrigin': 'Orden',
                'pattern': 'Patrón',
                
        }

        widgets = { 				

                'Período contable':forms.TextInput(),
                'Código':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Orden':forms.TextInput(),
                'Patrón':forms.TextInput(),
                
        }

class ByBudgetForms(forms.Form):

    originB = forms.ChoiceField()
    operationB = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ByBudgetForms, self).__init__(*args, **kwargs)
        
        self.fields['originB'].label = 'Seleccione el origen'
        self.fields['operationB'].label = 'Seleccione la operación'

class ByAccountOpForms(forms.Form):
    accountsP = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ByAccountOpForms, self).__init__(*args, **kwargs)
        
        self.fields['accountsP'].label = 'Seleccione el período contable'

class ByInformForms(forms.Form):

    inform = forms.ChoiceField()
    detalles = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ByInformForms, self).__init__(*args, **kwargs)
        
        self.fields['inform'].label = 'Tipo de informe'
        self.fields['detalles'].label = 'Tipo de informe detalle'

class ByRubroUpdate(forms.Form):

    CHOICES = [('AUXILIAR','AUXILIAR'),('MAYOR', 'MAYOR')]
    rubroRubUpdate = forms.CharField(widget=forms.TextInput(attrs={'disabled':'disabled'})) 
    typeRubroRubUpdate = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    descriptionRubUpdate = forms.CharField()
    
    
    def __init__(self, *args, **kwargs):
        super(ByRubroUpdate, self).__init__(*args, **kwargs)
        
        self.fields['rubroRubUpdate'].label = 'Rubro'
        self.fields['typeRubroRubUpdate'].label = 'Tipo de rubro'
        self.fields['descriptionRubUpdate'].label = 'Descripción'  
