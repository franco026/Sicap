# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class BudgetsAccount(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    corriente = models.CharField(max_length=100)
    nature = models.CharField(max_length=100)
    typeaccount = models.CharField(db_column='typeAccount', max_length=100)  # Field name made lowercase.
    datecreation = models.DateField(db_column='dateCreation')  # Field name made lowercase.
    level = models.IntegerField()
    accountfather = models.BigIntegerField(db_column='accountFather', blank=True, null=True)  # Field name made lowercase.
    accountperiod = models.ForeignKey('BudgetsAccountperiod', models.DO_NOTHING, db_column='accountPeriod_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'budgets_account'


class BudgetsAccountperiod(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    initialdate = models.DateField(db_column='initialDate')  # Field name made lowercase.
    finaldate = models.DateField(db_column='finalDate')  # Field name made lowercase.
    bussines = models.ForeignKey('BudgetsBussines', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_accountperiod'


class BudgetsAccounttyperubro(models.Model):
    typeaccount = models.CharField(db_column='typeAccount', max_length=100)  # Field name made lowercase.
    document = models.CharField(max_length=100)
    account = models.ForeignKey(BudgetsAccount, models.DO_NOTHING, blank=True, null=True)
    bussines = models.ForeignKey('BudgetsBussines', models.DO_NOTHING, blank=True, null=True)
    rubro = models.ForeignKey('BudgetsRubro', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_accounttyperubro'


class BudgetsAgreement(models.Model):
    numberag = models.CharField(db_column='numberAg', max_length=100)  # Field name made lowercase.
    descriptionag = models.TextField(db_column='descriptionAg')  # Field name made lowercase.
    dateag = models.DateField(db_column='dateAg')  # Field name made lowercase.
    origin = models.ForeignKey('BudgetsOrigin', models.DO_NOTHING, blank=True, null=True)
    typeagreement = models.ForeignKey('BudgetsTypeagreement', models.DO_NOTHING, db_column='typeAgreement_id')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'budgets_agreement'


class BudgetsBussines(models.Model):
    name = models.CharField(unique=True, max_length=100)
    nit = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    representative = models.CharField(max_length=100)
    rubropattern = models.CharField(db_column='rubroPattern', max_length=100)  # Field name made lowercase.
    accountpattern = models.CharField(db_column='accountPattern', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'budgets_bussines'


class BudgetsDiscount(models.Model):
    name = models.CharField(max_length=100)
    typediscount = models.TextField(db_column='typeDiscount')  # Field name made lowercase.
    state = models.CharField(max_length=100)
    acumulate = models.CharField(max_length=100)
    basecalculate = models.CharField(db_column='baseCalculate', max_length=100)  # Field name made lowercase.
    average = models.FloatField()
    initialvalue = models.BigIntegerField(db_column='initialValue', blank=True, null=True)  # Field name made lowercase.
    finalvalue = models.BigIntegerField(db_column='finalValue', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(BudgetsAccount, models.DO_NOTHING, blank=True, null=True)
    acumulateother = models.ForeignKey('BudgetsOtherdiscount', models.DO_NOTHING, db_column='acumulateOther_id', blank=True, null=True)  # Field name made lowercase.
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_discount'


class BudgetsDiscountmovement(models.Model):
    base = models.BigIntegerField(blank=True, null=True)
    value = models.BigIntegerField(blank=True, null=True)
    discount = models.ForeignKey(BudgetsDiscount, models.DO_NOTHING, blank=True, null=True)
    movement = models.ForeignKey('BudgetsMovement', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_discountmovement'


class BudgetsInform(models.Model):
    namei = models.CharField(db_column='nameI', max_length=100)  # Field name made lowercase.
    category = models.CharField(max_length=100)
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_inform'


class BudgetsInformationmovement(models.Model):
    typemovement = models.CharField(db_column='typeMovement', max_length=100)  # Field name made lowercase.
    rightseconomic = models.BooleanField(db_column='RightsEconomic')  # Field name made lowercase.
    movement = models.ForeignKey('BudgetsMovement', models.DO_NOTHING, blank=True, null=True)
    third = models.ForeignKey('BudgetsThird', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_informationmovement'


class BudgetsInformbank(models.Model):
    namei = models.CharField(db_column='nameI', max_length=100)  # Field name made lowercase.
    category = models.CharField(max_length=100)
    digiti = models.BigIntegerField(db_column='digitI')  # Field name made lowercase.
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_informbank'


class BudgetsInformbankdetall(models.Model):
    codeinfd = models.CharField(db_column='codeInfD', max_length=100)  # Field name made lowercase.
    descriptioninfd = models.TextField(db_column='descriptionInfD')  # Field name made lowercase.
    activity = models.CharField(max_length=100)
    inform = models.ForeignKey(BudgetsInformbank, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_informbankdetall'


class BudgetsInformdetall(models.Model):
    codeinfd = models.CharField(db_column='codeInfD', max_length=100)  # Field name made lowercase.
    descriptioninfd = models.TextField(db_column='descriptionInfD')  # Field name made lowercase.
    activity = models.CharField(max_length=100)
    inform = models.ForeignKey(BudgetsInform, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_informdetall'


class BudgetsMovement(models.Model):# Field name made lowercase.
    concept = models.CharField(max_length=100)
    value = models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()
    disponibility = models.BigIntegerField(blank=True, null=True)
    register = models.BigIntegerField(blank=True, null=True)
    obligation = models.BigIntegerField(blank=True, null=True)
    vouchepayment = models.BigIntegerField(db_column='vouchePayment', blank=True, null=True)  # Field name made lowercase.
    budgeteject = models.BigIntegerField(db_column='budgetEject', blank=True, null=True)  # Field name made lowercase.
    observation = models.TextField(blank=True, null=True)
    agreement = models.ForeignKey(BudgetsAgreement, models.DO_NOTHING, blank=True, null=True)
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)
    origin = models.ForeignKey('BudgetsOrigin', models.DO_NOTHING, blank=True, null=True)
    agreementnameag = models.BigIntegerField(db_column='agreementNameAg', blank=True, null=True)  # Field name made lowercase.
    nameRubro = models.ForeignKey('BudgetsRubro', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_movement'


class BudgetsMovementacount(models.Model):
    debito = models.BigIntegerField(blank=True, null=True)
    credito = models.BigIntegerField(blank=True, null=True)
    account = models.ForeignKey(BudgetsAccount, models.DO_NOTHING, blank=True, null=True)
    movement = models.ForeignKey(BudgetsMovement, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_movementacount'


class BudgetsOperation(models.Model):
    codeop = models.CharField(db_column='codeOp', max_length=2)  # Field name made lowercase.
    nameop = models.CharField(db_column='nameOp', max_length=100)  # Field name made lowercase.
    descriptionop = models.TextField(db_column='descriptionOp')  # Field name made lowercase.
    operation = models.CharField(max_length=10)
    orderop = models.IntegerField(db_column='orderOp')  # Field name made lowercase.
    contraoperar = models.BigIntegerField(db_column='contraOperar', blank=True, null=True)  # Field name made lowercase.
    contraoperarname = models.CharField(db_column='contraOperarName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contraorigin = models.BigIntegerField(db_column='contraOrigin', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'budgets_operation'


class BudgetsOperationOrigin(models.Model):
    operation = models.ForeignKey(BudgetsOperation, models.DO_NOTHING)
    origin = models.ForeignKey('BudgetsOrigin', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'budgets_operation_origin'
        unique_together = (('operation', 'origin'),)


class BudgetsOrigin(models.Model):
    nameorigin = models.CharField(db_column='nameOrigin', max_length=100)  # Field name made lowercase.
    codeorigin = models.CharField(db_column='codeOrigin', max_length=100)  # Field name made lowercase.
    descriptionorigin = models.TextField(db_column='descriptionOrigin')  # Field name made lowercase.
    orderorigin = models.IntegerField(db_column='orderOrigin')  # Field name made lowercase.
    finaldateorigin = models.DateField(db_column='finalDateOrigin')  # Field name made lowercase.
    pattern = models.CharField(db_column='pattern', max_length=100, null=True)

    accountperiod = models.ForeignKey(BudgetsAccountperiod, models.DO_NOTHING, db_column='accountPeriod_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'budgets_origin'


class BudgetsOtherdiscount(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'budgets_otherdiscount'


class BudgetsRubro(models.Model):
    rubro = models.CharField(max_length=100)
    ccpet = models.BooleanField(null=True, blank=True,)
    rubrofather = models.BigIntegerField(db_column='rubroFather', blank=True, null=True)  # Field name made lowercase.
    nivel = models.IntegerField()
    description = models.TextField()
    datecreation = models.DateField(db_column='dateCreation')  # Field name made lowercase.
    initialbudget = models.BigIntegerField(db_column='initialBudget')  # Field name made lowercase.
    typerubro = models.CharField(db_column='typeRubro', max_length=100)  # Field name made lowercase.
    realbudget = models.BigIntegerField(db_column='realBudget')  # Field name made lowercase.
    budgeteject = models.BigIntegerField(db_column='budgetEject')  # Field name made lowercase.
    imported = models.CharField(max_length=100, blank=True, null=True)
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)
    origin = models.ForeignKey(BudgetsOrigin, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_rubro'


class BudgetsRubroInform(models.Model):
    rubro = models.ForeignKey(BudgetsRubro, models.DO_NOTHING)
    inform = models.ForeignKey(BudgetsInform, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'budgets_rubro_inform'
        unique_together = (('rubro', 'inform'),)


class BudgetsRubroInformdetall(models.Model):
    rubro = models.ForeignKey(BudgetsRubro, models.DO_NOTHING)
    informdetall = models.ForeignKey(BudgetsInformdetall, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'budgets_rubro_informdetall'
        unique_together = (('rubro', 'informdetall'),)


class BudgetsRubrobalanceoperation(models.Model):
    typeoperation = models.CharField(db_column='typeOperation', max_length=100)  # Field name made lowercase.
    value = models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()
    nameRubro = models.ForeignKey(BudgetsRubro, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)
    movement = models.ForeignKey(BudgetsMovement, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_rubrobalanceoperation'


class BudgetsRubromovement(models.Model):
    value = models.BigIntegerField()
    valuep = models.BigIntegerField(db_column='valueP')  # Field name made lowercase.
    balance = models.BigIntegerField()
    date = models.DateField()
    nameRubro = models.ForeignKey(BudgetsRubro, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)
    movement = models.ForeignKey(BudgetsMovement, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_rubromovement'


class BudgetsThird(models.Model):
    typeidentification = models.CharField(db_column='typeIdentification', max_length=64)  # Field name made lowercase.
    identification = models.BigIntegerField()
    name = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_third'


class BudgetsTypeagreement(models.Model):
    codeta = models.CharField(db_column='codeTA', max_length=100)  # Field name made lowercase.
    nameta = models.CharField(db_column='nameTA', max_length=100)  # Field name made lowercase.
    descriptionta = models.TextField(db_column='descriptionTA')  # Field name made lowercase.
    ordenta = models.IntegerField(db_column='ordenTA')  # Field name made lowercase.
    validacionta = models.CharField(db_column='validacionTA', max_length=100)  # Field name made lowercase.
    mensajeta = models.CharField(db_column='mensajeTA', max_length=100)  # Field name made lowercase.
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_typeagreement'


class BudgetsTypecontract(models.Model):
    nametc = models.CharField(db_column='nameTC', max_length=100)  # Field name made lowercase.
    description = models.TextField()
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_typecontract'


class BudgetsTypecontractdetail(models.Model):
    codetypec = models.CharField(db_column='codeTypeC', max_length=100)  # Field name made lowercase.
    descriptiontypec = models.TextField(db_column='descriptionTypeC')  # Field name made lowercase.
    value = models.CharField(max_length=100)
    digitstc = models.BigIntegerField(db_column='digitsTC') 
    typecontract = models.ForeignKey(BudgetsTypecontract, models.DO_NOTHING, db_column='typeContract_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'budgets_typecontractdetail'


class BudgetsValuesaccountobligation(models.Model):
    typeaccount = models.CharField(db_column='typeAccount', max_length=100)  # Field name made lowercase.
    value = models.BigIntegerField(blank=True, null=True)
    account = models.ForeignKey(BudgetsAccounttyperubro, models.DO_NOTHING, blank=True, null=True)
    obligation = models.ForeignKey(BudgetsRubromovement, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_valuesaccountobligation'


class BudgetsVoucher(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField()
    number = models.IntegerField()
    category = models.CharField(max_length=100)
    datecreation = models.DateField(db_column='dateCreation')  # Field name made lowercase.
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_voucher'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class UsersUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    typeidentification = models.CharField(db_column='typeIdentification', max_length=64)  # Field name made lowercase.
    identification = models.BigIntegerField()
    genre = models.CharField(max_length=64)
    typeuser = models.CharField(db_column='typeUser', max_length=64)  # Field name made lowercase.
    address = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    observation = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'users_user'


class UsersUserGroups(models.Model):
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_groups'
        unique_together = (('user', 'group'),)


class UsersUserUserPermissions(models.Model):
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_user_permissions'
        unique_together = (('user', 'permission'),)



class  BudgetstypeDocument(models.Model):
    codigo = models.CharField(max_length=2)
    description = models.CharField(max_length=100)
    bussines = models.ForeignKey(BudgetsBussines,  models.DO_NOTHING, blank=True, null=True)
    accountPeriod = models.ForeignKey(BudgetsAccountperiod, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_typeDocument'

class  BudgetstypeContractMovement(models.Model):
    
    movement = models.ForeignKey('BudgetsMovement', models.DO_NOTHING, blank=True, null=True)
    typecontractdetail = models.ForeignKey('BudgetsTypecontractdetail', models.DO_NOTHING, db_column='typecontractdetail_id', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'budgets_typeContractMovement'


class  BudgetsClosedPeriod(models.Model):
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100,blank=True, null=True)
    activate = models.BooleanField()
    accountPeriod = models.ForeignKey(BudgetsAccountperiod, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_ClosedPeriod'

class BudgetsCCPET(models.Model):
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=100,null=True, blank=True)
    description = models.CharField(max_length=2000,null=True, blank=True)
    bussines = models.ForeignKey(BudgetsBussines, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets_CCPET'

