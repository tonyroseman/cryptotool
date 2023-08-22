from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.forms import RegistrationForm,LoginForm,UserPasswordResetForm,UserSetPasswordForm,UserPasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
import telegram 
import json



from django.contrib.auth.decorators import login_required
from .models import UserSettingsData
from .coinmodule import CryptoModule
from .notify import Notify


def auth_signup(request):
  if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
        form.save()
        
          
        return redirect('/accounts/auth-signin/')
      else:
        print("Registration failed!")
  else:
    form = RegistrationForm()
  context = {'form': form}
  return render(request, 'accounts/auth-signup.html', context)

class AuthSignin(auth_views.LoginView):
  template_name = 'accounts/auth-signin.html'
  form_class = LoginForm
  success_url = '/'

class UserPasswordResetView(auth_views.PasswordResetView):
  template_name = 'accounts/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/recover-password.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/recover-password.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm


def user_logout_view(request):
  logout(request)
  
  return redirect('/accounts/auth-signin/')


# Dashboard
def index(request):
  
  api = CryptoModule()
  coins = api.get_top_coins(limit=1000)
  
  
  context = {
      'coins': coins
  }
  return render(request, 'pages/index.html', context)
@login_required(login_url='/accounts/auth-signin')
def get_coindata_all(request):
  if request.method == "GET":
    
    api = CryptoModule()
    coins = api.get_top_coins(limit=int(request.user.limitcount))
    
    context = {
        'data': coins
    }
    return JsonResponse (context, status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)
@login_required(login_url='/accounts/auth-signin')
def get_coindata_user(request):
  
  if request.method == "GET":
    
    api = CryptoModule()
    coins = api.get_user_coins(limit=int(request.user.limitcount))
    usersettingsdata = UserSettingsData.objects.get(userid=request.user)
    # coins.append(json.loads(usersettingsdata.data.replace("'", "\"")))
    context = {
        'data': coins,
        'settings': json.loads(usersettingsdata.data.replace("'", "\"")),
        
    }
    
    return JsonResponse (context, status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)
@login_required(login_url='/accounts/auth-signin')
def send_telegram_message(request):
  
  if request.method == "GET":
    
    notify = Notify()
    symbols = request.GET['symbols'].split(',')
    coindic = {}
    for symbol in symbols:
        coindic[symbol] = 1
    api = CryptoModule()
    coins = api.get_user_coins(limit=int(request.user.limitcount))
    
    for data in coins:
       
       if coindic.get(data['symbol']) is not None:
          notify.saveNotify(data, request.user)
          
    
      
    # bot = TelegramBot()
    # bot.sendMessage("OK",request.user.telegram)
    context = {
        'data': 'OK',
        
        
    }
    return JsonResponse (context,status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)
# UI Element
@login_required(login_url='/accounts/auth-signin')
def bc_typography(request):
    return render(request, 'pages/bc_typography.html')

@login_required(login_url='/accounts/auth-signin')
def icon_feather(request):
    return render(request, 'pages/icon-feather.html')

# Table
@login_required(login_url='/accounts/auth-signin')
def tbl_bootstrap(request):
   
    return render(request, 'pages/tbl_allcoin.html')

# Chart & Maps
@login_required(login_url='/accounts/auth-signin')
def chart_apex(request):
    return render(request, 'pages/chart-apex.html')

@login_required(login_url='/accounts/auth-signin')
def map_google(request):
    return render(request, 'pages/map-google.html')

@login_required(login_url='/accounts/auth-signin')
def save_settings(request):
    msg = "Saved your settings."
    if request.method == 'POST':
      settingsData = {}
      if len(request.POST.keys()) > 1:
        for key in request.POST.keys():
          if key != 'csrfmiddlewaretoken':
              if key != 'tlg' and key[0:1] != 't' :
                if request.POST['t' + key] != '':
                  settingsData[key] = request.POST[key]
                  settingsData['t' + key] = request.POST['t' + key]
              elif key == 'tlg':
                  settingsData[key] = request.POST[key]
        usersettingsdata = None
        try:
            usersettingsdata = UserSettingsData.objects.get(userid=request.user)
            usersettingsdata.data = str(settingsData)
            usersettingsdata.save() 
            
        except UserSettingsData.DoesNotExist:
            usersettingsdata = UserSettingsData()
            usersettingsdata.userid = request.user
            usersettingsdata.data = str(settingsData)
            usersettingsdata.save()
            
      

      # print(request.POST.get('m3'))
      
      if request.method == 'POST':
        msg = "Saved your settings."
    else:
        msg = "Invalid access."
    context = {  
        'data': json.loads(usersettingsdata.data.replace("'", "\"")),
        'msg' : msg
    }
    return render(request, 'pages/setting.html', context)
# Pages

@login_required(login_url='/accounts/auth-signin')
def user_profile(request):
    return render(request, 'pages/user-profile.html')
    
@login_required(login_url='/accounts/auth-signin')
def setting_page(request):
    msg = ''
    data = None
    try:
      usersettingsdata = UserSettingsData.objects.get(userid=request.user)
      data = json.loads(usersettingsdata.data.replace("'", "\""))
    except UserSettingsData.DoesNotExist:
      msg = 'Settings does not exist'
    context = {        
        'data': data,
        'msg' : msg
    }
    
    return render(request, 'pages/setting.html', context)
@login_required(login_url='/accounts/auth-signin')
def records(request):
    
    return render(request, 'pages/records.html')
