from django.conf.urls import url, include
from apps.users.views import *

urlpatterns = [

    url(r'users/index', indexWelocome, name="indexUser"),
    url(r'users/createUser', CreateUser.as_view(), name='createUser'),
    url(r'ajax/getAP', GetAccountPeriod.as_view(), name='getAcccountPeriod'),
    url(r'ajax/startApp',StartApp.as_view() , name='getStartApp'),
    url(r'ajax/getValidatePassword/(?P<pkUser>\d+)/',GetValidatePassword.as_view() , name='getValidatePassword'),
    url(r'ajax/getValidatePassword/(?P<pkUser>\d+)/',GetValidatePassword.as_view() , name='getValidatePassword'),
    url(r'admin/(?P<pkUser>\d+)/$', AccountAdmin.as_view() , name='admin'),
    url(r'deleteUsers/(?P<pkUser>\d+)/$', DeleteUsers.as_view() , name='deleteUsers'),

    url(r'getListBussines/(?P<pkUser>\d+)/$', GetListBussines.as_view() , name='getListBussines'),
    url(r'linkBussines/(?P<pkUser>\d+)/$', LinkBussines.as_view() , name='linkBussines'),

]