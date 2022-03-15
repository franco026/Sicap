from copyreg import constructor
from django.shortcuts import render
from apps.users.models import *
from apps.budgets.models import *
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from apps.users.forms import *
from apps.budgets.forms import *
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse,HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

# Create your views here.
class CreateUser(CreateView):

    model = User
    form_class = UserForm
    template_name = 'users/createUser.html'

    def get_success_url(self,**kwargs):
        return reverse_lazy("admin",  kwargs={'pkUser': self.request.user.id})

class LoginUser(View):

    def  get(self, request, *args, **kwargs):
        username = request.GET.get('usernameInput')
        password = request.GET.get('passwordInput')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)

            if request.user.typeUser != 'admin':
                bussines =  BussinesUsers.objects.filter(user_id=request.user.id).values('bussines__name','bussines__id')
                Periods =  AccountPeriod.objects.filter(bussines_id=list(bussines)[0]['bussines__id']).values('name','id')
                data = {
                    'formAC': "GG",
                    "usuario": request.user.typeUser,
                    "id": request.user.id,
                    "listB": list(bussines),
                    "listP": list(Periods)
                }
            else:
                data = {
                    'formAC': "GG",
                    "usuario": request.user.typeUser,
                    "id": request.user.id
                }

            return JsonResponse(data)


class GetAccountPeriod(View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    
    def  get(self, request, *args, **kwargs):

        bussines =  Bussines.objects.get(name=request.GET.get('nameBussines'))
        accountPeriod =  AccountPeriod.objects.all().filter(bussines_id=bussines.id).values('name')
        return JsonResponse({"AC": list(accountPeriod)})

def success(request):

    context = {}
    context['user'] = request.user
    return render(request, "users/success.html", context)

def userLogout(request):

	logout(request)
	return HttpResponseRedirect(reverse('userLogin'))


def indexWelocome(request):
    return render(request, 'base/baseSicap.html')


def loginS(request):
    
    form = ByBussinesForms()
    ACform = AccountPeriodForm()
    context = {'form': form, 'ACform': ACform }
    return render(request, 'users/login.html', context)


class StartApp(View):

    def  get(self, request, *args, **kwargs):

        bussines = Bussines.objects.get(name=request.GET.get('nameBussines'))
        account = AccountPeriod.objects.get(bussines_id=bussines.id,name=request.GET.get('nameAC'))
        nameAC=request.GET.get('nameAC')
        request.session['nameBussines'] = bussines.name
        request.session['nitBussines'] = bussines.nit
        request.session['accountPeriodBussines'] = account.name
        data = {
            'idBussines': bussines.id,
            'idAC': account.id,
            'nameBussines': request.GET.get('nameBussines'),
            'nameAC': nameAC,
            'patron': bussines.rubroPattern,
            'userID': request.user.id,
            'patronAccount': bussines.accountPattern
        }
        return JsonResponse(data)

class GetValidatePassword(View):

    def  get(self, request, *args, **kwargs):

        user = User.objects.get(id=request.GET.get('user'))
        if check_password(request.GET.get('password'), user.password):
            return JsonResponse({"EQUALS": "TRUE"})
        else:
            return JsonResponse({"EQUALS": "FALSE"})


class AccountAdmin(ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = User
    queryset = model.objects.order_by('id')
    template_name = 'users/listUsers.html'

    def get_context_data(self):
        context = super(AccountAdmin, self).get_context_data()
        context['UserForm'] = UserForm
        return context  

    def get_queryset(self):
        queryset = super(AccountAdmin, self).get_queryset()
        return User.objects.filter(~Q(id = self.kwargs['pkUser']))

class DeleteUsers(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        userDelete = User.objects.get(id=request.GET.get('userId'))
        userDelete.delete()
        return JsonResponse({'DELETE':True})


class GetListBussines(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        listBussines = Bussines.objects.filter().values('id','name')

        linkBussines = BussinesUsers.objects.filter(user_id = request.GET.get('userID')).values('bussines_id')


        return JsonResponse({'LB':list(listBussines),'SL':list(linkBussines)})


class LinkBussines(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        linkBussinesExist = BussinesUsers.objects.filter(user_id = request.GET.get('userID')).exists()

        if linkBussinesExist == True:

            linkBussines = BussinesUsers.objects.get(user_id = request.GET.get('userID'))
            linkBussines.bussines_id = request.GET.get('businessID')
            linkBussines.user_id = request.GET.get('userID')
            linkBussines.save()
        else:
            linkBussines = BussinesUsers.objects.create(
                user_id = request.GET.get('userID'),
                bussines_id = request.GET.get('businessID')
            )

        return JsonResponse({'SAVE':True})
