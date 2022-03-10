from django.conf.urls import url, include
from apps.users.views import *

urlpatterns = [

    url(r'users/index', indexWelocome, name="indexUser"),
    url(r'users/createUser', CreateUser.as_view(), name='createUser'),
    url(r'ajax/getAP', GetAccountPeriod.as_view(), name='getAcccountPeriod'),
    url(r'ajax/startApp',StartApp.as_view() , name='getStartApp'),
    url(r'ajax/getValidatePassword/(?P<pkUser>\d+)/',GetValidatePassword.as_view() , name='getValidatePassword'),

]