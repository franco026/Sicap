from django.conf.urls import url, include
from apps.settingsSICAP.views import *

urlpatterns = [
    
    url(r'ajax/settingsOP/(?P<pkUser>\d+)/', GetOriginSettings.as_view(), name='settingsOP'),
    url(r'ajax/settingsOP2/(?P<pkUser>\d+)/', GetOriginSettings2.as_view(), name='settingsOP2'),

    
    url(r'ajax/settingsOG/(?P<pkUser>\d+)/', CreateOriginSettings.as_view(), name='settingsOG'),
    url(r'ajax/settingsCreateOP/(?P<pkUser>\d+)/', CreateOperationSettings.as_view(), name='settingsCreateOP'),
    url(r'ajax/settingsInfDetall/(?P<pkUser>\d+)/', CreateInformDetall.as_view(), name='settingsInfDetall'),
    url(r'ajax/createInform/(?P<pkUser>\d+)/$', CreateInform.as_view(), name='createInform'), 
    
    url(r'settings/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListAccountPeriod.as_view() , name='settings'),



    url(r'settings/listInform/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListInform.as_view() , name='listInform'),
    url(r'settings/createTypeAgreement/(?P<pkUser>\d+)/', CreateTypeAgreement.as_view(), name='createTypeAgreement'), 
    url(r'settings/listTypeAgreement/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListTypeAgreement.as_view() , name='listTypeAgreement'),
    url(r'ajax/updateTypeAgreement/(?P<pkUser>\d+)/', UpdateTipeAgreement.as_view(), name='updateTypeAgreement'),
    url(r'settings/deleteAll/(?P<pkUser>\d+)/', DeleteAll.as_view() , name='deleteAll'),
    url(r'ajax/updateAccountPeriod/(?P<pkUser>\d+)/', UpdateAccountPeriod.as_view(), name='updateAccountPeriod'),
    url(r'ajax/updateInform/(?P<pkUser>\d+)/', UpdateInform.as_view(), name='updateInform'),
    url(r'settings/listOperations/(?P<pk>\d+)/(?P<pkUser>\d+)/', ListOperations.as_view() , name='listOperations'),
    url(r'ajax/updateOperation/(?P<pkUser>\d+)/', UpdateOperation.as_view(), name='updateOperation'),
    url(r'ajax/getOperationsContra/(?P<pkUser>\d+)/', GetOperationsContra.as_view(), name='getOperationsContra'),
    url(r'ajax/updateContraOperation/(?P<pkUser>\d+)/', UpdateContraOperation.as_view(), name='updateContraOperation'),
    url(r'ajax/getOriginOperation/(?P<pkUser>\d+)/', GetOriginOperation.as_view(), name='getOriginOperation'),
    url(r'ajax/getInfoOrigin/(?P<pkUser>\d+)/', GetInfoOrigin.as_view(), name='getInfoOrigin'),
    url(r'ajax/updatePattern/(?P<pkUser>\d+)/', UpdatePattern.as_view(), name='updatePattern'),

    url(r'ajax/changeWindowsOperation/(?P<pkUser>\d+)/', ChangeWindowsOperation.as_view(), name='changeWindowsOperation'),
    url(r'settings/listDiscount/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListDiscount.as_view() , name='listDiscount'),
    url(r'settings/typeDocument/(?P<pk>\d+)/(?P<pkUser>\d+)/$', typeDocumentView.as_view() , name='typeDocument'),
     url(r'settings/CCPET/(?P<pk>\d+)/(?P<pkUser>\d+)/', CCPETView.as_view() , name='CCPETView'),

    url(r'ajax/createDiscount/(?P<pkUser>\d+)/$', CreateDiscount.as_view(), name='createDiscount'),
    url(r'ajax/getListInformsDetall/(?P<pkUser>\d+)/$', GetInformsDetall.as_view(), name='getListInformsDetall'),
    url(r'ajax/addCategoryDetall/(?P<pkUser>\d+)/$', AddCategoryDetall.as_view(), name='addCategoryDetall'),
    url(r'ajax/updateCategoryDetall/(?P<pkUser>\d+)/$', UpdateCategoryDetall.as_view(), name='updateCategoryDetall'),
    url(r'ajax/deleteCategoryDetall/(?P<pkUser>\d+)/$', DeleteCategoryDetall.as_view(), name='deleteCategoryDetall'),

     url(r'ajax/getCategoryInformsDetall/(?P<pkUser>\d+)/$', GetCategoryInformsDetall.as_view(), name='getCategoryInformsDetall'),



    url(r'settings/listAccount/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListAccount.as_view() , name='listAccount'),
    url(r'ajax/createAccount/(?P<pkUser>\d+)/$', CreateAccount.as_view(), name='createAccount'),
    url(r'ajax/updateAccount/(?P<pkUser>\d+)/', UpdateAccount.as_view(), name='updateAccount'),

    url(r'settings/generateAccounting/(?P<pkUser>\d+)/', generateAccounting , name='generateAccounting'),
    url(r'ajax/getAccountSettings/(?P<pkUser>\d+)/', GetAccountSettings.as_view(), name='getAccountSettings'),
    url(r'ajax/createAccountingOpTip/(?P<pkUser>\d+)/$', CreateAccountingOpTip.as_view(), name='createAccountingOpTip'),
    url(r'ajax/getBudget/(?P<pkUser>\d+)/', GetBudget.as_view(), name='getBudget'),
    url(r'ajax/createAccountRubro/(?P<pkUser>\d+)/', CreateAccountRubro.as_view(), name='createAccountRubro'),
    url(r'ajax/getAccountsByRubros/(?P<pkUser>\d+)/', GetAccountsByRubros.as_view(), name='getAccountsByRubros'),
    url(r'ajax/searchAccount/(?P<pkUser>\d+)/', SearchAccount.as_view(), name='searchAccount'),
    url(r'ajax/getListAccount/(?P<pkUser>\d+)/', GetListAccount.as_view(), name='getListAccount'),
    url(r'ajax/getListAccountCCPET/(?P<pkUser>\d+)/', GetListAccountCCPET.as_view(), name='getListAccountCCPET'),
    
    url(r'settings/listInformBank/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListInformBank.as_view() , name='listInformBank'),
    url(r'ajax/createInformBank/(?P<pkUser>\d+)/$', CreateInformBank.as_view(), name='createInformBank'), 
    url(r'ajax/settingsInfDetailBank/(?P<pkUser>\d+)/', CreateInformDetailBank.as_view(), name='settingsInfDetailBank'),
    url(r'ajax/updateInformBank/(?P<pkUser>\d+)/', UpdateInformBank.as_view(), name='updateInformBank'),
    url(r'ajax/changeWindowsInformDetailBank/(?P<pkUser>\d+)/', ChangeWindowsInformDetailBank.as_view(), name='changeWindowsInformDetailBank'),
    url(r'ajax/importAccountsCCPETBD/(?P<pkUser>\d+)/', importAccountsCCPETBD.as_view(), name='importAccountsCCPETBD'),

    url(r'ajax/importAccountsBD/(?P<pkUser>\d+)/', ImportAccountsBD.as_view(), name='importAccountsBD'),

    url(r'ajax/searchAccountButton/(?P<pkUser>\d+)/', SearchAccountButton.as_view(), name='searchAccountButton'),

    url(r'ajax/getSearchAccountButton/(?P<pkUser>\d+)/', GetSearchAccountButton.as_view(), name='getSearchAccountButton'),
    
    url(r'ajax/deleteAccountsByRubro/(?P<pkUser>\d+)/', DeleteAccountsByRubro.as_view(), name='deleteAccountsByRubro'),
    url(r'ajax/validateAccountsByRubro/(?P<pkUser>\d+)/', ValidationAccountByRubro.as_view(), name='validateAccountsByRubro'),


    url(r'ajax/getListDocument/(?P<pkUser>\d+)/', getListDocument.as_view(), name='getListDocument'),
    url(r'ajax/getListPeriod/(?P<pkUser>\d+)/', GetListPeriod.as_view(), name='getListPeriod'),
    url(r'ajax/createTypeDocument/(?P<pkUser>\d+)/', CreateTypeDocument.as_view(), name='createTypeDocument'),
    url(r'ajax/deleteTypeDocument/(?P<pkUser>\d+)/', DeleteTypeDocument.as_view(), name='deleteTypeDocument'),
    url(r'ajax/updateTypeDocument/(?P<pkUser>\d+)/', UpdateTypeDocument.as_view(), name='updateTypeDocument'),
    

    url(r'ajax/getDiscount/(?P<pkUser>\d+)/$', GetDiscount.as_view(), name='getDiscount'),
    url(r'ajax/updateDiscount/(?P<pkUser>\d+)/$', UpdateDiscount.as_view(), name='updateDiscount'),
    url(r'ajax/deleteInformsDetall/(?P<pkUser>\d+)/$', DeleteInformsDetall.as_view(), name='deleteInformsDetall'),

    url(r'ajax/getDetailAccountObligation/(?P<pkUser>\d+)/$', GetDetailAccountObligation.as_view(), name='getDetailAccountObligation'),

    url(r'ajax/deleteCCPETImported/(?P<pkUser>\d+)/', DeleteCCPETImported.as_view(), name='deleteCCPETImported'),
    
]