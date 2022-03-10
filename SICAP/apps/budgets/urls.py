from django.conf.urls import url, include
from apps.budgets.views import *

urlpatterns = [

    url(r'bussines/base', base , name='index'),
    url(r'budget/createBudget/(?P<pkUser>\d+)/', mainBudget , name='menu'),
    url(r'bussines/createBussines', CreateBussines.as_view(), name='createBussines'), 
    url(r'bussines/listBussines', ListBussines.as_view(), name='listBussines'),
    url(r'ajax/createAC/(?P<pkUser>\d+)/', CreateAccountPeriod.as_view(), name='createAccountPeriod'),
    url(r'ajax/createOriginAC/(?P<pkUser>\d+)/', GetAccountPeriodOrigin.as_view(), name='getAccountPeriodOrigin'),
    url(r'ajax/createBudget/(?P<pkUser>\d+)/', GetOriginBudget.as_view(), name='getOriginBudget'),
    url(r'bussines/createOperation', CreateOperation.as_view(), name='createOperation'),
    url(r'ajax/createAccountPeriodOp/(?P<pkUser>\d+)/', GetAccountPeriodOperation.as_view(), name='getAccountPeriodOperation'),
    url(r'ajax/createAccounPeriodOriginOp/(?P<pkUser>\d+)/', GetAccountPeriodOriginOperation.as_view(), name='getAccountPeriodOriginOperation'),   
    url(r'ajax/createOrigin/(?P<pkUser>\d+)/', CreateOrigin.as_view(), name='createOrigin'),
    url(r'ajax/getOperationBudget/(?P<pkUser>\d+)/', GetOperationBudget.as_view(), name='getOperationBudget'),
    url(r'ajax/searchRubroTw/(?P<pkUser>\d+)/', SearchRubroTw.as_view(), name='searchRubroTw'),
    url(r'ajax/createRubro/(?P<pkUser>\d+)/', CreateRubro.as_view(), name='createRubro'),
    url(r'ajax/getRubrosOrigin/(?P<pkUser>\d+)/', GetRubrosOrigin.as_view(), name='getRubrosOrigin'),
    url(r'ajax/getOperationByOperate/(?P<pkUser>\d+)/', GetOperationByOperate.as_view(), name='getOperationByOperate'),
    url(r'ajax/updateRubro/(?P<pkUser>\d+)/', UpdateRubro.as_view(), name='updateRubro'),
    url(r'ajax/getRubrosContraOperation/(?P<pkUser>\d+)/', GetRubrosContraOperation.as_view(), name='getRubrosContraOperation'),
    url(r'ajax/createOperations/(?P<pkUser>\d+)/', CreateOperations.as_view(), name='createOperations'),
    url(r'settings/deleteRubro/(?P<pkUser>\d+)/', DeleteRubro.as_view() , name='deleteRubro'),
    
    url(r'ajax/getDetailRubro/(?P<pkUser>\d+)/', GetDetailRubro.as_view(), name='getDetailRubro'),
    url(r'budget/importRubro/(?P<idBussines>\d+)/(?P<idOrigin>\d+)/', ImportRubro, name='importRubro'),
    url(r'ajax/getDetallAgreement/(?P<pkUser>\d+)/', GetDetallAgreement.as_view(), name='getDetallAgreement'),
    url(r'ajax/getRubroCreate/(?P<pkUser>\d+)/', GetRubroCreate.as_view(), name='getRubroCreate'),
    url(r'ajax/importRubrosBD/(?P<pkUser>\d+)/', ImportRubrosBD.as_view(), name='importRubrosBD'),
    url(r'ajax/getRubroOperationDetail/(?P<pkUser>\d+)/', GetRubroOperationDetail.as_view(), name='getRubroOperationDetail'),
    url(r'ajax/getInformtUpdateRubro/(?P<pkUser>\d+)/', GetInformtUpdateRubro.as_view(), name='getInformtUpdateRubro'),
    url(r'ajax/updateAgreementRubro/(?P<pkUser>\d+)/', UpdateAgreementRubro.as_view(), name='updateAgreementRubro'),
    url(r'ajax/deleteRubrosImported/(?P<pkUser>\d+)/', DeleteRubrosImported.as_view(), name='deleteRubrosImported'),
    url(r'ajax/getMovementsByOrigin/(?P<pkUser>\d+)/', GetMovementsByOrigin.as_view(), name='getMovementsByOrigin'),
    url(r'ajax/getDisponibilityByRubros/(?P<pkUser>\d+)/', GetDisponibilityByRubros.as_view(), name='getDisponibilityByRubros'),
    url(r'ajax/getUpdateOperationByOperate/(?P<pkUser>\d+)/', GetUpdateOperationByOperate.as_view(), name='getUpdateOperationByOperate'),
    url(r'ajax/UpdateOperations/(?P<pkUser>\d+)/', UpdateOperations.as_view(), name='updateOperations'),
    url(r'ajax/deleteOperations/(?P<pkUser>\d+)/', DeleteOperations.as_view(), name='deleteOperations'),
    url(r'ajax/deleteAgreementsOperations/(?P<pkUser>\d+)/',DeleteAgreementsOperations.as_view(),  name='deleteAgreementsOperations'),
    url(r'ajax/getAgreement/(?P<pkUser>\d+)/',GetAgreement.as_view(),  name='getAgreement'),
    url(r'ajax/getInforms/(?P<pkUser>\d+)/',GetInforms.as_view(),  name='getInforms'),
    url(r'ajax/getInformsDetall/(?P<pkUser>\d+)/',GetInformsDetall.as_view(),  name='getInformsDetall'),
    url(r'ajax/saveInformsDetall/(?P<pkUser>\d+)/',SaveInformsDetall.as_view(),  name='saveInformsDetall'),
    url(r'ajax/mayorizacion/(?P<pkUser>\d+)/',Mayorizacion.as_view(),  name='mayorizacion'),
    
    url(r'settings/deleteAccount/(?P<pkUser>\d+)/', DeleteAccount.as_view() , name='deleteAccount'),
    url(r'ajax/getClosedMounth/(?P<pkUser>\d+)/', GetClosedMounth.as_view(), name='getClosedMounth'),
    url(r'ajax/deactivateMonth/(?P<pkUser>\d+)/', DeactivateMonth.as_view(), name='deactivateMonth'),
    url(r'ajax/getDatePeriod/(?P<pkUser>\d+)/', GetDatePeriod.as_view(), name='getDatePeriod'),
    url(r'ajax/getPatternOrigin/(?P<pkUser>\d+)/', GetPatternOrigin.as_view(), name='getPatternOrigin'),

    



    



]