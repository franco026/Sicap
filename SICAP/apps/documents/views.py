from copyreg import constructor
from django.db import connections
from django.forms.models import construct_instance
from django.shortcuts import render
from apps.documents.models import *
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from apps.documents.forms import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime, date, timedelta
import simplejson as json
from tablib import Dataset 
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#///////////////Document tatan
class ListVoucher(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = Voucher
    queryset= model.objects.order_by('name')
    template_name = 'documents/listVoucher.html'

    def get_context_data(self):
        context = super(ListVoucher, self).get_context_data()
        context['voucherForm'] = VoucherForm
        context['voucherUpdateForm'] = ByVoucherUpdate
        return context  

    def get_queryset(self):
        queryset = super(ListVoucher, self).get_queryset()
        return Voucher.objects.filter(bussines_id=self.kwargs['pk'])
        
class CreateVoucher(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        today = datetime.now()
        bussinesId= request.GET.get('bussines')
        code = request.GET.get('code').upper()
        name = request.GET.get('name').upper()
        description = request.GET.get('description').upper()
        order = request.GET.get('order')
        number = request.GET.get('number')
        category = request.GET.get('category').upper()
 
        bussines = Bussines.objects.get(id=bussinesId)
        voucherExist = Voucher.objects.filter(name=name, bussines_id=bussinesId).exists()
        if voucherExist == False:
            newVoucher = Voucher.objects.create(
                bussines=bussines, code=code, name=name, description=description, order=order, number=int(number), category=category, dateCreation=today
            )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class UpdateVoucher(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs): 
        
        updateVoucher = Voucher.objects.get(id=request.GET.get('id'))
        code = request.GET.get('code').upper()
        if request.GET.get('equalName') == 'TRUE':
            
            updateVoucher.code = request.GET.get('code').upper()
            updateVoucher.name = request.GET.get('name').upper()
            updateVoucher.description = request.GET.get('description').upper()
            updateVoucher.order = request.GET.get('order')
            updateVoucher.number = request.GET.get('number')
            updateVoucher.category = request.GET.get('category').upper()  
            updateVoucher.save()     
            return JsonResponse({'CREATE':"TRUE"})
        else:
            voucherExist = Voucher.objects.filter(code=code, bussines_id=request.GET.get('bussinesId')).exists()
            if voucherExist == False:
               
                updateVoucher.code = request.GET.get('code').upper()
                updateVoucher.name = request.GET.get('name').upper()
                updateVoucher.description = request.GET.get('description').upper()
                updateVoucher.order = request.GET.get('order')
                updateVoucher.number = request.GET.get('number')
                updateVoucher.category = request.GET.get('category').upper()  
                updateVoucher.save()  
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"}) 
        
def generateDocuments(request,pkUser):

    thirdForm = ThirdForm()
    context = {'thirdForm': thirdForm } 
    return render(request, 'documents/generateDocuments.html',context)

class GetVoucher(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        if request.GET.get('option') == '1':
            bussinesId= request.GET.get('idBussines')
            voucher = Voucher.objects.filter(bussines_id=bussinesId).values('name')
            return JsonResponse({"VH": list(voucher)})
        elif request.GET.get('option') == '2':
            bussinesId= request.GET.get('idBussines')
            accountPeriod =  AccountPeriod.objects.get(bussines_id=bussinesId, name=request.GET.get('nameAC'))
            origin = Origin.objects.filter(accountPeriod_id=accountPeriod.id).exclude(nameOrigin='INGRESOS').values('nameOrigin')
            return JsonResponse({"OR": list(origin)})
        elif request.GET.get('option') == '3':
            bussinesId= request.GET.get('idBussines')
            accountPeriod =  AccountPeriod.objects.get(bussines_id=bussinesId, name=request.GET.get('nameAC'))
            origin = Origin.objects.get(accountPeriod_id=accountPeriod.id, nameOrigin=request.GET.get('origin'))
            return JsonResponse({"ID": origin.id})
        else:
            return JsonResponse({"else": "true"})

class ListThird(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = Third
    queryset= model.objects.order_by('name')
    template_name = 'documents/listThird.html'

    def get_context_data(self):
        context = super(ListThird, self).get_context_data()
        context['thirdForm'] = ThirdForm
        context['byThirdUpdateForm'] = ByThirdUpdate
        return context  

    def get_queryset(self):
        queryset = super(ListThird, self).get_queryset()
        return Third.objects.filter(bussines_id=self.kwargs['pk'])
        
class CreateThird(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        
        bussinesId= request.GET.get('bussines')
        typeIdentification = request.GET.get('typeIdentification').upper()
        identification = request.GET.get('identification')
        name = request.GET.get('name').upper()
        surnames = request.GET.get('surnames').upper()
        reason = request.GET.get('reason').upper()
        phone = request.GET.get('phone')
        city = request.GET.get('city').upper()
 
        bussines = Bussines.objects.get(id=bussinesId)
        thirdExist = Third.objects.filter(identification=identification, bussines_id=bussinesId).exists()
        if thirdExist == False:
            newThird = Third.objects.create(
                bussines=bussines, typeIdentification=typeIdentification, identification=identification, name=name, surnames=surnames, reason=reason, phone=phone, city=city
            )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class UpdateThird(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs):
 
        updateThird = Third.objects.get(id=request.GET.get('id'))
        identification = request.GET.get('identification')
        if request.GET.get('equalName') == 'TRUE':
            
            updateThird.typeIdentification = request.GET.get('typeIdentification').upper()
            updateThird.identification = request.GET.get('identification')
            updateThird.name = request.GET.get('name').upper()
            updateThird.surnames = request.GET.get('surnames').upper()
            updateThird.reason = request.GET.get('reason').upper()
            updateThird.phone = request.GET.get('phone')
            updateThird.city = request.GET.get('city').upper()  
            updateThird.save()     
            return JsonResponse({'UPDATE':"TRUE"})
        else:
            thirdExist = Third.objects.filter(identification=identification, bussines_id=request.GET.get('bussinesId')).exists()
            if thirdExist == False:

                updateThird.typeIdentification = request.GET.get('typeIdentification').upper()
                updateThird.identification = request.GET.get('identification')
                updateThird.name = request.GET.get('name').upper()
                updateThird.surnames = request.GET.get('surnames').upper()
                updateThird.reason = request.GET.get('reason').upper()
                updateThird.phone = request.GET.get('phone')
                updateThird.city = request.GET.get('city').upper()  
                updateThird.save()  
                return JsonResponse({'UPDATE':"TRUE"})
            else:
                return JsonResponse({'UPDATE':"FALSE"}) 

class ListTypeContract(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = TypeContract
    queryset= model.objects.order_by('name')
    template_name = 'documents/listTypeContract.html'

    def get_context_data(self):
        context = super(ListTypeContract, self).get_context_data()
        context['typeContractForm'] = TypeContractForm
        context['typeContractDetailForm'] = TypeContractDetailForm
        context['byTypeContractUpdateForm'] = ByTypeContractUpdate
        
        return context  

    def get_queryset(self):
        queryset = super(ListTypeContract, self).get_queryset()
        return TypeContract.objects.filter(bussines_id=self.kwargs['pk'])
        
class CreateTypeContract(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        bussinesId= request.GET.get('bussines')
        nameTC = request.GET.get('nameTC').upper()
        description = request.GET.get('description')
    
        bussines = Bussines.objects.get(id=bussinesId)
        typeContractExist = TypeContract.objects.filter(nameTC=nameTC, bussines_id=bussinesId).exists()
        if typeContractExist == False:
            newtypeContract = TypeContract.objects.create(
                bussines=bussines, nameTC=nameTC, description=description,
            )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class CreateDetailTypeContract(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        codeTypeC=request.GET.get('codeTypeC')
        typeContract = TypeContract.objects.get(id=request.GET.get('typeContractId'))
        detailTypeContractExist = TypeContractDetail.objects.filter(codeTypeC=codeTypeC.upper(), typeContract_id=typeContract.id).exists()
        if detailTypeContractExist == False:
            newIdetailTypeContract = TypeContractDetail.objects.create(
            typeContract= typeContract, 
            codeTypeC=codeTypeC.upper(), 
            descriptionTypeC=request.GET.get('descriptionTypeC').upper(), 
        )
            detalle= {'id':newIdetailTypeContract.id,'codeTypeC':newIdetailTypeContract.codeTypeC}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})



class ManageDetallTypeContract(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        dataDetall=json.loads(request.GET.get('newData'))
        for x in range(0,len(dataDetall)):
            data = TypeContractDetail.objects.get(id= dataDetall[x]['idDetall'])
            data.value = dataDetall[x]['value']
            data.digitstc = dataDetall[x]['digit']
            data.save()

        return JsonResponse({'CREATE':"TRUE"})

class ManageTypeContract(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        typeContract = TypeContract.objects.get(id=request.GET.get('typeContractId'))
        detailTypeContractExist = TypeContractDetail.objects.filter(typeContract_id=typeContract.id).exists()
        detailTypeContract = TypeContractDetail.objects.filter(typeContract_id=typeContract.id).values('id','typeContract','codeTypeC','descriptionTypeC','value','digitstc')
        if detailTypeContractExist == True:
            return JsonResponse({'CREATE':"TRUE",'LT': list(detailTypeContract)})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class UpdateTypeContract(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs): 

 
        updateTypeContract = TypeContract.objects.get(id=request.GET.get('id'))
        nameTC = request.GET.get('nameTC').upper()
        if request.GET.get('equalName') == 'TRUE':
            
            updateTypeContract.nameTC = request.GET.get('nameTC').upper()
            updateTypeContract.description = request.GET.get('description').upper()
            updateTypeContract.categoryTC = request.GET.get('categoryTC').upper()
            updateTypeContract.digitsTC = request.GET.get('digitsTC').upper()
            updateTypeContract.save()     
            return JsonResponse({'CREATE':"TRUE"})
        else:
            typeContractExist = TypeContract.objects.filter(nameTC=nameTC, bussines_id=request.GET.get('bussinesId')).exists()
            if typeContractExist == False:

                updateTypeContract.nameTC = request.GET.get('nameTC').upper()
                updateTypeContract.description = request.GET.get('description').upper()
                updateTypeContract.categoryTC = request.GET.get('categoryTC').upper()
                updateTypeContract.digitsTC = request.GET.get('digitsTC').upper()
                updateTypeContract.save()  
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"})

class GetDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
    
        today = datetime.strptime(request.GET.get('dateCreateDP'), '%Y-%m-%d')
        print(today)
        disponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        if disponibility == False:
            disponibilityFormat = str(today.year) + str(today.month)+str(today.day)+str(0)
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="DISPONIBILIDAD").values('id','value','balance','disponibility','observation','date')
            return JsonResponse({"DI": disponibilityFormat,"MV": list(movements)})
        else:        
            lastDisponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="DISPONIBILIDAD").values('id','value','balance','disponibility','observation','date')
            
            return JsonResponse({"DI": lastDisponibility.disponibility+1,"MV": list(movements)})


class CreateDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        today = datetime.now()
        disponibilitys = json.loads(request.GET.get('disponibilitys'))
        bussines=Bussines.objects.get(id=request.GET.get('bussines'))
        disponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        if disponibility == False:
            disponibilityFormat = str(today.year) + str(today.month)+str(today.day)+str(0)
            newDisponibility = Movement.objects.create(
                bussines=bussines,concept="DISPONIBILIDAD",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=request.GET.get('date'),disponibility=request.GET.get('disponibilityCode'),origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            for x in range(0,len(disponibilitys)):
                rubroBalanceOperation = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation='DISPONIBILIDAD',value=disponibilitys[x]['value'],balance=disponibilitys[x]['value'],date=today,nameRubro_id=disponibilitys[x]['id'],movement=newDisponibility) 
                rubroMov = RubroMovement.objects.create(bussines=bussines,value=disponibilitys[x]['value'],valueP=0,balance=disponibilitys[x]['value'],date=today,nameRubro_id=disponibilitys[x]['id'],movement=newDisponibility) 
                rubro = Rubro.objects.get(id=disponibilitys[x]['id'])
                rubro.budgetEject = disponibilitys[x]['balance']
                rubro.save()
            return JsonResponse({"CREATE": "TRUE","ID":newDisponibility.id,"DP": request.GET.get('disponibilityCode')})
        else:        

            lastDisponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            newDisponibility = Movement.objects.create(
                bussines=bussines,concept="DISPONIBILIDAD",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=request.GET.get('date'),disponibility=lastDisponibility.disponibility+1,origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            print(newDisponibility)
            for x in range(0,len(disponibilitys)):
                
                rubroMov = RubroMovement.objects.create(bussines=bussines,value=disponibilitys[x]['value'],valueP=0,balance=disponibilitys[x]['value'],date=today,nameRubro_id=disponibilitys[x]['id'],movement=newDisponibility) 
                rubroBalanceOperation = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation='DISPONIBILIDAD',value=disponibilitys[x]['value'],balance=disponibilitys[x]['value'],date=today,nameRubro_id=disponibilitys[x]['id'],movement=newDisponibility) 
                rubro = Rubro.objects.get(id=disponibilitys[x]['id'])
                rubro.budgetEject = disponibilitys[x]['balance']
                rubro.save()
            return JsonResponse({"CREATE": "TRUE","ID":newDisponibility.id,"DP": request.GET.get('disponibilityCode')})

class GetDataToRegister(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        third = Third.objects.filter(bussines_id=request.GET.get('bussines')).values('name','surnames','id')        
        typeContract = TypeContract.objects.filter(bussines_id=request.GET.get('bussines')).values('nameTC','id')
        listContract = []
        count = 0
        for x in range(0,len(typeContract)):
            detall = TypeContractDetail.objects.filter(typeContract_id = typeContract[x]['id']).exists()
            """ detall2 = TypeContractDetail.objects.filter(typeContract_id = typeContract[x]['id']).values('value')
            
            for g in range(0,len(detall2)):
                print(detall2[g])
             """
            if detall :
                listContract.append(typeContract[x])
        
        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="DISPONIBILIDAD").values('disponibility','id')
        listMovement = []
        
        for x in range(0,len(movement)):

            rubroOperation = RubroBalanceOperation.objects.filter(movement_id = movement[x]['id']).values('movement_id','balance')
            cont = 0
            for v in range(0,len(rubroOperation)):

                if(rubroOperation[x]['balance'] == 0):
                    cont += 1

            if cont != 2:
                listMovement.append( movement[x])
            
        registers = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="REGISTRO").values('register','id','value','balance','observation','date')
        
        return JsonResponse({"TH": list(third), "TC":list(listContract),"MV":list(listMovement),"RG":list(registers)}) 

class GetDataRubroDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        rubroMovement = RubroMovement.objects.filter(nameRubro_id=request.GET.get('id'),movement__concept='DISPONIBILIDAD', date__gte=request.GET.get('initialDate'),date__lte=request.GET.get('finalDate')).values('movement__disponibility','value','balance','nameRubro','date')
        return JsonResponse({"DPRUBRO": list(rubroMovement)})

class GetOperationsByOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        origin = Origin.objects.get(nameOrigin=request.GET.get('originID'),accountPeriod_id=request.GET.get('accountPeriod'))
        operations = Operation.objects.filter(origin=origin.id).values('nameOp')
        return JsonResponse({"OP": list(operations)})

class GetDisponibilityRegister(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="DISPONIBILIDAD").values('disponibility','observation','value','balance','date','id')
        return JsonResponse({"DP": list(movement)})

class GetThirds(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        third = Third.objects.filter(bussines_id=request.GET.get('bussines')).values('id','name','surnames','typeIdentification','identification','phone')        
        return JsonResponse({"TH": list(third)})        

class FillDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        movement = Movement.objects.get(id=request.GET.get('disponibility'))
        movementRExist = Movement.objects.filter(disponibility=request.GET.get('disponibility')).exists()
        movementObli = Movement.objects.filter(disponibility=request.GET.get('disponibility')).values()
        
        rubroMovement = RubroMovement.objects.filter(movement_id=request.GET.get('disponibility')).values('id','value','nameRubro','valueP','balance')
        rubroList = []
        third = []
        
        for x in range(0,len(list(rubroMovement))):
            print(rubroMovement[x])
            if movementRExist :
                movementR = Movement.objects.filter(disponibility=request.GET.get('disponibility')).last()
                third = InformationMovement.objects.filter(movement_id = movementR.id ).values('third__id','third__name','third__surnames')
    
            rubro = Rubro.objects.get(id=list(rubroMovement)[x]['nameRubro'])
            rubroList.append({"idDispo":list(rubroMovement)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"value":list(rubroMovement)[x]['balance'],"valueP":list(rubroMovement)[x]['balance'],"Third": list(third) })
        
        

        return JsonResponse({"RUBRO":list(rubroList), "OBSERVATION": movement.observation,"DATE": movement.date})

class GetRegisterSerial(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
    
    
        today = datetime.strptime(request.GET.get('dateCreateDP'), '%Y-%m-%d')
        register = Movement.objects.filter(concept="REGISTRO", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()
        if register == False:
            registerFormat = str(1010)+str(today.year)+str(today.month)+str(today.day)+str(0)
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="REGISTRO").values('id','value','balance','register','observation')
            return JsonResponse({"RE": registerFormat,"MV": list(movements)})
        else:        
            lastRegister = Movement.objects.filter(concept="REGISTRO", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="REGISTRO").values('id','value','balance','register','observation')
            return JsonResponse({"RE": lastRegister.register+1,"MV": list(movements)})



class CreateRegister(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        today = datetime.now()
        registers = json.loads(request.GET.get('registers'))
        bussines=Bussines.objects.get(id=request.GET.get('bussines'))
        register = Movement.objects.filter(concept="REGISTRO", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        

        if register == False:
            registerFormat = str(1010)+str(today.year)+str(today.month)+str(today.day)+str(0)
            newRegister = Movement.objects.create(
                bussines=bussines,concept="REGISTRO",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=today,disponibility=request.GET.get('disponibility'),register=request.GET.get('registerCode'),origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            newInformationMovement = InformationMovement.objects.create(movement_id=newRegister.id, typeMovement='REGISTRO', third_id = request.GET.get('third'),RightsEconomic=True)
            newMovementContact = TypeContractMovement.objects.create(
                movement_id=newRegister.id,
                typeContractdetail_id = request.GET.get('contract')
            )
            for x in range(0,len(registers)):
                rubroBalanceOperation = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation='REGISTRO',value=registers[x]['value'],balance=registers[x]['value'],date=request.GET.get('date'),nameRubro_id=registers[x]['id'],movement=newRegister) 
                rubroMov = RubroMovement.objects.create(bussines=bussines,value=registers[x]['value'],valueP=0,balance=registers[x]['value'],date=request.GET.get('date'),nameRubro_id=registers[x]['id'],movement=newRegister) 
                print(registers[x]['idDispo'])
                disponibilityMove = RubroMovement.objects.get(id=registers[x]['idDispo'])
                disponibilityMove.valueP = disponibilityMove.valueP+registers[x]['value']
                disponibilityMove.balance = disponibilityMove.balance-registers[x]['value']
                disponibilityMove.save()

                disponibilityOpe = RubroBalanceOperation.objects.get(id=registers[x]['idDispo'])
                disponibilityOpe.balance = disponibilityOpe.balance-registers[x]['value']
                disponibilityOpe.save()
                
            return JsonResponse({"CREATE": "TRUE","ID":newRegister.id,"RG": newRegister.register})
        else:        
            lastRegister = Movement.objects.filter(concept="REGISTRO", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()            
            newRegister = Movement.objects.create(
                bussines=bussines,concept="REGISTRO",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=today,disponibility=request.GET.get('disponibility'),register=lastRegister.register+1,origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            newInformationMovement = InformationMovement.objects.create(movement_id=newRegister.id, typeMovement='REGISTRO', third_id = request.GET.get('third'),RightsEconomic=True)
            newMovementContact = TypeContractMovement.objects.create(
                movement_id=newRegister.id,
                typeContractdetail_id = request.GET.get('contract')
            )
            for x in range(0,len(registers)):
                
                rubroBalanceOperation = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation='REGISTRO',value=registers[x]['value'],balance=registers[x]['value'],date=request.GET.get('date'),nameRubro_id=registers[x]['id'],movement=newRegister)   
                rubroMov = RubroMovement.objects.create(bussines=bussines,value=registers[x]['value'],valueP=0,balance=registers[x]['value'],date=request.GET.get('date'),nameRubro_id=registers[x]['id'],movement=newRegister) 
                disponibilityMove = RubroMovement.objects.get(id=registers[x]['idDispo'])
                disponibilityMove.valueP = disponibilityMove.valueP+registers[x]['value']
                disponibilityMove.balance = disponibilityMove.balance-registers[x]['value']
                disponibilityMove.save()

                disponibilityOpe = RubroBalanceOperation.objects.get(id=registers[x]['idDispo'])
                disponibilityOpe.balance = disponibilityOpe.balance-registers[x]['value']
                disponibilityOpe.save()
            return JsonResponse({"CREATE": "TRUE","ID":newRegister.id,"RG": newRegister.register})


class GetDataToObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        third = Third.objects.filter(bussines_id=request.GET.get('bussines')).values('name','surnames','id')        
        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="REGISTRO").values('register','id')
        obligations = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="OBLIGACION").values('obligation','date','id','value','balance','observation','date')
        return JsonResponse({"TH": list(third),"MV":list(movement),"OB":list(obligations)}) 

class GetObligationSerial(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
    
        today = datetime.strptime(request.GET.get('dateCreateDP'), '%Y-%m-%d')
        obligation = Movement.objects.filter(concept="OBLIGACION", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        if obligation == False:
            obligationFormat = str(2020)+str(today.year)+str(today.month)+str(today.day)+str(0)
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="OBLIGACION").values('id','value','balance','obligation','observation')
            return JsonResponse({"OB": obligationFormat,"MV": list(movements)})
        else:        
            lastRegister = Movement.objects.filter(concept="OBLIGACION", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="OBLIGACION").values('id','value','balance','obligation','observation')
            return JsonResponse({"OB": lastRegister.obligation+1,"MV": list(movements)})

class FillObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        movement = Movement.objects.get(id=request.GET.get('obligation'))
        rubroMovement = RubroMovement.objects.filter(movement_id=request.GET.get('obligation')).values('movement__obligation','id','value','nameRubro','valueP')
        rubroList = []

        for x in range(0,len(list(rubroMovement))):

            rubro = Rubro.objects.get(id=list(rubroMovement)[x]['nameRubro'])
            rubroList.append({"obligation":list(rubroMovement)[x]['movement__obligation'],"idObligation":list(rubroMovement)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"value":list(rubroMovement)[x]['value'],"valueP":list(rubroMovement)[x]['valueP'] })

        return JsonResponse({"RUBRO":list(rubroList), "OBSERVATION": movement.observation,"DATE":movement.date})

class FillRegister(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        movement = Movement.objects.get(id=request.GET.get('register'))
        rubroMovement = RubroMovement.objects.filter(movement_id=request.GET.get('register')).values('movement__register','id','value','nameRubro','valueP')

        rubroList = []

        thirdRegiter = InformationMovement.objects.get(movement_id = movement.id)
        for x in range(0,len(list(rubroMovement))):

            rubro = Rubro.objects.get(id=list(rubroMovement)[x]['nameRubro'])
            rubroList.append({"register":list(rubroMovement)[x]['movement__register'],"idRegister":list(rubroMovement)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"value":list(rubroMovement)[x]['value'],"valueP":list(rubroMovement)[x]['valueP'] })

        return JsonResponse({"RUBRO":list(rubroList), "OBSERVATION": movement.observation,"DATE":movement.date,"THIRD":thirdRegiter.third_id})

class GetRegistersOB(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="REGISTRO").values('register','observation','value','balance','date','id')
        return JsonResponse({"RG": list(movement)})

class GetObligationsVC(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="OBLIGACION").values('obligation','observation','value','balance','date','id')
        return JsonResponse({"OB": list(movement)})

class CreateObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        today = datetime.now()
        obligations = json.loads(request.GET.get('obligations'))
        accounts = json.loads(request.GET.get('accounts'))
        bussines=Bussines.objects.get(id=request.GET.get('bussines'))
        obligation = Movement.objects.filter(concept="OBLIGACION", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()
        accountsCount = 0
        
        if request.GET.get('rightsEconomic')=="TRUE":
            rigths = True
        else: 
            rigths = False

        if obligation == False:
            obligationFormat = str(1010)+str(today.year)+str(today.month)+str(today.day)+str(0)
            newObligation = Movement.objects.create(
                bussines=bussines,concept="OBLIGACION",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=today,register=request.GET.get('register'),obligation=request.GET.get('obligationCode'),origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            newInformationMovement = InformationMovement.objects.create(movement_id=newObligation.id, typeMovement='OBLIGACION', third_id = request.GET.get('third'),RightsEconomic=rigths)

            if len(accounts)!=0:

                for x in range(0,len(obligations)):
                    rubroBalanceOperation = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation='OBLIGACION',value=obligations[x]['value'],balance=obligations[x]['value'],date=request.GET.get('date'),nameRubro_id=obligations[x]['id'],movement=newObligation)   
                    rubroMov = RubroMovement.objects.create(bussines=bussines,value=obligations[x]['value'],valueP=0,balance=obligations[x]['value'],date=request.GET.get('date'),nameRubro_id=obligations[x]['id'],movement=newObligation) 
                    registerMov = RubroMovement.objects.get(id=obligations[x]['idRegister'])
                    registerMov.valueP = registerMov.valueP+obligations[x]['value']
                    registerMov.balance = registerMov.balance-obligations[x]['value']
                    registerMov.save()


                    registerOpe = RubroBalanceOperation.objects.get(id=obligations[x]['idRegister'])
                    registerOpe.balance = registerOpe.balance-obligations[x]['value']
                    registerOpe.save()
                    for y in range(accountsCount,accountsCount+2):
                        valuesAccount = ValuesAccountObligation.objects.create(account_id=accounts[y]['obligationID'],obligation_id=rubroMov.id,typeAccount=accounts[y]['typeAccount'],value=accounts[y]['value'],payment_value=False)      
                    accountsCount =  accountsCount+2  

                
                return JsonResponse({"CREATE": "TRUE", "ID":newObligation.id})
            else:
                for x in range(0,len(obligations)):
                    rubroMov = RubroMovement.objects.create(bussines=bussines,value=obligations[x]['value'],valueP=0,balance=obligations[x]['value'],date=request.GET.get('date'),nameRubro_id=obligations[x]['id'],movement=newObligation) 
                    
                    register = RubroMovement.objects.get(id=obligations[x]['idRegister'])
                    register.valueP = register.valueP+obligations[x]['value']
                    register.balance = register.balance-obligations[x]['value']
                    register.save()


                    register = RubroBalanceOperation.objects.get(id=obligations[x]['idRegister'])
                    register.balance = register.balance-obligations[x]['value']
                    register.save()
                return JsonResponse({"CREATE": "TRUE", "ID":newObligation.id})          
        else:        
            lastObligation = Movement.objects.filter(concept="OBLIGACION", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            print(request.GET.get('register'))
            newObligation = Movement.objects.create(
                bussines=bussines,concept="OBLIGACION",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=today,register=request.GET.get('register'),obligation=lastObligation.obligation+1,origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            newInformationMovement = InformationMovement.objects.create(movement_id=newObligation.id, typeMovement='OBLIGACION', third_id = request.GET.get('third'),RightsEconomic=rigths)

            if len(accounts)!=0:
                print(obligations,"aqui")
                for x in range(0,len(obligations)):
                
                    rubroBalanceOperation = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation='OBLIGACION',value=obligations[x]['value'],balance=obligations[x]['value'],date=request.GET.get('date'),nameRubro_id=obligations[x]['id'],movement=newObligation)   
                    rubroMov = RubroMovement.objects.create(bussines=bussines,value=obligations[x]['value'],valueP=0,balance=obligations[x]['value'],date=request.GET.get('date'),nameRubro_id=obligations[x]['id'],movement=newObligation) 
                    registerMov = RubroMovement.objects.get(id=obligations[x]['idRegister'])
                    registerMov.valueP = registerMov.valueP+obligations[x]['value']
                    registerMov.balance = registerMov.balance-obligations[x]['value']
                    registerMov.save()


                    registerOpe = RubroBalanceOperation.objects.get(id=obligations[x]['idRegister'])
                    registerOpe.balance = registerOpe.balance-obligations[x]['value']
                    registerOpe.save()


                    for y in range(accountsCount,2):
                        valuesAccount = ValuesAccountObligation.objects.create(account_id=accounts[y]['obligationID'],obligation_id=rubroMov.id,typeAccount=accounts[y]['typeAccount'],value=accounts[y]['value'],payment_value=False)      
                    accountsCount =  accountsCount+2  
            else:
                for x in range(0,len(obligations)):
                
                    rubroMov = RubroMovement.objects.create(bussines=bussines,value=obligations[x]['value'],valueP=obligations[x]['value'],balance=obligations[x]['balance'],date=request.GET.get('date'),nameRubro_id=obligations[x]['id'],movement=newObligation) 
                    registerMov = RubroMovement.objects.get(id=obligations[x]['idRegister'])
                    registerMov.valueP = registerMov.valueP+obligations[x]['value']
                    registerMov.balance = registerMov.balance-obligations[x]['value']
                    registerMov.save()

            return JsonResponse({"CREATE": "TRUE","ID":newObligation.id})
 

class GetDataToVoucherPayment(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        third = Third.objects.filter(bussines_id=request.GET.get('bussines')).values('name','surnames','id')        
        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="OBLIGACION").values('register','id')
        obligations = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="VOUCHER").values('vouchePayment','id','value','balance','observation','date')
        return JsonResponse({"TH": list(third),"MV":list(movement),"VP":list(obligations)}) 

class GetAccountsByRubro(LoginRequiredMixin,View):
    
    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        accountsByRubro = AccountTypeRubro.objects.filter(rubro_id=request.GET.get('rubro')).values('id','rubro__id','account__code','account__description','typeAccount','document','account_id','account__typeAccount')        
        listAccount = []
        cantidad = 0
        for i in range(0, len(accountsByRubro)):
            print(accountsByRubro[i]['account__code'])
            mm = Account.objects.filter(code__startswith=accountsByRubro[i]['account__code']).values('id','typeAccount','description','code')

            print(list(mm))
            filter = accountAux(request, accountsByRubro[i]['account__typeAccount'],accountsByRubro[i]['account_id'],accountsByRubro[i]['account_id'],0)
            listAccount.append({
                "id": accountsByRubro[i]['id'],
                "typeAccount": accountsByRubro[i]['typeAccount'],
                "account": accountsByRubro[i]['account__code'],
                "description": accountsByRubro[i]['account__description'],
                "code": accountsByRubro[i]['account_id'],
                "document":  accountsByRubro[i]['document'],
                "account_id": accountsByRubro[i]['account_id'],
                "accounts": list(mm)
            })

            items_found = []
            for element in listAccount:
                if (not element in items_found):
                    # items_found acumula los dic que ya se analizaron para no repetirlos
                    items_found.append(element['typeAccount'])

                    elem_count = items_found.count(element['typeAccount']) # Se cuentan los elementos
                    if elem_count > 1:
                        # Si hay mas de 1 repeticion, crear el diccionario nuevo
                        cantidad = cantidad + 1
        return JsonResponse({"AC":list(listAccount),"RP":cantidad})


def accountAux(request,type ,id,idOld,cont):
    if type == 'M':
        listAccountAux = Account.objects.filter(accountFather=id).values('id','typeAccount',)
        cont =  cont + 1
        return accountAux(request,listAccountAux[0]['typeAccount'],listAccountAux[0]['id'],id,cont)
    else: 
        if cont > 0:
            listAux = Account.objects.filter(accountFather=idOld).values('id','typeAccount','description','code')
            return listAux
        else:
            listAux = Account.objects.filter(id=id).values('id','typeAccount','description','code')
            return listAux	
    
#--------------Disponibilidad----------
class GetDetallsDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('disponibility')).values('id','nameRubro','value','balance','valueP')
        rubroMovReExist = Movement.objects.filter(disponibility=request.GET.get('disponibility')).exists()
        if rubroMovReExist:
            rubroList = []
            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])
                rubroList.append({"valueR":rubroMov[x]['valueP'], "rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance']})
            print(rubroList)
            return JsonResponse({"RUBRO": list(rubroList)})
        else:
            rubroList = []
            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])
                rubroList.append({"valueR":0, "rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP']})
            return JsonResponse({"RUBRO": list(rubroList)})


class GetRubroImpDisponibility(LoginRequiredMixin,View):
    
    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        movements = Movement.objects.filter(origin_id=request.GET.get('origin'),id=request.GET.get('disponibility')).values('id','value','balance','disponibility','observation','date')
        rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('disponibility')).values('id','nameRubro','value','balance','valueP','date')
        globalDisponibility = Movement.objects.get(id=request.GET.get('disponibility'))
 
        rubroList = []

        for x in range(0,len(list(rubroMov))):
   
            disponibilityValue=RubroMovement.objects.get(movement_id=globalDisponibility,nameRubro_id=list(rubroMov)[x]['nameRubro'])
            print(list(rubroMov))
            rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'],origin_id=request.GET.get('origin'))

            rubroList.append({"dispoID":list(rubroMov)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"budgetEject":rubro.budgetEject+int(list(rubroMov)[x]['value']) ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance']})
        
        return JsonResponse({"RUBRO": list(rubroList), "MV": list(movements)})

class UpdateRID(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        
        
        rubroMovement = RubroMovement.objects.filter(movement_id=request.GET.get('disponibility'),movement__concept='DISPONIBILIDAD').values('nameRubro','movement_id')
        rubroMovementv = RubroMovement.objects.filter(nameRubro_id = rubroMovement[0]['nameRubro'], movement_id__gt = request.GET.get('disponibility')).values('id')
        print(len(rubroMovementv))
        if len(rubroMovementv) != 0:
            return JsonResponse({"OPERO": "NO"})
        else:
            disponibilityGeneral = Movement.objects.get(id=request.GET.get('disponibility'))
            rubroMovementDispPartic = RubroMovement.objects.get(id=request.GET.get('id'))
            rubro = Rubro.objects.get(id=request.GET.get('rubro'))
            #GENERAL
            disponibilityGeneral.value = disponibilityGeneral.value - int(request.GET.get('oldValue'))
            disponibilityGeneral.balance = disponibilityGeneral.balance - int(request.GET.get('balance'))
            disponibilityGeneral.save()
            disponibilityGeneral.value = disponibilityGeneral.value + int(request.GET.get('sendValue'))
            disponibilityGeneral.balance = disponibilityGeneral.balance + int(request.GET.get('newBalance'))
            disponibilityGeneral.save()
        
            #IMPLICADO

            rubroMovementDispPartic.value = int(request.GET.get('sendValue')) 
            rubroMovementDispPartic.valueP = int(request.GET.get('sendValue')) 
            rubroMovementDispPartic.balance = int(request.GET.get('newBalance'))  
            rubroMovementDispPartic.save()

            #RUBRO

            rubro.budgetEject = rubro.budgetEject+int(request.GET.get('oldValue')) #sumo el valor  del prespuesto por ejecutar     
            rubro.save()
            rubro.budgetEject = rubro.budgetEject-int(request.GET.get('sendValue')) #resto el valor  del prespuesto por ejecutar     
            rubro.save()

            return JsonResponse({"OPERO": "SI"})

class UpdateRIDDetall(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        
        bussines=Bussines.objects.get(id=request.GET.get('bussines'))
        disponibilityGeneral = Movement.objects.get(disponibility=request.GET.get('disponibility'))
        disponibilitys = json.loads(request.GET.get('newDate'))
        today = datetime.now()
        print(disponibilitys)
        if len(disponibilitys) > 0:
            for x in range(0,len(disponibilitys)):
                disponibilityGeneral.value = disponibilityGeneral.value + disponibilitys[x]['value']
                disponibilityGeneral.balance = disponibilityGeneral.balance + disponibilitys[x]['balance']

                rubroMov = RubroMovement.objects.create(bussines=bussines,value=disponibilitys[x]['value'],valueP=disponibilitys[x]['value'],balance=disponibilitys[x]['balance'],date=today,nameRubro_id=disponibilitys[x]['id'],movement_id=request.GET.get('id')) 
                rubro = Rubro.objects.get(id=disponibilitys[x]['id'])
                rubro.budgetEject = disponibilitys[x]['balance']
                rubro.save()

        

        disponibilityGeneral.observation = request.GET.get('observation')
        disponibilityGeneral.date = request.GET.get('date')
        disponibilityGeneral.save()
    

        return JsonResponse({"OPERO": "SI"})
    
#----------------registro---------
class GetDetailRegister(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('register')).values('nameRubro','value','balance','valueP','movement_id')
        rubroMovObliExist = Movement.objects.filter(register = request.GET.get('register')).exists()
        rubroList = []
        if rubroMovObliExist == True:

            rubroMovObli = Movement.objects.get(register = request.GET.get('register'))
            ValueObli = RubroMovement.objects.filter(movement_id = rubroMovObli.id).values('id','nameRubro','value','balance','valueP')
            print(ValueObli)
            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=rubroMov[x]['nameRubro'])
                movDisp = Movement.objects.get(id = rubroMov[x]['movement_id'])
                RubMovDisp = RubroMovement.objects.get(movement_id = movDisp.disponibility,nameRubro_id = rubroMov[x]['nameRubro'] )
                third = InformationMovement.objects.filter(movement_id = request.GET.get('register') ).values('third__id','third__name','third__surnames')
                rubroList.append({"valueObli":list(ValueObli)[x]['valueP'],"rubro":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP'], "valueDis": RubMovDisp.value})
            return JsonResponse({"DRG": list(rubroList), "Third": list(third)})
        else:

            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=rubroMov[x]['nameRubro'])
                movDisp = Movement.objects.get(id = rubroMov[x]['movement_id'])
                RubMovDisp = RubroMovement.objects.get(movement_id = movDisp.disponibility,nameRubro_id = rubroMov[x]['nameRubro'] )
                third = InformationMovement.objects.filter(movement_id = request.GET.get('register') ).values('third__id','third__name','third__surnames')
                rubroList.append({"valueObli":0,"rubro":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP'], "valueDis": RubMovDisp.value})
            return JsonResponse({"DRG": list(rubroList), "Third": list(third)})


class GetRubroImpDetailRegister(LoginRequiredMixin,View):
    
    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        
        registers = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), id=request.GET.get('register')).values('id','register','value','balance','observation','date')
        
        third = Third.objects.filter(bussines_id=request.GET.get('bussines')).values('id','name','surnames','phone','identification','typeIdentification')
        selectThird = InformationMovement.objects.filter(movement_id = list(registers)[0]['id']).values('third_id','id','RightsEconomic')


        typeContract = TypeContract.objects.filter(bussines_id=request.GET.get('bussines')).values('id','nameTC')
        selectTypeContract = TypeContractMovement.objects.filter(movement_id = list(registers)[0]['id']).values('id','typeContractdetail__id','typeContractdetail__codeTypeC','typeContractdetail__value','typeContractdetail__typeContract_id','typeContractdetail__digitstc')
        
        typeContractDetail = TypeContractDetail.objects.filter(typeContract_id = list(selectTypeContract)[0]['typeContractdetail__typeContract_id']).values('id','value','digitstc')
        
        
        print(list(registers))
        rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('register')).values('id','nameRubro_id','value','balance','valueP','date')
        globalRegister = Movement.objects.get(id=request.GET.get('register'))
        rubroList = []

        for x in range(0,len(list(rubroMov))):

            disponibilityValue=RubroMovement.objects.get(movement_id=globalRegister.disponibility,nameRubro_id=list(rubroMov)[x]['nameRubro_id'])
            rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro_id'])

            rubroList.append({"registerID":list(rubroMov)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":disponibilityValue.value,"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP']})
           
        return JsonResponse({"DRG": list(rubroList), "RG": list(registers), "TH": list(third), "TC": list(typeContract), "STC":list(selectTypeContract), "STH":list(selectThird), "TCD": list(typeContractDetail)})

class UpdateDetailRegister(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        
        rubroMovement = RubroMovement.objects.get(id=request.GET.get('id'))
        register = Movement.objects.get(id=request.GET.get('register'))

        disponibility = RubroMovement.objects.get(movement_id=register.disponibility, nameRubro_id = rubroMovement.nameRubro)

 
        register.value = register.value - int(request.GET.get('oldValue'))
        register.balance = register.balance - int(request.GET.get('balance'))
        register.save()

        register.value = register.value + int(request.GET.get('sendValue'))
        register.balance = register.balance + int(request.GET.get('balanceChange'))
        register.save()

        rubroMovement.value = int(request.GET.get('sendValue')) #sumo el valor 
        rubroMovement.valueP = int(request.GET.get('sendValue'))  #sumo el valueP
        rubroMovement.balance = int(request.GET.get('balanceChange'))  #sumo el saldo
        rubroMovement.save()

        disponibility.valueP = disponibility.valueP+int(request.GET.get('oldValue'))  #sumo el saldo del registro global
        disponibility.save()
        disponibility.valueP = disponibility.valueP-int(request.GET.get('sendValue')) #resto el valor  del registro global
        disponibility.save()

        register.date = request.GET.get('date')
        register.observation = request.GET.get('observation')
        register.save()
        

        return JsonResponse({"OPERO": "SI"})



#----------------Obligación---------
class GetDetailObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('obligation')).values('nameRubro','value','balance','valueP','movement_id','id')
        """  rubroMovPayExist = Movement.objects.filter(obligation = request.GET.get('obligation')).exists() """

        rubroList = []
        """ if rubroMovPayExist: """

        """ rubroMovPay = Movement.objects.get(obligation = request.GET.get('obligation')) """
        """  ValuePay= RubroMovement.objects.filter(movement_id = rubroMovPay.id).values('id','nameRubro','value','balance','valueP') """

        for x in range(0,len(list(rubroMov))):
            rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])

            movReg = Movement.objects.get(id = rubroMov[x]['movement_id'])
            
            RubMovReg = RubroMovement.objects.get(movement_id = movReg.register,nameRubro_id = rubroMov[x]['nameRubro'] )
            third = InformationMovement.objects.filter(movement_id = request.GET.get('obligation') ).values('third__id','third__name','third__surnames')
            rubroList.append({"valueP":list(rubroMov)[x]['valueP'],"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP'], "valueR": RubMovReg.value, "idMov":rubroMov[x]['id']})
        return JsonResponse({"OB": list(rubroList), "Thrid": list(third)})

        """ else:

            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])

                movReg = Movement.objects.get(id = rubroMov[x]['movement_id'])
                
                RubMovReg = RubroMovement.objects.get(movement_id = movReg.register,nameRubro_id = rubroMov[x]['nameRubro'] )
                third = InformationMovement.objects.filter(movement_id = request.GET.get('obligation') ).values('third__id','third__name','third__surnames')
                rubroList.append({"valueP":0,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP'], "valueR": RubMovReg.value,"idMov":rubroMov[x]['id']})
            return JsonResponse({"OB": list(rubroList), "Thrid": list(third)})
 """
class GetRubroImpDetailObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        print(request.GET.get('obligation'))

        rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('obligation')).values('id','nameRubro','value','balance','valueP')
        globalObligation = Movement.objects.get(id=request.GET.get('obligation'))

        ObligationM = Movement.objects.filter(id=request.GET.get('obligation')).values('id','observation','date')

        thirdSelect = InformationMovement.objects.filter(movement_id=globalObligation.id).values('id','third_id','RightsEconomic')
        third = Third.objects.filter(bussines_id = request.GET.get('bussines')).values('id','name','surnames')
        print(list(third))
        rubroList = []
       
        for x in range(0,len(list(rubroMov))):
            
            obligationValue=RubroMovement.objects.get(movement_id=globalObligation.register,nameRubro_id=list(rubroMov)[x]['nameRubro'])
            rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])

            rubroList.append({"idObligation":list(rubroMov)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":obligationValue.value,"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP']})
           
        return JsonResponse({"OB": list(rubroList),"STH":list(thirdSelect),"TH":list(third), "OBM":list(ObligationM)})


class UpdateDetailObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        
        rubroMovement = RubroMovement.objects.get(id=request.GET.get('id'))
        obligation = Movement.objects.get(id=request.GET.get('obligation'))
        register = RubroMovement.objects.get(movement_id=obligation.register, nameRubro_id = rubroMovement.nameRubro)

 
        obligation.value = obligation.value - int(request.GET.get('oldValue'))
        obligation.balance = obligation.balance - int(request.GET.get('balance'))
        obligation.save()

        obligation.value = obligation.value + int(request.GET.get('sendValue'))
        obligation.balance = obligation.balance + int(request.GET.get('newBalance'))
        obligation.save()

        rubroMovement.value = int(request.GET.get('sendValue')) #sumo el valor 
        rubroMovement.valueP = int(request.GET.get('sendValue'))  #sumo el valueP
        rubroMovement.balance = int(request.GET.get('newBalance'))  #sumo el saldo
        rubroMovement.save()
        print(request.GET.get('sendValue'))
        register.valueP = register.valueP+int(request.GET.get('oldValue'))  #sumo el saldo del registro global
        register.save()
        register.valueP = register.valueP-int(request.GET.get('sendValue')) #resto el valor  del registro global
        register.save()


        """ register.valueP = register.valueP + int(request.GET.get('sendValue'))

        rubroMovement.value = int(request.GET.get('sendValue')) #resto el valor 
        rubroMovement.valueP = int(request.GET.get('sendValue'))  #resto el valueP
        rubroMovement.balance = int(request.GET.get('newBalance'))  #sumo el saldo
        rubroMovement.save()

        obligation.value = obligation.value - int(request.GET.get('oldValue'))
        obligation.balance = obligation.balance - int(request.GET.get('balance'))
        obligation.save()

        obligation.value = obligation.value + int(request.GET.get('sendValue'))
        obligation.balance = obligation.balance + int(request.GET.get('newBalance'))
        obligation.save()

        register.valueP = register.valueP+int(request.GET.get('oldValue'))  #sumo el saldo del registro global
        register.save()
        register.valueP = register.valueP-int(request.GET.get('sendValue')) #sumo el valor  del registro global
        register.save()
 """











        

            
        return JsonResponse({"OPERO": "SI"})

class UpdateAccountToObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        accountAsociateUpdate = AccountTypeRubro.objects.get(id=request.GET.get('id'))
        accountAsociateUpdate.account_id = request.GET.get('idTypeAccountUpdate')
        accountAsociateUpdate.save()
        return JsonResponse({"UPDATE": "SI"}) 


class GetRegistersOB(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="REGISTRO").values('register','observation','value','balance','date','id')
        return JsonResponse({"RG": list(movement)})

class FilterObligationByName(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        informationByName = InformationMovement.objects.filter(third_id=request.GET.get('id'),typeMovement='OBLIGACION').values('movement_id','movement__observation','movement__obligation','movement__origin','movement__date')
        return JsonResponse({"MV": list(informationByName)}) 

class GetObligationsSelect(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        account = ValuesAccountObligation.objects.filter(obligation_id=request.GET.get('id'),typeAccount = 'Credito').values('id','account__account__description','account__account__code','account__account__id','typeAccount','value','account__document','account__rubro__rubro')
        return JsonResponse({"account":list(account)})

    """ globalObligation = Movement.objects.get(id=request.GET.get('id'))
        rubroMovement = RubroMovement.objects.filter(movement_id=request.GET.get('id')).values('id','nameRubro','value','balance','valueP','movement__obligation')
        voucher = Voucher.objects.filter(bussines_id=request.GET.get('bussines')).values('code','name','description','category','id')        
        accountToSend = []
        discountToSend = []


        globalObligation = AccountTypeRubro.objects.get(id=request.GET.get('id'),typeAccount = )

        for x in range(0,len(list(rubroMovement))):
            account = ValuesAccountObligation.objects.filter(obligation_id=list(rubroMovement)[x]['id']).values('id','account__account__description','account__account__code','account__account__id','typeAccount','value','account__document')
            print(account)
            for x in range(0,len(list(account))):
                accountToSend.append({"code":list(account)[x]['account__account__code'],"id":list(account)[x]['account__account__id']})
        
        for x in range(0,len(list(accountToSend))):
            discount = Discount.objects.filter(state='AUTOMATICO',bussines_id=request.GET.get('bussines')).values('account__code','name','account','typeDiscount','state','acumulate','baseCalculate','average','initialValue','finalValue','id')
            print("dsd",list(discount))
            for x in range(0,len(list(discount))):
                discountToSend.append({"id":list(discount)[x]['id'],"name":list(discount)[x]['name'],"account_code":list(discount)[x]['account__code'],"account":list(discount)[x]['account'],"typeDiscount":list(discount)[x]['typeDiscount'],"state":list(discount)[x]['state'],"acumulate":list(discount)[x]['acumulate'],"baseCalculate":list(discount)[x]['baseCalculate'],"average":list(discount)[x]['average'],"initialValue":list(discount)[x]['initialValue'],"finalValue":list(discount)[x]['finalValue']})
        rubroList = []
        
        
        for x in range(0,len(list(rubroMovement))):
            rubro = Rubro.objects.get(id=list(rubroMovement)[x]['nameRubro'])
            rubroList.append({"obligation":list(rubroMovement)[x]['movement__obligation'],"idObligation":list(rubroMovement)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"value":list(rubroMovement)[x]['value'],"balance":list(rubroMovement)[x]['balance'],"valueP":list(rubroMovement)[x]['valueP'] })
 """
      

class GetDiscountsManuals(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        discount = Discount.objects.filter(state='MANUAL',bussines_id=request.GET.get('bussines'), account__isnull = False).values('id','account__code','name','account','typeDiscount','state','acumulate','baseCalculate','average','initialValue','finalValue','account__description')
        return JsonResponse({"DC": list(discount)}) 

class GetTypeDocument(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        voucher = typeDocument.objects.filter(bussines_id=request.GET.get('bussines'),accountPeriod_id =request.GET.get('period')).values('codigo','description','id') 
        print(request.GET.get('bussines'),request.GET.get('period'))       
        return JsonResponse({"VC": list(voucher)}) 

class CreateVoucherPayment(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):


        today = datetime.now()
        payments = json.loads(request.GET.get('payments'))
        discounts = json.loads(request.GET.get('discounts'))
        accounts = json.loads(request.GET.get('accounts'))
        bussines=Bussines.objects.get(id=request.GET.get('bussines'))
        voucher = Movement.objects.filter(concept="COMPROBANTE", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        if voucher == False:
            voucherPaymentFormat = str(3040)+str(today.year)+str(today.month)+str(today.day)+str(0)
            newVoucher = Movement.objects.create(
                    bussines=bussines,
                    concept="COMPROBANTE",
                    value=request.GET.get('value'),
                    balance=request.GET.get('balance'),
                    date=request.GET.get('date'),
                    obligation=request.GET.get('obligation'),
                    vouchePayment=request.GET.get('paymentCode'),
                    origin=Origin.objects.get(id=request.GET.get('origin')),
                    observation=request.GET.get('observation')
            )

            for x in range(0,len(payments)):
                rubroBalanceOperation = RubroBalanceOperation.objects.create(
                    bussines=bussines,
                    typeOperation='COMPROBANTE',
                    value=payments[x]['value'],
                    balance=payments[x]['value'],
                    date=request.GET.get('date'),
                    bussines_id=request.GET.get('bussines'),
                    movement_id = newVoucher.id,
                    nameRubro_id=payments[x]['id']
                    ) 

                rubroMov = RubroMovement.objects.create(
                    bussines=bussines,
                    value=payments[x]['value'],
                    valueP=0,
                    balance=payments[x]['value'],
                    date=request.GET.get('date'),
                    bussines_id=request.GET.get('bussines'),
                    nameRubro_id=payments[x]['id'],
                    movement_id=newVoucher.id
                ) 

                
                obligationMov = RubroMovement.objects.get(id=payments[x]['idObligation'])
                obligationMov.valueP = obligationMov.valueP+payments[x]['value']
                obligationMov.balance = obligationMov.balance-payments[x]['value']
                obligationMov.save()

                obligationOpe = RubroBalanceOperation.objects.get(id=payments[x]['idObligation'])
                obligationOpe.balance = obligationOpe.balance-payments[x]['value']
                obligationOpe.save()

            for x in range(0,len(discounts)):
                discountMovement = DiscountMovement.objects.create(
                    discount_id=discounts[x]['id'],
                    movement_id=newVoucher.id,
                    base=discounts[x]['base'],
                    value=discounts[x]['value']
                )              
            for x in range(0,len(accounts)):
                if(accounts[x]['tipo']=='Debito'):

                    movementAcount = MovementAcount.objects.create(
                        movement_id=newVoucher.id,
                        account_id=accounts[x]['id'],
                        debito=accounts[x]['value'],       
                    )
                else:
                    movementAcount = MovementAcount.objects.create(
                        movement_id=newVoucher.id,
                        account_id=accounts[x]['id'],
                        credito=accounts[x]['value'],       
                    )
            return JsonResponse({"CREATE": "TRUE"})
        
        
        else:        
            lastVoucher = Movement.objects.filter(concept="COMPROBANTE", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()         
            newVoucher = Movement.objects.create(
                    bussines=bussines,
                    concept="COMPROBANTE",value=request.GET.get('value'),
                    balance=request.GET.get('balance'),
                    date=today,
                    obligation=request.GET.get('obligation'),
                    vouchePayment=lastVoucher.vouchePayment+1,
                    origin=Origin.objects.get(id=request.GET.get('origin')),
                    observation=request.GET.get('observation')
            )
            for x in range(0,len(payments)):

                rubroBalanceOperation = RubroBalanceOperation.objects.create(
                    bussines=bussines,
                    typeOperation='COMPROBANTE',
                    value=payments[x]['value'],
                    balance=payments[x]['value'],
                    date=request.GET.get('date'),
                    nameRubro_id=payments[x]['id'],
                    movement_id = newVoucher.id,

                    ) 
                rubroMov = RubroMovement.objects.create(
                    bussines=bussines,
                    value=payments[x]['value'],
                    valueP=0,
                    balance=payments[x]['value'],
                    date=request.GET.get('date'),
                    nameRubro_id=payments[x]['id'],
                    movement_id=newVoucher.id
                    ) 
                obligationMov = RubroMovement.objects.get(id=payments[x]['idObligation'])
                obligationMov.valueP = obligationMov.valueP+payments[x]['value']
                obligationMov.balance = obligationMov.balance-payments[x]['value']
                obligationMov.save()

                obligationOpe = RubroBalanceOperation.objects.get(id=payments[x]['idObligation'])
                obligationOpe.balance = obligationOpe.balance-payments[x]['value']
                obligationOpe.save()
            for x in range(0,len(discounts)):
                discountMovement = DiscountMovement.objects.create(discount_id=discounts[x]['id'],movement_id=newVoucher.id,base=discounts[x]['base'],value=discounts[x]['value'])              
            for x in range(0,len(accounts)):
                if(accounts[x]['tipo']=='Debito'):

                    movementAcount = MovementAcount.objects.create(
                        movement_id=newVoucher.id,
                        account_id=accounts[x]['id'],
                        debito=accounts[x]['value'],       
                    )
                else:
                    movementAcount = MovementAcount.objects.create(
                        movement_id=newVoucher.id,
                        account_id=accounts[x]['id'],
                        credito=accounts[x]['value'],       
                    )   

            return JsonResponse({"CREATE": "TRUE"})

class GetSerialVoucherPayment(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
    
        today = datetime.strptime(request.GET.get('dateCreateDP'), '%Y-%m-%d')
        voucherPayment = Movement.objects.filter(concept="COMPROBANTE", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        if voucherPayment == False:
            voucherPaymentFormat = str(3040)+str(today.year)+str(today.month)+str(today.day)+str(0)
            return JsonResponse({"VP": voucherPaymentFormat})
        else:        
            lastRegister = Movement.objects.filter(concept="COMPROBANTE", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            return JsonResponse({"VP": lastRegister.vouchePayment+1})


class FilterToObligation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        if request.GET.get('filter') == "DOCUMENT":
            people = Third.objects.filter(identification__iexact=request.GET.get('text').upper()).values('id','name','identification','surnames','reason','typeIdentification')
            
            return JsonResponse({"TH": list(people)}) 
        else:
            people = Third.objects.filter(name__iexact=request.GET.get('text').upper()).values('id','name','identification','surnames','reason','typeIdentification')
            return JsonResponse({"TH": list(people)}) 


class Thirdfilter(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        
        listpeopleOb = []
        listaccount = []
        
        if request.GET.get('typefilter') == "DOCUMENT":
            people = Third.objects.filter(identification=request.GET.get('filter'),bussines_id=request.GET.get('idBussines')).values('id','name','identification','surnames','reason','typeIdentification')
            for x in range(0,len(people)):
                listpeople = InformationMovement.objects.filter(third_id=people[x]['id']).values('id','movement_id','typeMovement')

                for y in range(0,len(listpeople)):
                    listpeople2 = RubroBalanceOperation.objects.filter(movement_id=listpeople[y]['movement_id'], movement__isnull = False).values('value','movement__register','movement__obligation','nameRubro_id','movement__balance','date','movement__observation','id', 'movement__origin__nameOrigin')
       
                    if list(listpeople)[y]['typeMovement'] == 'OBLIGACION':
                        ##regiter = Movement.objects.filter(id = list(listpeople2)[y]['movement__register'], origin__isnull = False).values('register','origin__nameOrigin')
                        print(list(listpeople2),"prueb")

                        rubromove = RubroMovement.objects.filter(movement_id=listpeople[y]['movement_id']).values('valueP','id','value')

                        for g in range(0,len(rubromove)):
                            accountobli = ValuesAccountObligation.objects.filter(obligation_id = rubromove[g]['id'] ).values('id','typeAccount','value','obligation_id','account__account__description','account__account__code','account__account__id','typeAccount','value','account__document','account__rubro__rubro')
                        for g in range(0,len(listpeople2)):
                            rubro = Rubro.objects.filter(id = list(listpeople2)[g]['nameRubro_id']).values('rubro','description','id')
                            listpeople2[g]['nameRubro_id'] = list(rubro)[0]['rubro']
                            listpeople2[g]['Rubro_id'] = list(rubro)[0]['id']
                            listpeople2[g]['description'] = list(rubro)[0]['description']
                            listpeople2[g]['rubromove'] = list(rubromove)[g]['value']
                            listpeople2[g]['idobligation'] = list(rubromove)[g]['id']
                            listpeople2[g]['typeMovement'] = list(listpeople)[x]['typeMovement']
                            


                        listpeopleOb.append({
                            "idThird": people[x]['id'],
                            "name": people[x]['name'],
                            "surnames": people[x]["surnames"],
                            "identification": people[x]['identification'],
                            "movement": list(listpeople)[y]['typeMovement'],
                            "operation": list(listpeople2)
                        })
                 
            return JsonResponse({"TH": list(people),"LB": list(listpeopleOb), "MV": list(listpeople)})  
        else:
            people = Third.objects.filter(name__contains=request.GET.get('filter').upper(),bussines_id=request.GET.get('idBussines')).values('id','name','identification','surnames','reason','typeIdentification')

            for x in range(0,len(people)):
                infMovement = InformationMovement.objects.filter(third_id=people[x]['id']).values('id','movement_id','typeMovement')

                for y in range(0,len(infMovement)):
                    if infMovement[y]['typeMovement'] == 'OBLIGACION':
                        rubroBO = RubroBalanceOperation.objects.filter(movement_id=infMovement[y]['movement_id'], movement__isnull = False).values('value','movement__register','movement__obligation','nameRubro_id','movement__balance','date','movement__observation','id', 'movement__origin__nameOrigin')
                        ##regiter = Movement.objects.filter(id = list(listpeople2)[y]['movement__register'], origin__isnull = False).values('register','origin__nameOrigin')
                        rubromove = RubroMovement.objects.filter(movement_id=infMovement[y]['movement_id']).values('valueP','id','value')

                        """ for g in range(0,len(rubromove)):
                            accountobli = ValuesAccountObligation.objects.filter(obligation_id = rubromove[g]['id'] ).values('id','typeAccount','value','obligation_id','account__account__description','account__account__code','account__account__id','typeAccount','value','account__document','account__rubro__rubro') """
                       
                        for g in range(0,len(rubroBO)):
                            rubro = Rubro.objects.filter(id = list(rubroBO)[g]['nameRubro_id']).values('rubro','description','id')
                            rubroBO[g]['nameRubro_id'] = list(rubro)[0]['rubro']
                            rubroBO[g]['Rubro_id'] = list(rubro)[0]['id']
                            rubroBO[g]['description'] = list(rubro)[0]['description']
                            rubroBO[g]['rubromove'] = list(rubromove)[g]['value']
                            rubroBO[g]['idobligation'] = list(rubromove)[g]['id']
                            rubroBO[g]['typeMovement'] = list(infMovement)[x]['typeMovement']
                            


                        listpeopleOb.append({
                            "idThird": people[x]['id'],
                            "name": people[x]['name'],
                            "surnames": people[x]["surnames"],
                            "identification": people[x]['identification'],
                            "movement": list(infMovement)[y]['typeMovement'],
                            "operation": list(rubroBO)
                        })

            
            return JsonResponse({"TH": list(people),"LB": list(listpeopleOb), "MV": list(infMovement)})  



class FillTypeContract(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        typecontract = TypeContractDetail.objects.filter(typeContract_id=request.GET.get('contract')).values('id','codeTypeC','descriptionTypeC','value','digitstc')

        return JsonResponse({"Contract":list(typecontract)})



class UpdateDetailRegisterBase(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        register = Movement.objects.filter(register=request.GET.get('movementID')).exists()
        print(register)    
        if register == False:

        
            typeContractMovement = TypeContractMovement.objects.get(id=request.GET.get('TypeContractMovement_id'))
            typeContractMovement.typeContractdetail_id = request.GET.get('TypeContractMovementID')
            typeContractMovement.save()

            third = InformationMovement.objects.get(movement_id=request.GET.get('movementID'))
            third.third_id = request.GET.get('thirdID')
            third.save()

            register = Movement.objects.get(id=request.GET.get('movementID'))
            register.date = request.GET.get('date')
            register.observation = request.GET.get('observation')
            register.save()
            

            return JsonResponse({"OPERO": "SI"})
        else:
            return JsonResponse({"OPERO": "NO"})



class UpdateDetailObligateBase(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        Obligation = Movement.objects.filter(register=request.GET.get('movementID')).exists()
        print(Obligation)    
        if Obligation == False:

            third = InformationMovement.objects.get(movement_id=request.GET.get('movementID'))
            third.third_id = request.GET.get('thirdID')
            third.save()

            Obligation = Movement.objects.get(id=request.GET.get('movementID'))
            Obligation.date = request.GET.get('date')
            Obligation.observation = request.GET.get('observation')
            Obligation.save()
            

            return JsonResponse({"OPERO": "SI"})
        else:
            return JsonResponse({"OPERO": "NO"})


class GetAccountRubroExists(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        Obligation = AccountTypeRubro.objects.filter(rubro_id=request.GET.get('rubro')).exists()
        print(Obligation)    
        if Obligation == True:
            return JsonResponse({"EXISTE": "SI"})
        else:
            return JsonResponse({"EXISTE": "NO"})

class GetDiscountAuto(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
    
        discount = Discount.objects.filter(state="AUTOMATICO", bussines_id = request.GET.get('bussines'), account__isnull = False).values('id','account__code','name','account','typeDiscount','state','acumulate','baseCalculate','average','initialValue','finalValue','account__description')

        return JsonResponse({"DC": list(discount)})
