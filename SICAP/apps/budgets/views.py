from copyreg import constructor
from traceback import print_tb
from typing import Type
from django.db import connections
from django.shortcuts import render
from apps.budgets.models import *
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from apps.budgets.forms import *
from django.urls import reverse_lazy, reverse
from apps.settingsSICAP.forms import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import date
from datetime import datetime
import simplejson as json
from tablib import Dataset 
from django.views.decorators.csrf import csrf_exempt
import sys
from django.db.models import Sum

# Create your views here.


class CreateBussines(CreateView):

    model = Bussines
    form_class = BussinesForm
    template_name = 'bussines/createBussines.html'

    def get_success_url(self,**kwargs):
        return reverse_lazy("listBussines",  kwargs={'pkUser': self.request.user.id})

class ListBussines(LoginRequiredMixin,ListView):

    model = Bussines
    queryset= model.objects.order_by('name')
    template_name = 'bussines/listBussines.html'

    def get_context_data(self):
        context = super(ListBussines, self).get_context_data()
        context['ACform'] = AccountPeriodForm
        context['Originform'] = OriginForm
        context['ByAccountOpforms'] = ByAccountOpForms
        context['Operationform'] = OperationForm
        return context

    def get_queryset(self):
        queryset = super(ListBussines, self).get_queryset()
        return Bussines.objects.all()

class DeleteBussines(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        bussinesDelete = Bussines.objects.get(id=request.GET.get('bussinesID'))
        bussinesDelete.delete()
        return JsonResponse({'DELETE':True})


###################### Vistas relacionadas con periodos contables ####################
class CreateAccountPeriod(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs): 

        bussinesId= request.GET.get('bussines')
        name = request.GET.get('name')
        state = request.GET.get('state')
        initialDate = request.GET.get('initialDate')
        finalDate = request.GET.get('finalDate')
        bussines = Bussines.objects.get(id=bussinesId)
        accountPeriodExist = AccountPeriod.objects.filter(name=name.upper(), bussines_id=bussinesId).exists()

        listDates = request.GET.get('listDate')
        dates = json.loads(listDates)

        if accountPeriodExist == False:
            newAccountPeriod = AccountPeriod.objects.create(
                bussines=bussines, name=name.upper(), state=state.upper(), initialDate=initialDate, finalDate=finalDate
            )
            for x in range(0,len(dates)):
                print(dates[x])
                newClosedPeriod =  ClosedPeriod.objects.create(
                    month =  dates[x]['mount'],
                    activate = dates[x]['activate'],
                    year = dates[x]['year'],
                    accountPeriod_id = newAccountPeriod.id
                )
            accountPeriod = {'id':newAccountPeriod.id,'name':newAccountPeriod.name}
            return JsonResponse({'CREATE':"TRUE", 'ACID':newAccountPeriod.id, 'ACName':newAccountPeriod.name})
        else:
            return JsonResponse({'CREATE':"FALSE"})


        return JsonResponse({'CREATE':"TRUE"})

class GetAccountPeriodOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        accountPeriod =  AccountPeriod.objects.all().filter(bussines_id=request.GET.get('bussinesIdO')).values('name')
        return JsonResponse({"AC": list(accountPeriod)})


class CreateOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        nameAccount = request.GET.get('accountPeriod')
        nameAccount = nameAccount[:-1]
        accountPeriod = AccountPeriod.objects.get(name=nameAccount.upper())

        originExist = Origin.objects.filter(nameOrigin=request.GET.get('nameOrigin').upper(), accountPeriod_id=accountPeriod).exists()
        if originExist == False:
            nameOrigin = request.GET.get('nameOrigin')
            codeOrigin = request.GET.get('codeOrigin')
            descriptionOrigin = request.GET.get('descriptionOrigin')

            newOrigin = Origin.objects.create(nameOrigin=nameOrigin.upper(),codeOrigin=codeOrigin.upper(),descriptionOrigin=descriptionOrigin.upper(),orderOrigin=request.GET.get('orderOrigin').upper(),finalDateOrigin=request.GET.get('finalDateOrigin'),accountPeriod=accountPeriod)
            origin = {'id':newOrigin.id,'name':newOrigin.nameOrigin}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})
        
def mainBudget(request,pkUser):

    informForm = ByInformForms()
    updateForm = ByRubroUpdate()
    typeAgreement = TypeAgreementForm()
    context = {'informForm':informForm, 'updateForm': updateForm, 'typeAgreement':typeAgreement }
    return render(request, 'budget/budget.html', context)

""" class CreateOperation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        origins = json.loads(request.GET.get('origin'))
        bussines=request.GET.get('bussines')
        for x in range(0,len(origins)):
            nameAccount = request.GET.get('accountPeriod')
            nameAccount = nameAccount
            accountPeriod = AccountPeriod.objects.get(name=nameAccount, bussines_id=bussines)
            
            getOrigin  = Origin.objects.get(nameOrigin=origins[x], accountPeriod_id=accountPeriod)
            objOrigin = Origin.objects.filter(nameOrigin=origins[x], accountPeriod_id=accountPeriod)
            operationExist = Operation.objects.filter(nameOp=request.GET.get('nameOp').upper(), origin=getOrigin).exists()
            if operationExist == False:
                newOperation = Operation.objects.create(
                    codeOp=request.GET.get('codeOp').upper(), 
                    nameOp=request.GET.get('nameOp').upper(), 
                    descriptionOp=request.GET.get('descriptionOp').upper(), 
                    operation=request.GET.get('operation').upper(), 
                    orderOp=request.GET.get('orderOp')
                    
                )
                newOperation.origin.add(*objOrigin)
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"})
 """
        
class GetAccountPeriodOperation(LoginRequiredMixin,View): # funcion para cargar el periodo contable

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
   
        idBussines = request.GET.get('bussinesIdOP') #id de la empresa porque el periodo contable esta relacionado con la empresa
        accountPeriod = AccountPeriod.objects.filter(bussines_id=idBussines).values('name')# se filtra por el id de la empresa el periodo contable
        return JsonResponse({"ACName": list(accountPeriod)})

class GetAccountPeriodOriginOperation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        accountPeriod = AccountPeriod.objects.get(name=request.GET.get('accountPeriod'))
        origins = Origin.objects.filter(accountPeriod_id=accountPeriod.id).values('nameOrigin')# con el .values('nameOrigin') le paso a mi lista lo que necesito
        return JsonResponse({"OR": list(origins)})

class GetInforms(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        inform = Inform.objects.filter(bussines_id=request.GET.get('idBussines')).values('id','nameI')
        return JsonResponse({"OR": list(inform)})

class GetInformsDetall(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        print(request.GET.get('idInforms'))
        print(request.GET.get('nameOrigin'))
        detall = []
        informdetall = InformDetall.objects.filter(inform_id = request.GET.get('idInforms')).values('codeInfD','id')
        origin = Origin.objects.get(nameOrigin=request.GET.get('nameOrigin'))
        rubrosDetall = Rubro.objects.filter(origin_id = origin, rubroinformdetall__detall__isnull=False).values('rubro','id','description','rubroinformdetall__detall_id','rubroinformdetall__id','rubroinformdetall__informdetall_id','rubroinformdetall__detall__descriptionInfD').order_by('id')
        rubros = Rubro.objects.filter(origin_id = origin,typeRubro='A').values('rubro','id','description')
        for x in range(0,len(informdetall)):
            detall += Detall.objects.filter(informDetall_id = informdetall[x]['id']).values('id','descriptionInfD','informDetall_id')
        return JsonResponse({"RB": list(rubros),"IF": list(informdetall),"RD":list(rubrosDetall),"DT":list(detall)})


        
class SaveInformsDetall(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        newData =  json.loads(request.GET.get('newData'))
        print(newData)
        for x in newData:
            rubroinformdetall = RubroInformdetall.objects.get(rubro_id = x[1],informdetall_id = x[2])
            rubroinformdetall.detall_id = x[0]
            rubroinformdetall.save()
        return JsonResponse({"TRUE":"TRUE"})


class GetOriginBudget(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
       
        option =request.GET.get('option')
        if option =='1':
            nameAC = request.GET.get('nameAC')### Cambio
            accountPeriod = AccountPeriod.objects.get(name=nameAC, bussines_id=request.GET.get('idBussines'))
            origintest = Origin.objects.filter(accountPeriod_id=accountPeriod.id).values('nameOrigin','id','pattern')
            return JsonResponse({"OR": list(origintest)})
        elif  option=='2':
            inform  = Inform.objects.filter(bussines_id=request.GET.get('idBussines')).values('nameI')
            return JsonResponse({"IF": list(inform)})
        elif option=='3': 
            informDetallTest  = InformDetall.objects.filter(inform__nameI=request.GET.get('inform')).values('codeInfD')
            return JsonResponse({"IFD": list(informDetallTest)})
        elif option=='4': 
            typeAgreement  = TypeAgreement.objects.filter().values("nameTA","id")
            agreement  = Agreement.objects.filter(id = request.GET.get('id')).values("dateAg","id")
            print(agreement)
            return JsonResponse({"TA": list(typeAgreement),"DT": list(agreement)})
        elif option=='5': 
            agrementMovement = Movement.objects.filter(agreement_id=request.GET.get('id')).values('id','nameRubro','value','balance','budgetEject', 'concept')
            movementList = []
            for x in range(0,len(list(agrementMovement))):
                rubro = Rubro.objects.get(id=list(agrementMovement)[x]['nameRubro'])
                movementList.append({"id":list(agrementMovement)[x]['id'],"rubroID":rubro.id,"rubro":rubro.rubro,"initialbudget":rubro.initialBudget,"realbudget":rubro.realBudget,"description":rubro.description,"value":list(agrementMovement)[x]['value'],"balance":list(agrementMovement)[x]['balance'] ,"budgetEject":list(agrementMovement)[x]['budgetEject'] ,"concept":list(agrementMovement)[x]['concept']})
                
            return JsonResponse({"AMO": list(movementList)})
        else:
            return JsonResponse({"INFORMATION": "FALSE"})

class GetOperationBudget(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        typeagreement = []
        nameOrigin = request.GET.get('nameOrigin')
        accountPeriod = AccountPeriod.objects.get(name=request.GET.get('nameAC')) ###
        origin = Origin.objects.get(nameOrigin=nameOrigin, accountPeriod=accountPeriod.id)
        operations = Operation.objects.filter(origin=origin.id).values('nameOp')
        rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')
        movementIni = Agreement.objects.filter(origin_id=origin.id).values('id','descriptionAg','numberAg','typeAgreement','dateAg')
        for x in range(0,len(movementIni)):
            typeagreement += TypeAgreement.objects.filter(id = movementIni[x]['typeAgreement']).values('nameTA')
        return JsonResponse({"Pattern":origin.pattern,"ID":origin.id ,"OP": list(operations),"RUBRO": list(rubro),"AG":list(movementIni), "NTA": list(typeagreement)})

class GetRubroCreate(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        origin = Origin.objects.get(id=request.GET.get('origin'))
        rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')
        return JsonResponse({"RUBRO": list(rubro)})

class CreateRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        today = datetime.now()
        rubroExists = Rubro.objects.filter(rubro=request.GET.get('rubro'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin')).exists()
        ccpetExists = CCPET.objects.all()
        if len(list(ccpetExists)) > 1:
            if rubroExists == False:
                if len(request.GET.get('rubro')) == 1:
                    if request.GET.get('typeRubro') == 'AUXILIAR':
                        existccpet = CCPET.objects.filter(code=request.GET.get('rubro'),accountPeriod_id=request.POST.get('period')).exists()
                        if existccpet == True:
                            rubro = Rubro.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                            ccpet = 1,
                            origin = Origin.objects.get(id=request.GET.get('origin')), 
                            rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today,budgetEject=request.GET.get('initialBudget'), initialBudget = request.GET.get('initialBudget'), typeRubro = "A", realBudget=request.GET.get('initialBudget'),  
                            )
                        else:
                            rubro = Rubro.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                            origin = Origin.objects.get(id=request.GET.get('origin')), 
                            ccpet = 0,
                            rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today,budgetEject=request.GET.get('initialBudget'), initialBudget = request.GET.get('initialBudget'), typeRubro = "A", realBudget=request.GET.get('initialBudget'),  
                            )
                            
                        inform = json.loads(request.GET.get('inform'))
                        informDetall = json.loads(request.GET.get('detallInform'))
                        for x in range(0,len(inform)):
                            objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('bussines'))
                            objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])

                            rubro.inform.add(*objInform)
                            rubro.informdetall.add(*objDetall)

                        movement = Movement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            nameRubro_id = rubro.id, concept = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today        
                        ) 
                        rubroMov = RubroMovement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            value = request.GET.get('initialBudget'), valueP = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro_id = rubro.id, movement = movement     
                        ) 
                        rubroMov = RubroBalanceOperation.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            typeOperation = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro_id = rubro.id,    
                        )
                    else:
                        existccpet = CCPET.objects.filter(code=request.GET.get('rubro'),accountPeriod_id=request.POST.get('period')).exists()
                        if existccpet == True:
                            rubro = Rubro.objects.create(
                                bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                                ccpet = 1,
                                origin = Origin.objects.get(id=request.GET.get('origin')), 
                                rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = 0, typeRubro = "M",realBudget=0, budgetEject= 0,
                            )
                        else:

                            rubro = Rubro.objects.create(
                                bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                                ccpet = 0,
                                origin = Origin.objects.get(id=request.GET.get('origin')), 
                                rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = 0, typeRubro = "M",realBudget=0, budgetEject= 0,
                            )
                        movement = Movement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            nameRubro_id = rubro.id, concept = 'CREACION', value = 0, balance = 0, date = today        
                        ) 
                        rubroMov = RubroMovement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            value = 0, valueP = 0, balance = 0, date = today, nameRubro_id =rubro.id, movement = movement     
                        ) 
                        rubroMov = RubroBalanceOperation.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            typeOperation = 'CREACION', value = 0, balance = 0, date = today, nameRubro_id = rubro.id,    
                        )

                else:
                    rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                    rubromovement = RubroMovement.objects.filter(nameRubro_id = rubroFather.id,bussines_id=request.GET.get('bussines')).exists()

                    if rubromovement == True:
                        return JsonResponse({"MOVIMIENTO": "TRUE"})
                    
                    if request.GET.get('typeRubro') == 'AUXILIAR':
        
                        
                        existccpet = CCPET.objects.filter(code=request.GET.get('rubro'),accountPeriod_id=request.POST.get('period')).exists()
                        if existccpet == True:
                            rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                            if rubroFather.typeRubro == 'A':
                                rubroFather.typeRubro = 'M'
                                rubroFather.save()
                            
                            rubro = Rubro.objects.create(
                                bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                                ccpet = 1,
                                origin = Origin.objects.get(id=request.GET.get('origin')),
                                rubro = request.GET.get('rubro'),
                                rubroFather = rubroFather.id, 
                                nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = request.GET.get('initialBudget'), typeRubro = "A", realBudget=request.GET.get('initialBudget'), budgetEject=request.GET.get('initialBudget'),
                            )
                        else:
                            rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                            if rubroFather.typeRubro == 'A':
                                rubroFather.typeRubro = 'M'
                                rubroFather.save()
                            rubro = Rubro.objects.create(
                                bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                                origin = Origin.objects.get(id=request.GET.get('origin')),
                                ccpet = 0,
                                rubro = request.GET.get('rubro'),
                                rubroFather = rubroFather.id, 
                                nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = request.GET.get('initialBudget'), typeRubro = "A", realBudget=request.GET.get('initialBudget'), budgetEject=request.GET.get('initialBudget'),
                            )
                        inform = json.loads(request.GET.get('inform'))
                        informDetall = json.loads(request.GET.get('detallInform'))
                        for x in range(0,len(inform)):
                            objInform = Inform.objects.filter(nameI=inform[x])
                            objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                            rubro.inform.add(*objInform)
                            rubro.informdetall.add(*objDetall)

                        movement = Movement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            nameRubro_id = rubro.id, concept = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today
                        ) 
                        rubroMov = RubroMovement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            value = request.GET.get('initialBudget'), valueP = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro_id = rubro.id, movement = movement    
                        ) 
                        rubroMov = RubroBalanceOperation.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            typeOperation = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro_id = rubro.id,    
                        )              
                        rubroFatherValue(request, rubroFather.id, int(request.GET.get('initialBudget')))
                    else:
                        rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                        existccpet = CCPET.objects.filter(code=request.GET.get('rubro'),accountPeriod_id=request.POST.get('period')).exists()
                        if existccpet == True:
                            rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                            if rubroFather.typeRubro == 'A':
                                rubroFather.typeRubro = 'M'
                                rubroFather.save()
                            rubro = Rubro.objects.create(
                                bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                                ccpet = 1,
                                origin = Origin.objects.get(id=request.GET.get('origin')), 
                                rubroFather = rubroFather.id, 
                                rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = 0, typeRubro = "M", realBudget=0,budgetEject= 0
                            )
                        else:
                            rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                            if rubroFather.typeRubro == 'A':
                                rubroFather.typeRubro = 'M'
                                rubroFather.save()
                            rubro = Rubro.objects.create(
                                bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                                ccpet = 0,
                                origin = Origin.objects.get(id=request.GET.get('origin')), 
                                rubroFather = rubroFather.id, 
                                rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = 0, typeRubro = "M", realBudget=0,budgetEject= 0
                            )
                        movement = Movement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            nameRubro_id = rubro.id, concept = 'CREACION', value = 0, balance = 0, date = today        
                        ) 
                        rubroMov = RubroMovement.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            value = 0, valueP = 0, balance = 0, date = today, nameRubro_id = rubro.id, movement = movement     
                        ) 
                        rubroMov = RubroBalanceOperation.objects.create(
                            bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                            typeOperation = 'CREACION', value = 0, balance = 0, date = today, nameRubro_id = rubro.id,    
                        )
                
                rubroinfordetall =  Rubro.objects.last()
                RubroAuxiliar = Rubro.objects.filter(id = rubroinfordetall.id).values('typeRubro')
                if(RubroAuxiliar[0]['typeRubro']=='A'):
                    for inform in Inform.objects.all():
                        informdetallExist = InformDetall.objects.filter(inform_id = inform.id).exists()
                        newRubroInform = RubroInform.objects.create(
                                rubro_id = rubroinfordetall.id,
                                inform_id = inform.id
                            ) 
                        if(informdetallExist):
                            informdetall = InformDetall.objects.filter(inform_id = inform.id).values('id')
                            
                            for x in informdetall:
                                newRubroInformDetall = RubroInformdetall.objects.create(
                                    rubro_id = rubroinfordetall.id,
                                    informdetall_id = x['id'],
                        ) 
                return JsonResponse({"CREATE": "TRUE"}) 
            else:
                return JsonResponse({"CREATE": "FALSE"})
        else:
            return JsonResponse({"CREATECCPET": "FALSE"})
#////////////////// jva actulizar rubro////////////
class GetDetailRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        rubros = Rubro.objects.filter(id=request.GET.get('id'), origin__nameOrigin=request.GET.get('origin'), bussines_id=request.GET.get('bussines')).values('id','origin_id','bussines_id','rubro','rubroFather','typeRubro','nivel','description','dateCreation','initialBudget','realBudget','budgetEject')
        rubroFather = Rubro.objects.filter(id=rubros[0]['rubroFather'], origin__nameOrigin=request.GET.get('origin'), bussines_id=request.GET.get('bussines')).values('rubro')
        
        return JsonResponse({"RUBRO": list(rubros), "RUBROFATHER": list(rubroFather)})

class GetInformtUpdateRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        rubros = RubroInformdetall.objects.filter(rubro_id=request.GET.get('id'), informdetall__isnull=False,informdetall__inform__isnull=False ).values('informdetall__inform__nameI','informdetall__codeInfD')
        print( list(rubros))
        return JsonResponse({"RUBRO": list(rubros)})

class UpdateRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):      

        updateRubro = Rubro.objects.get(id=request.GET.get('id'))



        if updateRubro.typeRubro == 'A' and request.GET.get('typeRubro')=='M':

            rubroExists = Rubro.objects.filter(rubroFather=request.GET.get('id'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()

            movementExists = Movement.objects.filter(nameRubro_id=request.GET.get('id')).exclude(concept='CREACION').exists()

            rubroMovement = RubroMovement.objects.filter(nameRubro_id=request.GET.get('id'), movement__concept='DISPONIBILIDAD').exists()

            if movementExists == False and rubroMovement == False:
                    
                updateRubro.typeRubro = 'M'
                updateRubro.description = request.GET.get('description')
                updateRubro.initialBudget = request.GET.get('initialBudget')
                updateRubro.save()
                inform = json.loads(request.GET.get('inform'))
                informDetall = json.loads(request.GET.get('detallInform'))
                rbList = list(Rubro.objects.filter(id=request.GET.get('id')).values('inform__nameI','informdetall__codeInfD'))
                if rbList[0]['inform__nameI'] != None:
                    for x in range(0,len(rbList)):
                        objInformG = Inform.objects.get(nameI=rbList[x]['inform__nameI'], bussines_id=request.GET.get('idBussines'))
                        objDetallG = InformDetall.objects.get(codeInfD=rbList[x]['informdetall__codeInfD'],inform_id=objInformG.id)

                        updateRubro.inform.remove(objInformG.id)
                        updateRubro.informdetall.remove(objDetallG.id)

                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()
                else:
                    updateRubro.description = request.GET.get('description')
                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()

                    originId = request.GET.get('origin')
                    origin = Origin.objects.get(id=originId)
                    rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')                       
                    
                    return JsonResponse({"RUBRO": list(rubro), "MOVIMIENTO": 'FALSE'})        
            else:
                return JsonResponse({"MOVIMIENTO": 'TRUE'})    

        elif updateRubro.typeRubro == 'A' and request.GET.get('typeRubro')=='A':
            movementExists = Movement.objects.filter(nameRubro_id=request.GET.get('id')).exclude(concept='CREACION').exists()
            rubroMovement = RubroMovement.objects.filter(nameRubro_id=request.GET.get('id'), movement__concept='DISPONIBILIDAD').exists()

            if movementExists == False and rubroMovement == False:
                updateRubro.description = request.GET.get('description')
                updateRubro.initialBudget = request.GET.get('initialBudget')
                inform = json.loads(request.GET.get('inform'))
                informDetall = json.loads(request.GET.get('detallInform'))
                rbList = list(Rubro.objects.filter(id=request.GET.get('id')).values('inform__nameI','informdetall__codeInfD'))
                if rbList[0]['inform__nameI'] != None:
                    for x in range(0,len(rbList)):
                        objInformG = Inform.objects.get(nameI=rbList[x]['inform__nameI'], bussines_id=request.GET.get('idBussines'))
                        objDetallG = InformDetall.objects.get(codeInfD=rbList[x]['informdetall__codeInfD'],inform_id=objInformG.id)

                        updateRubro.inform.remove(objInformG.id)
                        updateRubro.informdetall.remove(objDetallG.id)

                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()
                else:
                    updateRubro.description = request.GET.get('description')
                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()

                    originId = request.GET.get('origin')
                    origin = Origin.objects.get(id=originId)
                    rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')                      
                    
                    return JsonResponse({"RUBRO": list(rubro), "MOVIMIENTO": 'FALSE'})        
            else:
                return JsonResponse({"MOVIMIENTO": 'TRUE'})

        elif updateRubro.typeRubro == 'M' and request.GET.get('typeRubro')=='A':


            rubroExists = Rubro.objects.filter(rubroFather=request.GET.get('id'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()
            if rubroExists == False:           
                updateRubro.description = request.GET.get('description')
                updateRubro.typeRubro = 'A'
                updateRubro.save()                             
                originId = request.GET.get('origin')
                origin = Origin.objects.get(id=originId)
                rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')                               
                return JsonResponse({"RUBRO": list(rubro), "SOY_FATHER": 'FALSE'})
            else:
                return JsonResponse({"SOY_FATHER": 'TRUE'})  
        else:
            updateRubro.description = request.GET.get('description')
            updateRubro.typeRubro = 'A'
            updateRubro.save()  
            originId = request.GET.get('origin')
            origin = Origin.objects.get(id=originId)
            rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')                               
            return JsonResponse({"RUBRO": list(rubro), "SOY_FATHER": 'FALSE'})
                   
        

class DeleteRubro(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):
        deleteRubro = Rubro.objects.get(id=request.GET.get('id'))
        option = request.GET.get('option')
        if deleteRubro.typeRubro == 'M':
            rubroExists = Rubro.objects.filter(rubroFather=request.GET.get('id'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()
            if rubroExists == False:
                if option=='1':
                    deleteRubro = Rubro.objects.get(id=request.GET.get('id'))
                    deleteRubro.delete()
                    
                    originId = request.GET.get('origin')
                    origin = Origin.objects.get(id=originId)
                    rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','budgetEject').order_by('rubro')
                    
                    return JsonResponse({'ELIMINADO': 'TRUE', "RUBRO": list(rubro)})
                else:
                    return JsonResponse({'ELIMINADO': 'FALSE'})
            else:
                return JsonResponse({"SOY_FATHER": 'TRUE'})
        else:
            movementExists = Movement.objects.filter(nameRubro_id=request.GET.get('id')).exclude(concept='CREACION').exists()
            rubroMovement = RubroMovement.objects.filter(nameRubro_id=request.GET.get('id'), movement__concept='DISPONIBILIDAD').exists()
            if movementExists == False and rubroMovement == False:
                deleteRubro = Rubro.objects.get(id=request.GET.get('id'))
                deleteRubro.delete()
                   
                originId = request.GET.get('origin')
                origin = Origin.objects.get(id=originId)
                rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')
                        
                return JsonResponse({'ELIMINADO': 'TRUE', "RUBRO": list(rubro)})        
            else:
                return JsonResponse({'MOVEMENTS': 'TRUE'}) 

class GetRubrosOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        rubros = Rubro.objects.filter(origin_id=request.GET.get('origin'), bussines_id=request.GET.get('bussines')).values('id','rubro','typeRubro','description','initialBudget','realBudget','budgetEject').order_by('rubro')
        return JsonResponse({"RUBRO": list(rubros)}) 

class GetUpdateOperationByOperate(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        print(request.GET.get('origin'),request.GET.get('operation'))
        origin = Origin.objects.get(id=request.GET.get('origin'))
        operation = Operation.objects.get(nameOp=request.GET.get('operation'), origin=origin)
        return JsonResponse({"OP": operation.operation})

class UpdateOperations(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def post(self, request, *args, **kwargs):
        agreementupdate = json.loads(request.POST.get('agreement'))
        agreement = Agreement.objects.get(id = agreementupdate[0]['id'])

        updateOperation = json.loads(request.POST.get('updateOperation'))
        updateContraOperation = json.loads(request.POST.get('updateContraOperation'))
        today = datetime.now()
        va = 0
        contrabalance = 0
        print(updateOperation,"-")
        print(updateContraOperation)
        for x in range(0,len(updateOperation)):
            print(updateOperation[x],x)
            if updateOperation[x]['new'] == True:
                print(updateOperation[x],'nuevo')
                bussines = Bussines.objects.get(id=request.POST.get('bussines'))
                rubro = Rubro.objects.get(rubro=updateOperation[x]['id'])
                movement = Movement.objects.create(bussines=bussines,nameRubro_id=rubro.id,concept=updateOperation[x]['concept'], value=updateOperation[x]['value'],balance=updateOperation[x]['balance'],date=today,agreement_id=agreementupdate[0]['id'],budgetEject=updateOperation[x]['byEject'],origin_id=request.POST.get('origin'))
                movement =  Movement.objects.last()
                rubroMov = RubroMovement.objects.create(bussines = bussines,value=updateOperation[x]['value'],valueP=rubro.realBudget,balance=updateOperation[x]['balance'],date=today,nameRubro_id=rubro.id,movement_id=movement.id) 
                rubroBalanceMov = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation=updateOperation[x]['concept'],value=updateOperation[x]['value'],balance=updateOperation[x]['balance'],date=today,nameRubro_id=rubro.id,movement_id=movement.id) 
                rubro.realBudget = updateOperation[x]['balance']
                rubro.budgetEject = updateOperation[x]['byEject']
                rubro.save()
            else:
                print(updateOperation[x],'Modificar')
                rubro = Rubro.objects.get(rubro=updateOperation[x]['rubro'])
                movementfilter = Movement.objects.filter(nameRubro_id=rubro.id,agreement_id__isnull=False).values('concept','balance','id','value')
                print(rubro,'rubro')
                print(movementfilter,'movimiento')
                if updateOperation[x]['Valuelast'] !=  updateOperation[x]['value']:
                    print('valor diferente')
                    movement = Movement.objects.get(id=updateOperation[x]['id'])
                    for y in range(0,len(movementfilter)):

                        if movementfilter[y]['id'] > updateOperation[x]['id']:
                            
                            print(movementfilter[y], "mayor")
                            operation = Operation.objects.filter(nameOp = movementfilter[y]['concept']).values('operation')

                            if(operation[0]['operation'] == '+'):

                                valueBalance = (movementfilter[y]['balance'] - updateOperation[x]['Valuelast']) + updateOperation[x]['value']
                            
                            elif(operation[0]['operation'] == '-'):

                                valueBalance = (movementfilter[y]['balance'] + updateOperation[x]['Valuelast']) - updateOperation[x]['value']
                            
                            
                            print(valueBalance, "nuevo valor")
                            updaterubros = Movement.objects.get(id = movementfilter[y]['id'])
                            updaterubros.balance = valueBalance
                            updaterubros.budgetEject = valueBalance
                            updaterubros.save()

                            updaterubroMov = RubroMovement.objects.get(movement_id = movementfilter[y]['id'])
                            updaterubroMov.balance = valueBalance
                            updaterubroMov.save()

                            rubroBalanceMov = RubroBalanceOperation.objects.get(movement_id=movementfilter[y]['id'])
                            rubroBalanceMov.balance = valueBalance
                            rubroBalanceMov.save()

                            rubro.realBudget = valueBalance
                            rubro.budgetEject = valueBalance
                            

                        else:
                            print(movementfilter[y], "No tiene")
                            rubro.realBudget = updateOperation[x]['balance']
                            rubro.budgetEject = updateOperation[x]['byEject']

                                #print(va,movementfilter[y]['balance'], updateOperation[x]['Valuelast'], movementfilter[y]['value'], updateOperation[x]['balance'],movementfilter[y]['id'] ,"\n")
                    movement.budgetEject = updateOperation[x]['byEject']
                    movement.balance = updateOperation[x]['balance']
                    movement.value = updateOperation[x]['value']
                    movement.date = today
                    movement.save()

                    rubroMov = RubroMovement.objects.get(movement_id = updateOperation[x]['id'])
                    rubroMov.value = updateOperation[x]['value']
                    rubroMov.balance = updateOperation[x]['balance']
                    rubroMov.date = today
                    rubroMov.save()
                    
                    rubroBalanceMov = RubroBalanceOperation.objects.get(movement_id=updateOperation[x]['id'])
                    rubroBalanceMov.value = updateOperation[x]['value']
                    rubroBalanceMov.balance = updateOperation[x]['balance']
                    rubroBalanceMov.date = today
                    rubroBalanceMov.save()
            
                rubro.save()    

        for x in range(0,len(updateContraOperation)):
            if updateContraOperation[x]['new']==True:
                bussines = Bussines.objects.get(id=request.POST.get('bussines'))
                contraRubro = Rubro.objects.get(rubro=updateContraOperation[x]['id'])
                contramovement = Movement.objects.create(bussines=bussines,nameRubro_id=contraRubro.id,concept=updateContraOperation[x]['concept'], value=updateContraOperation[x]['value'],balance=updateContraOperation[x]['balance'],date=today, agreement_id=agreementupdate[0]['id'],budgetEject=updateContraOperation[x]['byEject'],origin_id=request.POST.get('origin'))
                contramovement =  Movement.objects.last()
                contraRubroMov = RubroMovement.objects.create(bussines = bussines,value=updateContraOperation[x]['value'],valueP=contraRubro.realBudget,balance=updateContraOperation[x]['balance'],date=today,nameRubro_id=contraRubro.id,movement_id=contramovement.id) 
                contraRubroBalanceMov = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation=updateContraOperation[x]['concept'],value=updateContraOperation[x]['value'],balance=updateContraOperation[x]['balance'],date=today,nameRubro_id=contraRubro.id,movement_id=contramovement.id) 
                contraRubro.realBudget = updateContraOperation[x]['balance']
                contraRubro.budgetEject = updateContraOperation[x]['byEject']
                contraRubro.save()
            else:
                
                Contrarubro = Rubro.objects.get(rubro=updateContraOperation[x]['rubro'])
                Contramovement = Movement.objects.get(id=updateContraOperation[x]['id'])

                if updateContraOperation[x]['value'] != updateContraOperation[x]['Valuelast']:

                    contramovementfilter = Movement.objects.filter(nameRubro_id=Contrarubro.id,agreement_id__isnull=False).values('concept','balance','id','value')
                    
                    for y in range(0,len(contramovementfilter)):
                        if contramovementfilter[y]['id'] > updateContraOperation[x]['id']:
                            operation = Operation.objects.filter(nameOp = contramovementfilter[y]['concept']).values('operation')
                            if(operation[0]['operation'] == '+'):
                                contrabalance = (contramovementfilter[y]['balance'] -  updateContraOperation[x]['Valuelast']) + updateContraOperation[x]['value']
                            elif (operation[0]['operation'] == '-'):
                                contrabalance = (contramovementfilter[y]['balance'] +  updateContraOperation[x]['Valuelast']) - updateContraOperation[x]['value']
                                updatecontrarubros = Movement.objects.get(id= contramovementfilter[y]['id'])
                                updatecontrarubros.balance = contrabalance
                                updatecontrarubros.budgetEject = contrabalance
                                updatecontrarubros.save()

                                uContrarubroMov = RubroMovement.objects.get(movement_id = contramovementfilter[y]['id'])
                                uContrarubroMov.balance = contrabalance
                                uContrarubroMov.save()

                                uContrarubroBalanceMov = RubroBalanceOperation.objects.get(movement_id=contramovementfilter[y]['id'])
                                uContrarubroBalanceMov.balance = contrabalance
                                uContrarubroBalanceMov.save()

                                Contrarubro.realBudget = contrabalance
                                Contrarubro.budgetEject = contrabalance
                        else:
                            Contrarubro.realBudget = updateContraOperation[x]['balance']
                            Contrarubro.budgetEject = updateContraOperation[x]['byEject']



                    Contramovement.budgetEject = updateContraOperation[x]['byEject']
                    Contramovement.balance = updateContraOperation[x]['balance']
                    Contramovement.value = updateContraOperation[x]['value']
                    Contramovement.date = today
                    Contramovement.save()

                    ContrarubroMov = RubroMovement.objects.get(movement_id = updateContraOperation[x]['id'])
                    ContrarubroMov.value = updateContraOperation[x]['value']
                    ContrarubroMov.balance = updateContraOperation[x]['balance']
                    ContrarubroMov.date = today
                    ContrarubroMov.save()

                    ContrarubroBalanceMov = RubroBalanceOperation.objects.get(movement_id=updateContraOperation[x]['id'])
                    ContrarubroBalanceMov.value = updateContraOperation[x]['value']
                    ContrarubroBalanceMov.balance = updateContraOperation[x]['balance']
                    ContrarubroBalanceMov.date = today
                    ContrarubroBalanceMov.save()
                
                Contrarubro.save()
            
                    
                    


        agreement.numberAg = agreementupdate[0]['numberAg']
        agreement.dateAg = agreementupdate[0]['dateAg']
        agreement.descriptionAg = agreementupdate[0]['description']
        agreement.save()

        return JsonResponse({"OP":"TRUE"}) 

class GetOperationByOperate(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        origin = Origin.objects.get(id=request.GET.get('origin'))
        operation = Operation.objects.get(nameOp=request.GET.get('operation'), origin=origin)
        if operation.contraOperar == None:
            return JsonResponse({"OP": operation.operation,"CO": "No tiene agregado contraoperaciones"}) 
        else:
            contraOperation = Operation.objects.get(id=operation.contraOperar)
            contraoring = Origin.objects.get(id=operation.contraOrigin)
            return JsonResponse({"OP": operation.operation,"CO": contraOperation.nameOp, "NCO":contraoring.nameOrigin,"NOP":origin.nameOrigin}) 

class GetRubrosContraOperation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        operation = Operation.objects.get(nameOp=request.GET.get('operation'), origin=Origin.objects.get(id=request.GET.get('origin')))
        idContraOperation = operation.contraOperar
        contraoperation = Operation.objects.get(id=idContraOperation)
        rubros = Rubro.objects.filter(origin_id=operation.contraOrigin, bussines_id=request.GET.get('bussines')).values('id','rubro','typeRubro','description','initialBudget','realBudget','budgetEject').order_by('rubro')
        return JsonResponse({"RUBRO": list(rubros), "CONTRAOPERACION": str(contraoperation.operation),"NAME": contraoperation.nameOp}) 

class DeleteOperations(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def post(self, request, *args, **kwargs):
        deleteOperation = json.loads(request.POST.get('Operation'))
        va = 0
        print(deleteOperation,"elminar")
        for x in range(0,len(deleteOperation)):
            rubro = Rubro.objects.get(rubro=deleteOperation[x]['rubro'])
            movementfilter = Movement.objects.filter(nameRubro_id=rubro.id,agreement_id__isnull=False).values('concept','balance','id','value')
            print(list(movementfilter),"cambios",x)
            for y in range(0,len(movementfilter)):
                if movementfilter[y]['id'] > deleteOperation[x]['id']:
                    operation = Operation.objects.filter(nameOp = movementfilter[y]['concept']).values('operation')
                    if(operation[0]['operation'] == '+'):
                        va = movementfilter[y]['balance'] -  deleteOperation[x]['value']
                    elif(operation[0]['operation'] == '-'):
                        va = movementfilter[y]['balance'] +  deleteOperation[x]['value']
                    updaterubros = Movement.objects.get(id= movementfilter[y]['id'])
                    updaterubros.balance = va
                    updaterubros.budgetEject = va
                    updaterubros.save()

                    updaterubroMov = RubroMovement.objects.get(movement_id = movementfilter[y]['id'])
                    updaterubroMov.balance = va
                    updaterubroMov.save()

                    rubroBalanceMov = RubroBalanceOperation.objects.get(movement_id=movementfilter[y]['id'])
                    rubroBalanceMov.balance = va
                    rubroBalanceMov.save()

                    rubro.realBudget = va
                    rubro.budgetEject = va
                    print(movementfilter[y]['id'],va, "oper")
            if va ==  0:
                rubro.realBudget = deleteOperation[x]['balance']
                rubro.budgetEject = deleteOperation[x]['budgetEject']
            rubro.save()

        for x in range(0,len(deleteOperation)):
            rubroMov = RubroMovement.objects.filter(movement_id=deleteOperation[x]['id']).delete()
            rubroBalanceMov = RubroBalanceOperation.objects.filter(movement_id=deleteOperation[x]['id']).delete()
            movement = Movement.objects.filter(id=deleteOperation[x]['id']).delete()   
                    

        return JsonResponse({"OP":"TRUE"})

class DeleteAgreementsOperations(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def post(self, request, *args, **kwargs):
        agreementupdate = json.loads(request.POST.get('agreement'))
        agreement = Agreement.objects.get(id = agreementupdate[0]['id'])
        agreement.delete()
        return JsonResponse({"OP":"TRUE"}) 

class Mayorizacion(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def post(self, request, *args, **kwargs):
        agreement = Rubro.objects.filter(bussines_id = 1).values('id','rubro','rubroFather','typeRubro','realBudget','budgetEject').order_by('rubro')
        print(agreement)
        for x in range(0,len(agreement)):
            if(agreement[x]['typeRubro']=='M'):
                agreement[x]['realBudget'] = 0
                agreement[x]['budgetEject'] = 0
            if(agreement[x]['typeRubro']=='A'):
                rubrofather = agreement[x]['rubroFather']
                while(rubrofather != None ):
                    ru = Rubro.objects.get(id=rubrofather)
                    ru.realBudget = ru.realBudget + agreement[x]['realBudget']
                    ru.budgetEject =  ru.budgetEject + agreement[x]['budgetEject']
                    rubrofather = ru.rubroFather
                    ru.save()
        agreement.save()
        return JsonResponse({"OP":"TRUE"}) 

class CreateOperations(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def post(self, request, *args, **kwargs):
        agreement = Agreement.objects.create(
           origin_id = request.POST.get('origin'),
           numberAg = request.POST.get('number'),
           descriptionAg = request.POST.get('concept'),
           dateAg = request.POST.get('date'),
           typeAgreement = TypeAgreement.objects.get(nameTA=request.POST.get('typeAgreement'), bussines_id=request.POST.get('bussines'))
        )

        operation = json.loads(request.POST.get('operation'))
        contraoperation = json.loads(request.POST.get('contraoperation'))

        print(operation)
        print("Salto")
        print(contraoperation)
        bussines = Bussines.objects.get(id=request.POST.get('bussines'))
        agreement =  Agreement.objects.last()
        today = datetime.now()
        for x in range(0,len(operation)):
            bussines = Bussines.objects.get(id=request.POST.get('bussines'))
            rubro = Rubro.objects.get(id=operation[x]['id'])
            rubrofather = rubro.rubroFather
            movement = Movement.objects.create(bussines=bussines,nameRubro_id=operation[x]['id'],concept=operation[x]['concept'], value=operation[x]['value'],balance=operation[x]['balance'],date=today,agreement=agreement,budgetEject=operation[x]['byEject'],origin_id=request.POST.get('origin'))
            movement =  Movement.objects.last()
            rubroMov = RubroMovement.objects.create(bussines = bussines,value=operation[x]['value'],valueP=rubro.realBudget,balance=operation[x]['balance'],date=today,nameRubro_id=operation[x]['id'],movement_id=movement.id) 
            rubroBalanceMov = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation=operation[x]['concept'],value=operation[x]['value'],balance=operation[x]['balance'],date=today,nameRubro_id=operation[x]['id'],movement_id=movement.id) 
            rubro.realBudget = operation[x]['balance']
            rubro.budgetEject = operation[x]['byEject']
            rubro.save()
            """ while(rubrofather != None ):
                operate = Operation.objects.filter(nameOp = operation[x]['concept']).values('operation')
                ru = Rubro.objects.get(id=rubrofather)
                if operate[0]['operation'] == '+':
                    print("1",ru.realBudget,ru.budgetEject ,operation[x]['value'])
                    ru.realBudget = ru.realBudget + operation[x]['value']
                    ru.budgetEject =  ru.budgetEject + operation[x]['value']
                    print("2",ru.realBudget,ru.budgetEject, operation[x]['value'])
                    ru.save()
                    
                elif operation[0]['operation'] == '-':
                    ru.realBudget = ru.realBudget - operation[x]['value']
                    ru.budgetEject = ru.budgetEject  -operation[x]['value']
                    ru.save()
               
                rubrofather = ru.rubroFather """

        for x in range(0,len(contraoperation)):
            contraRubro = Rubro.objects.get(id=contraoperation[x]['id'])
            contrarubrofather = contraRubro.rubroFather
            contramovement = Movement.objects.create(bussines=bussines,nameRubro_id=contraoperation[x]['id'],concept=contraoperation[x]['concept'], value=contraoperation[x]['value'],balance=contraoperation[x]['balance'],date=today,agreement=agreement,budgetEject=contraoperation[x]['byEject'],origin_id=request.POST.get('origin'))
            contramovement =  Movement.objects.last()
            contraRubroMov = RubroMovement.objects.create(bussines = bussines,value=contraoperation[x]['value'],valueP=contraRubro.realBudget,balance=contraoperation[x]['balance'],date=today,nameRubro_id=contraoperation[x]['id'],movement_id=contramovement.id) 
            contraRubroBalanceMov = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation=contraoperation[x]['concept'],value=contraoperation[x]['value'],balance=contraoperation[x]['balance'],date=today,nameRubro_id=contraoperation[x]['id'],movement_id=contramovement.id) 
            contraRubro.realBudget = contraoperation[x]['balance']
            contraRubro.budgetEject = contraoperation[x]['byEject']
            contraRubro.save()
            """ while(contrarubrofather != None ):
                contoperation = Operation.objects.filter(nameOp = contraoperation[x]['concept']).values('operation')
                coru = Rubro.objects.get(id=contrarubrofather)
                if contoperation[0]['operation'] == '+':
                    coru.realBudget = coru.realBudget + contraoperation[x]['value']
                    coru.budgetEject =coru.budgetEject + contraoperation[x]['value']
                    coru.save()
                elif contoperation[0]['operation'] == '-':
                    coru.realBudget = coru.realBudget  - contraoperation[x]['value']
                    coru.budgetEject = coru.budgetEject - contraoperation[x]['value']
                    coru.save()
               
                contrarubrofather = coru.rubroFather """

        return JsonResponse({"OP":"TRUE"}) 

def ImportRubro(request,idBussines, idOrigin):

    if request.method == 'POST':
        dataset = Dataset() 
        newRubros = request.FILES['myfile']  
        importedData = dataset.load(newRubros.read())  
        today = datetime.now()
        for fila in importedData:
            rubroExists = Rubro.objects.filter(rubro=fila[1],bussines_id=idBussines,origin_id=idOrigin).exists()
            if rubroExists == False:
                if len(fila[1]) != 1:
                    value = searchImport(request,fila[1],idOrigin,idBussines,1)
                    filaRubro=str(fila[1])
                    getRubro = Rubro.objects.get(rubro=filaRubro[:-request.session.get('num')],bussines_id=idBussines,origin_id=idOrigin)
                    if  fila[0] == "A":
                        Rubro.objects.create(
                            bussines_id = idBussines,origin_id = idOrigin, rubroFather= getRubro.id, 
                            rubro = fila[1], nivel =getRubro.nivel+1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "A", realBudget=fila[3], imported="TRUE", 
                        )
                    else:
                        Rubro.objects.create(
                            bussines_id = idBussines, 
                            origin_id = idOrigin, rubroFather= getRubro.id,
                            rubro = fila[1], nivel =  getRubro.nivel+1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "M", realBudget=fila[3], imported="TRUE",
                        )
                else: 
                    if  fila[0] == "A":
                        Rubro.objects.create(
                                bussines_id = idBussines,origin_id = idOrigin, 
                                rubro = fila[1], nivel = 1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "A", realBudget=fila[3], imported="TRUE", 
                        )
                    else:
                        Rubro.objects.create(
                                bussines_id = idBussines, origin_id = idOrigin, 
                                rubro = fila[1], nivel = 1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "M", realBudget=fila[3], imported="TRUE",
                        )                    
            else:
                break
        return render(request, 'budget/chargeRubro.html')
    else:     
        return render(request, 'budget/chargeRubro.html')

class SearchRubroTw(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        rubroLen = request.GET.get('rubro')
        print(request.GET.get('rubroFather'))
        if len(rubroLen) == 1:
            return JsonResponse({"RUBROFATHER": "PRIMER RUBRO"})
        else:  
            ccpetValidate = CCPET.objects.filter(code=request.GET.get('rubroFather'),accountPeriod_id=request.GET.get('period')).exists()
            if ccpetValidate:
                ccpetValidate = CCPET.objects.filter(code=request.GET.get('rubroFather'),accountPeriod_id=request.GET.get('period')).values('type')

                if list(ccpetValidate)[0]['type'] == 'M':
                    return JsonResponse({"RubroMayor": True})
                else :
                    rubroExists = Rubro.objects.filter(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()

                    if rubroExists:

                        rubroNewExists = Rubro.objects.filter(rubro=request.GET.get('rubro'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()
                        
                        if rubroNewExists:
                            return JsonResponse({"Rubro": False, "RubroNew": False })
                        else:

                            last = Rubro.objects.all().last()
                            return JsonResponse({"Rubro": True, "RubroNew": True ,"RubroMayor": False,"LAST":last.rubro})
                        
                    else:
                        return JsonResponse({"Rubro": False, "RubroNew": False ,"LAST":last.rubro})
            else:
                rubroExists2 = Rubro.objects.filter(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()
                if rubroExists2:
                    rubro = Rubro.objects.filter(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).values('typeRubro')
                    if list(rubro)[0]['typeRubro'] == 'A':
                        """ rubroAuxiliar = Rubro.objects.get(rubro=request.GET.get('rubro'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin'))
                        rubroAuxiliar.typeRubro = 'M'
                        rubroAuxiliar.save() """

                        last = Rubro.objects.all().last()
                        return JsonResponse({"Rubro": True, "RubroNew": True,"RubroMayor": False,"LAST":last.rubro})
                else:
                    return JsonResponse({"Rubro": False,"RubroNew": False })

            """ if rubroExists2 :
                rubroExists = Rubro.objects.get(rubro=request.GET.get('rubro'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin'))
            else:
                
                rubro = request.GET.get('rubro')
                rubroExists = Rubro.objects.get(rubro=rubro,bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin'))
            last = Rubro.objects.all().last()
            return JsonResponse({"RUBROFATHER": "TRUE","LAST":last.rubro}) """


def rubroFatherValue(request, rubroFather, value):
    if(value != 0):
        rubroFather = Rubro.objects.get(id=rubroFather)   
        currentRealBudget = rubroFather.realBudget
        newRealBudget = currentRealBudget + value
        rubroFather.realBudget = newRealBudget
        rubroFather.budgetEject = newRealBudget
        rubroFather.save()
        if rubroFather.rubroFather == None:
            return True
        else:        
            return rubroFatherValue(request, rubroFather.rubroFather, value)


def searchImport(request, rubro,origin,bussines,discount):
    
    rubroExist = Rubro.objects.filter(rubro=rubro[:-discount],bussines_id=bussines,origin_id=origin).exists()
    
    if rubroExist==False:
        searchImport(request,rubro,origin,bussines,discount+1)
    else:
        request.session['num'] = discount
        return discount

class GetAgreement(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        print(request.GET.get('typeAgreement'),request.GET.get('bussines'))
        typeAgreement = TypeAgreement.objects.get(nameTA=request.GET.get('typeAgreement'), bussines_id=request.GET.get('bussines'))
        agreement =  Agreement.objects.filter(numberAg=request.GET.get('number'),origin_id = request.GET.get('origin'),typeAgreement_id = typeAgreement).exists()
        
        print(agreement)
        if agreement :
            return JsonResponse({"Exist": True})
        else:
            return JsonResponse({"Exist": False})


class GetDetallAgreement(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        rubros = []
        movements =  Movement.objects.filter(agreement_id=request.GET.get('agreement')).values('concept','value','balance','date','nameRubro','budgetEject')
        for x in range(0,len(movements)):
            rubros += Rubro.objects.filter(id = movements[x]['nameRubro'],bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origen')).values('initialBudget','realBudget','budgetEject','rubro','description')

        return JsonResponse({"MV": list(movements), "MR": list(rubros)})


class GetRubroOperationDetail(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        movements = RubroBalanceOperation.objects.filter(nameRubro_id=request.GET.get('id')).values('typeOperation','value','balance','date')
        return JsonResponse({"MVRUBRO": list(movements)})



class ImportRubrosBD(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  post(self, request, *args, **kwargs):
   
        bussines = request.POST.get('idBussines')
        rubrost = request.POST.get('rubros')
        rubros = json.loads(rubrost)
        origin = request.POST.get('origin')
        today = datetime.now()

        ccpet = CCPET.objects.all();

        if len(list(ccpet)) > 0:
            for x in range(0,len(rubros)):
                rubroExists = Rubro.objects.filter(rubro=rubros[x]['RB'],bussines_id=bussines,origin_id=origin).exists()
                if rubroExists == False:
                    if len(rubros[x]['RB']) != 1:
                        value = searchImport(request,rubros[x]['RB'],origin,bussines,1)
                        filaRubro=str(rubros[x]['RB'])
                        getRubro = Rubro.objects.get(rubro=filaRubro[:-request.session.get('num')],bussines_id=bussines,origin_id=origin)

                        existccpet = CCPET.objects.filter(code=rubros[x]['RB'],accountPeriod_id=request.POST.get('period')).exists()

                        if existccpet == True:
                            if  rubros[x]['TC'] == "A":
                                newRubro = Rubro.objects.create(
                                    bussines_id = bussines,origin_id = origin, rubroFather= getRubro.id, 
                                    ccpet = 1,
                                    rubro = rubros[x]['RB'], nivel =getRubro.nivel+1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "A", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                                )
                                movement = Movement.objects.create(bussines_id = bussines,  nameRubro_id = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today, origin_id=origin) 
                            else:
                                newRubro =Rubro.objects.create(
                                    bussines_id = bussines, 
                                    ccpet = 1,
                                    origin_id = origin, rubroFather= getRubro.id,
                                    rubro = rubros[x]['RB'], nivel =  getRubro.nivel+1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "M", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                                )
                                movement = Movement.objects.create(bussines_id = bussines, nameRubro_id = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today)
                        else:
                            if  rubros[x]['TC'] == "A":
                                newRubro = Rubro.objects.create(
                                    bussines_id = bussines,origin_id = origin, rubroFather= getRubro.id, 
                                    ccpet = 0,
                                    rubro = rubros[x]['RB'], nivel =getRubro.nivel+1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "A", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                                )
                                movement = Movement.objects.create(bussines_id = bussines,  nameRubro_id = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today, origin_id=origin) 
                            else:
                                newRubro =Rubro.objects.create(
                                    bussines_id = bussines, 
                                    ccpet = 0,
                                    origin_id = origin, rubroFather= getRubro.id,
                                    rubro = rubros[x]['RB'], nivel =  getRubro.nivel+1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "M", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                                )
                                movement = Movement.objects.create(bussines_id = bussines, nameRubro_id = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today) 

                    else: 
                        existccpet = CCPET.objects.filter(code=rubros[x]['RB'],accountPeriod_id=request.POST.get('period')).exists()

                        if existccpet == True:
                            if  rubros[x]['TC'] == "A":
                                newRubro = Rubro.objects.create(
                                        bussines_id = bussines,origin_id = origin, 
                                        ccpet = 1,
                                        rubro = rubros[x]['RB'], nivel = 1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "A", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                                )
                                movement = Movement.objects.create(bussines_id = bussines,  nameRubro_id = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today,origin_id=origin)                 
                            else:
                                newRubro = Rubro.objects.create(
                                        bussines_id = bussines, origin_id = origin, 
                                     ccpet = 1,
                                        rubro = rubros[x]['RB'], nivel = 1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "M", realBudget=rubros[x]['PI'], budgetEject=rubros[x]['PI'],imported="TRUE"
                                ) 
                                print(type(newRubro.id),newRubro)
                                movement = Movement.objects.create(bussines_id = bussines, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today,  nameRubro_id = newRubro.id) 
                        else:
                            if  rubros[x]['TC'] == "A":
                                newRubro = Rubro.objects.create(
                                        bussines_id = bussines,origin_id = origin, 
                                        ccpet = 0,
                                        rubro = rubros[x]['RB'], nivel = 1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "A", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                                )
                                movement = Movement.objects.create(bussines_id = bussines,  nameRubro_id = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today,origin_id=origin)                 
                            else:
                                newRubro = Rubro.objects.create(
                                        bussines_id = bussines, origin_id = origin, 
                                     ccpet = 0,
                                        rubro = rubros[x]['RB'], nivel = 1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "M", realBudget=rubros[x]['PI'], budgetEject=rubros[x]['PI'],imported="TRUE"
                                ) 
                                print(type(newRubro.id),newRubro)
                                movement = Movement.objects.create(bussines_id = bussines, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today,  nameRubro_id = newRubro.id) 

                            
                    rubroinfordetall =  Rubro.objects.last()
                    RubroAuxiliar = Rubro.objects.filter(id = rubroinfordetall.id).values('typeRubro')
                    if(RubroAuxiliar[0]['typeRubro']=='A'):
                        for inform in Inform.objects.all():
                            informdetallExist = InformDetall.objects.filter(inform_id = inform.id).exists()
                            newRubroInform = RubroInform.objects.create(
                                    rubro_id = rubroinfordetall.id,
                                    inform_id = inform.id
                                ) 
                            if(informdetallExist):
                                informdetall = InformDetall.objects.filter(inform_id = inform.id).values('id')
                                for x in informdetall:
                                    print(x['id'])
                                    newRubroInformDetall = RubroInformdetall.objects.create(
                                        rubro_id = rubroinfordetall.id,
                                        informdetall_id = x['id'],
                            )   
                else:
                    return JsonResponse({"IMPORT": "FALSE"})
                    break
            rubros = Rubro.objects.filter(bussines_id=bussines,origin_id=origin).values('id','rubro','description','initialBudget','budgetEject','typeRubro','realBudget').order_by('rubro')
            return JsonResponse({"IMPORT": "TRUE","RUBRO": list(rubros)})
        else:
            return JsonResponse({"IMPORTCCPET": "FALSE"})

class UpdateAgreementRubro(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs):
        typeagreement = []
        updateAgreement = Agreement.objects.get(id=request.GET.get('id'))
        listAgreement = Agreement.objects.filter(origin_id=request.GET.get('origin')).values('id', 'typeAgreement', 'numberAg', 'descriptionAg')
        
        updateAgreement.numberAg = request.GET.get('numberAg')
        updateAgreement.dateAg = request.GET.get('dateAg')
        updateAgreement.descriptionAg = request.GET.get('descriptionAg').upper()
        updateAgreement.typeAgreement_id =  request.GET.get('idtypeagreement')
        updateAgreement.save()
        for x in range(0,len(listAgreement)):
            typeagreement += TypeAgreement.objects.filter(id = listAgreement[x]['typeAgreement']).values('nameTA')
        return JsonResponse({'CREATE':"TRUE", 'AG':list(listAgreement), 'TA':list(typeagreement)})

class DeleteRubrosImported(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  post(self, request, *args, **kwargs):

        rubrost = request.POST.get('rubros')
        rubros = json.loads(rubrost)
        for x in range(0,len(rubros)):
            rubro = Rubro.objects.get(bussines_id=request.POST.get('idBussines'),origin_id = request.POST.get('origin'),rubro=rubros[x]['RB'])
            if rubro != None:
                rubro.delete()

        return JsonResponse({"DELETE": "TRUE"})



class GetMovementsByOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        movement = Movement.objects.filter(origin_id=request.GET.get('origin')).exclude(concept='CREACION').exists()
        print(movement)
        print(Movement.objects.filter(origin_id=request.GET.get('origin')).exclude(concept='CREACION'))
        if movement == True:
            return JsonResponse({"MOVEMENTS": "TRUE"})
        else:
            return JsonResponse({"MOVEMENTS": "FALSO"})

class GetDisponibilityByRubros(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        rubroMovement = RubroMovement.objects.filter(nameRubro_id=request.GET.get('id'),movement__concept='DISPONIBILIDAD').exists()
        if rubroMovement == True:
            rubroMovement = RubroMovement.objects.filter(nameRubro_id=request.GET.get('id'),movement__concept='DISPONIBILIDAD').aggregate(total_value=Sum('value'))
            listRubroMovement = RubroMovement.objects.filter(nameRubro_id=request.GET.get('id'),movement__concept='DISPONIBILIDAD').values('id')
            print(listRubroMovement)
            return JsonResponse({"DP": rubroMovement['total_value']})
        else:
            return JsonResponse({"DP": 0})



class DeleteAccount(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):
        print(request.GET.get('id'))
        deleteAccount = Account.objects.filter(id=request.GET.get('id')).values('typeAccount')
        option = request.GET.get('option')
        print(list(deleteAccount))
        if deleteAccount[0]['typeAccount'] == 'M':
            AccountExists = Account.objects.filter(accountFather=request.GET.get('id'),accountPeriod_id=request.GET.get('accountPeriod')).exists()
            accountingSeatExists = ValuesAccountObligation.objects.filter(account__account_id=request.GET.get('id')).exists()
            if AccountExists == False and accountingSeatExists == False:
                deleteAccount = Account.objects.get(id=request.GET.get('id'))
                deleteAccount.delete()
                return JsonResponse({'ELIMINADO': 'TRUE'})
            else:
                return JsonResponse({"SOY_FATHER": 'TRUE'})
        else:
            parametrizacionExists = AccountTypeRubro.objects.filter(account_id=request.GET.get('id')).exists()
            if parametrizacionExists == False:
                deleteAccount = Account.objects.get(id=request.GET.get('id'))
                deleteAccount.delete()
                return JsonResponse({'ELIMINADO': 'TRUE'})        
            else:
                return JsonResponse({'MOVEMENTS': 'TRUE'}) 


class GetClosedMounth(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        print(request.GET.get('period'))
        closed = ClosedPeriod.objects.filter(accountPeriod_id = request.GET.get('period')).values('id','month','year','activate')    
        period = AccountPeriod.objects.get(id = request.GET.get('period'))
        print(closed)
        return JsonResponse({"CM":list(closed),"NM":period.name})


class DeactivateMonth(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        closed = ClosedPeriod.objects.get(id = request.GET.get('idMes'))  
        if request.GET.get('activate') == 'false':
            closed.activate =  False
            closed.save()
        return JsonResponse({"TRUE":"CREATE"})

class GetDatePeriod(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        closed = ClosedPeriod.objects.filter(accountPeriod_id = request.GET.get('id')).values('month','year','activate')
        return JsonResponse({"LCP":list(closed)})



class GetPatternOrigin(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        closed = ClosedPeriod.objects.filter(accountPeriod_id = request.GET.get('id')).values('month','year','activate')
    
        Pattern = Origin.objects.filter(nameOrigin = request.GET.get('origin'), accountPeriod_id =  request.GET.get('idAC')).values('pattern')
        
        
        return JsonResponse({"PT":list(Pattern)})
