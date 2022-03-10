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

# Create your views here.
class CreateUser(CreateView):

    model = User
    form_class = UserForm
    template_name = 'users/createUser.html'
    success_url = reverse_lazy('index')

class LoginUser(View):

    def  get(self, request, *args, **kwargs):
        username = request.GET.get('usernameInput')
        password = request.GET.get('passwordInput')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)

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
    context = {'form': form }
    return render(request, 'users/login.html', context)


class StartApp(View):

    def  get(self, request, *args, **kwargs):

        bussines = Bussines.objects.get(name=request.GET.get('nameBussines'))
        account = AccountPeriod.objects.get(bussines_id=bussines.id,name=request.GET.get('nameAC')[:-1])
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
            print("coinciden")
            return JsonResponse({"EQUALS": "TRUE"})
        else:
            return JsonResponse({"EQUALS": "FALSE"})

