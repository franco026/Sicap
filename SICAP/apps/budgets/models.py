from django.db import models
from django.forms.fields import DateField
class Bussines(models.Model):

    # user = models.ForeignKey(Nodes, null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, unique=True)
    nit = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    address =  models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    representative = models.CharField(max_length=100)
    rubroPattern = models.CharField(max_length=100)
    accountPattern = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

class AccountPeriod(models.Model):

    CHOICES = [('Activo','Activo'),('Inactivo', 'Inactivo')]
    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100,choices=CHOICES)
    initialDate = models.DateField()
    finalDate = models.DateField()

    def __str__(self):
        return '{}'.format(self.name)

class Origin(models.Model):
    
    # Opcional poner la empresa
    # bussines = models.ForeignKey(Bussines, null=False, blank=True, on_delete=models.CASCADE)
    accountPeriod = models.ForeignKey(AccountPeriod, null=False, blank=True, on_delete=models.CASCADE)
    nameOrigin = models.CharField(max_length=100)
    codeOrigin = models.CharField(max_length=100)
    descriptionOrigin = models.TextField()
    orderOrigin = models.IntegerField()
    pattern = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.nameOrigin)

class Operation(models.Model):

    CHOICES = [('+','+'),('-', '-'),('*', '*'),('/', '/')]

    origin = models.ManyToManyField(Origin, blank=True)
    codeOp = models.CharField(max_length=2)
    nameOp = models.CharField(max_length=100)
    descriptionOp = models.TextField()
    operation = models.CharField(max_length=10,choices=CHOICES)
    orderOp = models.IntegerField()
    contraOperar = models.BigIntegerField(null=True, blank=True)
    contraOperarName = models.CharField(max_length=100,null=True, blank=True)
    contraOrigin = models.BigIntegerField(null=True, blank=True) 

    # Opcional poner  el periodo por facilidad
    # accountPeriod = models.ForeignKey(AccountPeriod, null=False, blank=True, on_delete=models.CASCADE)

class TypeAgreement(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    codeTA = models.CharField(max_length=100) 
    nameTA = models.CharField(max_length=100) 
    descriptionTA = models.TextField()
    ordenTA =  models.IntegerField()
    validacionTA = models.CharField(max_length=100, blank=True)
    mensajeTA = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '{}'.format(self.nameTA)

class Agreement(models.Model):

    origin = models.ForeignKey(Origin, null=True, blank=True, on_delete=models.CASCADE)
    numberAg = models.CharField(max_length=100)
    descriptionAg = models.TextField() 
    dateAg  = models.DateField()
    typeAgreement = models.ForeignKey(TypeAgreement, null=False, blank=True, on_delete=models.CASCADE)

class Inform(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    nameI = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

class InformDetall(models.Model):

    inform = models.ForeignKey(Inform, null=True, blank=True, on_delete=models.CASCADE)
    codeInfD = models.CharField(max_length=100)
    descriptionInfD = models.TextField() 

class Detall(models.Model):

    informDetall = models.ForeignKey(InformDetall, null=True, blank=True, on_delete=models.CASCADE)
    descriptionInfD = models.CharField(max_length=100)


class Rubro(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    origin =  models.ForeignKey(Origin, null=True, blank=True, on_delete=models.CASCADE)
    rubro = models.CharField(max_length=100)
    ccpet = models.BooleanField(null=True, blank=True,)
    rubroFather = models.BigIntegerField(null=True)
    nivel = models.IntegerField()
    description = models.TextField() 
    dateCreation = models.DateField()
    initialBudget = models.BigIntegerField()
    typeRubro = models.CharField(max_length=100)
    inform = models.ManyToManyField(Inform)
    informdetall = models.ManyToManyField(InformDetall)
    realBudget = models.BigIntegerField()
    budgetEject = models.BigIntegerField()
    imported =  models.CharField(max_length=100, null=True)

class Movement(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    agreement = models.ForeignKey(Agreement, null=True, blank=True, on_delete=models.CASCADE)
    nameRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, blank=True, null=True)  
    concept = models.CharField(max_length=100)
    value = models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()
    disponibility = models.BigIntegerField(null=True)
    register = models.BigIntegerField(null=True)
    obligation = models.BigIntegerField(null=True)
    vouchePayment = models.BigIntegerField(null=True)
    origin =  models.ForeignKey(Origin, null=True, blank=True, on_delete=models.CASCADE)
    budgetEject = models.BigIntegerField(null=True)
    observation = models.TextField(null=True)
    agreementNameAg = models.BigIntegerField(null=True)

class RubroMovement(models.Model):


    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    value = models.BigIntegerField()
    valueP =  models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()
    nameRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, blank=True, null=True)  
    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.CASCADE)

class RubroBalanceOperation(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.CASCADE)
    nameRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, blank=True, null=True) 
    typeOperation = models.CharField(max_length=100)
    value =  models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()

class Voucher(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    name =  models.CharField(max_length=100)
    description = models.TextField()
    order =  models.IntegerField()
    number =  models.IntegerField()
    category = models.CharField(max_length=100)
    dateCreation = models.DateField()

class Third(models.Model):
    
    CHOICES = [('Cédula de Ciudadanía', 'Cédula de Ciudadanía'), ('Cédula Extranjeria', 'Cédula Extrangeria'), ('Pasaporte', 'Pasaporte')]
    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    typeIdentification = models.CharField(max_length=64, choices=CHOICES)
    identification = models.BigIntegerField()
    name =  models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    reason =  models.CharField(max_length=100)
    phone =  models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    
class TypeContract(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    nameTC = models.CharField(max_length=100)
    description = models.TextField()

class TypeContractDetail(models.Model):

    typeContract = models.ForeignKey(TypeContract, null=True, blank=True, on_delete=models.CASCADE)
    codeTypeC = models.CharField(max_length=100)
    descriptionTypeC = models.TextField() 
    value = models.CharField(max_length=100)
    digitstc = models.CharField(max_length=10,null=True, blank=True,)

class Account(models.Model):

    CHOICES = [('Activo','Activo'),('Inactivo', 'Inactivo')]
    CHOICES2 = [('CORRIENTE','CORRIENTE'),('NOCORRIENTE', 'NOCORRIENTE')]
    CHOICES3 = [('M','M'),('A', 'A')]

    accountPeriod = models.ForeignKey(AccountPeriod, null=False, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    state = models.CharField(max_length=100,choices=CHOICES)
    corriente = models.CharField(max_length=100)
    nature = models.CharField(max_length=100)
    typeAccount = models.CharField(max_length=100,choices=CHOICES3)
    dateCreation = models.DateField(auto_now_add=True)
    level = models.IntegerField()
    accountFather = models.BigIntegerField(null=True)


    def __str__(self):
        return '{}'.format(self.code + "  "+ self.description) 

class AccountTypeRubro(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    rubro = models.ForeignKey(Rubro, null=True, blank=True, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    typeAccount = models.CharField(max_length=100)
    document = models.CharField(max_length=100)

class ValuesAccountObligation(models.Model):

    account = models.ForeignKey(AccountTypeRubro, null=True, blank=True, on_delete=models.CASCADE)
    obligation = models.ForeignKey(RubroMovement, null=True, blank=True, on_delete=models.CASCADE)
    typeAccount = models.CharField(max_length=100)
    value = models.BigIntegerField(null=True)
    payment_value = models.BooleanField(blank=True, null=True)

class InformationMovement(models.Model):

    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.CASCADE)
    typeMovement =  models.CharField(max_length=100)
    third = models.ForeignKey(Third, null=True, blank=True, on_delete=models.CASCADE)
    RightsEconomic = models.BooleanField()
    
class InformBank(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    nameI = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    digitI = models.BigIntegerField()

class InformBankDetall(models.Model):

    inform = models.ForeignKey(InformBank, null=True, blank=True, on_delete=models.CASCADE)
    codeInfD = models.CharField(max_length=100)
    descriptionInfD = models.TextField() 
    activity = models.CharField(max_length=100)


class OtherDiscount(models.Model):

    name =  models.CharField(max_length=100)
 
class Discount(models.Model):

    CHOICES2 = [('PORCENTAJE RANGO','PORCENTAJE RANGO'),('PORCENTAJE', 'PORCENTAJE'),('FIJO','FIJO'),('FIJO RANGO', 'FIJO RANGO')]
    CHOICES =  [('MANUAL','MANUAL'),('AUTOMATICO', 'AUTOMATICO')]
    CHOICES3 = [('SALUD','SALUD'),('RETENCION', 'RETENCION'),('OTROS','OTROS')]
    CHOICES4 = [('COMPROBANTE','COMPROBANTE'),('REGISTRO', 'REGISTRO')]

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    name =  models.CharField(max_length=100)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    typeDiscount = models.TextField(max_length=100,choices=CHOICES2)
    state = models.CharField(max_length=100,choices=CHOICES)
    acumulate = models.CharField(max_length=100,choices=CHOICES3)
    baseCalculate = models.CharField(max_length=100,choices=CHOICES4)
    average = models.FloatField()
    initialValue = models.BigIntegerField(null=True)
    finalValue = models.BigIntegerField(null=True)
    acumulateOther=  models.ForeignKey(OtherDiscount, null=True, blank=True, on_delete=models.CASCADE)

class DiscountMovement(models.Model):

    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.CASCADE)
    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.CASCADE)
    base = models.BigIntegerField(null=True)
    value = models.BigIntegerField(null=True)

class MovementAcount(models.Model):

    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    debito = models.BigIntegerField(null=True)
    credito = models.BigIntegerField(null=True)

class RubroInform(models.Model):
    rubro = models.ForeignKey(Rubro,  null=True, blank=True, on_delete=models.CASCADE)
    inform = models.ForeignKey(Inform, null=True, blank=True, on_delete=models.CASCADE)



class RubroInformdetall(models.Model):
    rubro = models.ForeignKey(Rubro, null=True, blank=True, on_delete=models.CASCADE)
    informdetall = models.ForeignKey(InformDetall, null=True, blank=True,on_delete=models.CASCADE)
    detall = models.ForeignKey(Detall, null=True, blank=True, on_delete=models.CASCADE)

class typeDocument(models.Model):
    codigo = models.CharField(max_length=2)
    description = models.CharField(max_length=100)
    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    accountPeriod = models.ForeignKey(AccountPeriod, null=True, blank=True, on_delete=models.CASCADE)


class TypeContractMovement(models.Model):
    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.CASCADE)
    typeContractdetail = models.ForeignKey(TypeContractDetail, null=True, blank=True, on_delete=models.CASCADE)

class ClosedPeriod(models.Model):
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100,null=True, blank=True,)
    activate = models.BooleanField()
    accountPeriod = models.ForeignKey(AccountPeriod, null=True, blank=True, on_delete=models.CASCADE)


class CCPET(models.Model):
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=100,null=True, blank=True)
    description = models.CharField(max_length=2000,null=True, blank=True)
    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)