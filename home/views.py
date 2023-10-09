from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.forms import RegistrationForm,LoginForm,UserPasswordResetForm,UserSetPasswordForm,UserPasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import views as auth_views
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import logout, login

import telegram 
import json
import time
import datetime



from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import UserSettingsData
from .models import UserAdvancedSettingsData
from .models import SystemSettingsData
from .models import CustomUser
from .coinmodule import CryptoModule
from .settingsModule import SettingsModule
from .models import UserNotifyData
from .models import ErrorLog
from .models import TelegramList

def is_user_active(user):
    return user.is_active
def auth_signup(request):
  if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
        
        user = form.save(commit=False)
        user.is_active = True
        user.save()  
        # current_site = get_current_site(request)
        # mail_subject = 'Activate your blog account.'
        # message = render_to_string('pages/acc_active_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token':account_activation_token.make_token(user),
        # })
        # to_email = form.cleaned_data.get('email')
        
        # email = EmailMessage(
        #             mail_subject, message, to=[to_email]
        # )
        # email.send()
        
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
  def form_valid(self, form):
        user = form.get_user()
        user.is_login = 1
        user.save()
        return super().form_valid(form)
  

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

  
  userdata = CustomUser.objects.get(id=request.user.id)
  userdata.is_login = 0
  userdata.save()
  logout(request)
 
  return redirect('/accounts/auth-signin/')


# Dashboard
def index(request):
  if request.user.is_authenticated:
    if( request.user.is_superuser):
       return redirect('/admin')
    request.user.limitcount = int(request.user.limitcount)
    api = CryptoModule()
    coins = api.get_top_coins(request.user, limit=int(request.user.limitcount))
  
  
    context = {
        'coins': coins
    }
    return render(request, 'pages/index.html', context)
  else:
    return redirect('auth_signin')
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def get_coindata_all(request):
  if request.method == "GET":
    
    api = CryptoModule()
    coins = api.get_top_coins(request.user, limit=int(request.user.limitcount))
    
    context = {
        'data': coins
    }
    return JsonResponse (context, status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def get_coindata_user(request):
  
  if request.method == "GET":
    advancedsettingsdata = UserAdvancedSettingsData.objects.get(userid=request.user)
    coinssetings = ""
    data = json.loads(advancedsettingsdata.data.replace("'", "\""))
    if 'coins' in data[0]:
       coinssetings = data[0]['coins']
    sm = SettingsModule(settingdata=data)
    api = CryptoModule()
    coins = api.get_user_coins(request.user, sm,limit=int(request.user.limitcount))
    coins = sm.getAllMatchedCoins(coins, coinssetings)
    usersettingsdata = UserSettingsData.objects.filter(userid=request.user)
    settings = []
    if(len(usersettingsdata) > 0):
      settings = json.loads(usersettingsdata[0].data.replace("'", "\""))
    # coins.append(json.loads(usersettingsdata.data.replace("'", "\"")))
    if 'coins' in settings:
        setcoins = settings['coins'].split(",")
        flag = True
        for setcoin in setcoins:
            if setcoin[0:1] != '-':
              flag = False
              break
        if flag is True:
           settings['coins'] = ''
             
    context = {
        'data': coins,
        'settings': settings,
        
    }
    
    return JsonResponse (context, status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def get_coindata_user_count(request):
  
  if request.method == "GET":
    advancedsettingsdata = UserAdvancedSettingsData.objects.get(userid=request.user)
      
    data = json.loads(advancedsettingsdata.data.replace("'", "\""))
    sm = SettingsModule(settingdata=data)
    api = CryptoModule()
    coins = api.get_user_coins(request.user, sm,limit=int(request.user.limitcount))
    count = sm.getAllMatchedCoinsCount(coins)
    
             
    context = {
        'count': count,
        
        
    }
    
    return JsonResponse (context, status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)
@login_required(login_url='admin/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def get_notifydata_user(request):
  
  if request.method == "GET":
    
    
    usernotifydata = UserNotifyData.objects.filter(userid=int(request.GET['user_id']))
    datas = []
    if(len(usernotifydata) > 0):
      no = 1
      for notidata in usernotifydata:
          
          jsondata = json.loads(notidata.data.replace("'", "\""))
          now_timestamp = time.time()
          offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
          localdatetime = notidata.created_on + offset
          jsondata['time'] = localdatetime.strftime("%Y-%m-%d %H:%M:%S")
          jsondata['no'] = no
          datas.append(jsondata)
          no+=1
    # coins.append(json.loads(usersettingsdata.data.replace("'", "\"")))
    context = {
        'data': datas,
        
        
    }
    
    return JsonResponse (context, status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)
@login_required(login_url='/accounts/auth-signin')
def get_users(request):
  
  if request.method == "GET":
    dbusers = None
    if(request.GET['type'] == 'Console'):
       dbusers = CustomUser.objects.filter(is_superuser = True)
    elif (request.GET['type'] == 'Website'):
        dbusers = CustomUser.objects.filter(is_superuser = False)
    else:
      if(request.user.is_superuser):
        dbusers = CustomUser.objects.all()
      else:
        dbusers = CustomUser.objects.filter(is_staff = 0) 
    users = []
    i = 0
    
    for user in dbusers:
      obj_user = {}
      obj_user['no'] = (i+1)
      obj_user['name'] = user.username
      obj_user['id'] = user.id
      obj_user['type'] = user.is_superuser
      obj_user['settings'] = user.id
      obj_user['noti'] = user.id
      users.append(obj_user)
      i=i+1
    
    # coins.append(json.loads(usersettingsdata.data.replace("'", "\"")))
    context = {
        'data': users,
        
        
    }
    
    return JsonResponse (context, status = 200)
  # some error occured
  return JsonResponse ({"error": ""}, status = 400)


@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
@login_required(login_url='/accounts/auth-signin')
def save_settings(request):
    alertMsg = "Saved your settings."
    if request.method == 'POST':
      settingsData = {}
      
      if len(request.POST.keys()) > 1:
        for key in request.POST.keys():
          if key != 'csrfmiddlewaretoken':
              if key != 'tlg' and key != 'coins' and key[0:1] != 't' :
                if request.POST['t' + key] != '':
                  settingsData[key] = request.POST[key]
                  settingsData['t' + key] = request.POST['t' + key]
              elif key == 'tlg' or key == 'coins':
                  settingsData[key] = request.POST[key].strip()
        if not 'tlg' in request.POST.keys():
           settingsData['tlg'] = '0'
        if settingsData['tlg'] == '1':
           
           alertMsg = "1"
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
      
    
    
    context = {  
        'userid': request.user.id,
        'data': json.loads(usersettingsdata.data.replace("'", "\"")),
        'tlgactive':request.user.tlgactive,
        'alertMsg' : alertMsg
    }
    return render(request, 'pages/setting.html', context)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def save_profile(request):
    alertMsg = "Saved your settings."
    if request.method == 'POST':
          userdata = CustomUser.objects.get(id=request.user.id)
          userdata.username = request.POST.get('username')
          userdata.email = request.POST.get('email')
          userdata.phone = request.POST.get('phone')
          userdata.telegram = request.POST.get('telegram')
          try:
            telegramlist = TelegramList.objects.get(data=userdata.telegram)            
            userdata.tlgactive = 1
          except TelegramList.DoesNotExist:
            userdata.tlgactive = 0
          if str(userdata.telegram).strip() == "": 
            userdata.tlgactive = 0
            try:
              
              usersettingsdata = UserSettingsData.objects.get(userid=userdata.id)
              data = json.loads(usersettingsdata.data.replace("'", "\""))
              if 'tlg' in data.keys():
                 data['tlg'] = '0'
              usersettingsdata.data = str(data)
              usersettingsdata.save()
              UserNotifyData.objects.filter(userid=userdata.id).delete()
              adsettings = UserAdvancedSettingsData.objects.get(userid=userdata.id)
              adsettings.istlg = 0
              adsettings.save()
            except UserSettingsData.DoesNotExist:            
              msg = 'Settings does not exist'
            except UserAdvancedSettingsData.DoesNotExist:
              msg = 'Settings does not exist'
          userdata.save()
          
             
             
    return redirect('/user-profile')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
@login_required(login_url='/accounts/auth-signin')
def disable_telegram(request):
    
    
    usersettingsdata = UserSettingsData.objects.get(userid=request.user)
    setdata = json.loads(usersettingsdata.data.replace("'", "\""))
    setdata['tlg']  = '0'
    usersettingsdata.data = str(setdata)
    usersettingsdata.save() 
    
    context = {  
        'data': setdata,
        'tlgactive':request.user.tlgactive,
        'alertMsg' : ""
    }
    return render(request, 'pages/setting.html', context)
# Pages
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def advanced_settings(request):
  tlgurl = ''
  try:
    syssettings = SystemSettingsData.objects.all()
    
    if(len(syssettings) > 0):
        data = json.loads(syssettings[0].data.replace("'", "\""))
        
        if 'tlgurl' in data:
          tlgurl = data['tlgurl']
    usersettingsdata = UserSettingsData.objects.get(userid=request.user)
    data = json.loads(usersettingsdata.data.replace("'", "\""))
    
  except UserSettingsData.DoesNotExist:
    msg = 'Settings does not exist'
  context = {  
        'userid': request.user.id,
        'tlgactive':request.user.tlgactive,
        'tlgurl':tlgurl,
    }
  return render(request, 'pages/advanced_settings.html', context)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def user_profile(request):
    return render(request, 'pages/user-profile.html')
    
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def setting_page(request):
    msg = ''
    data = None
    tlgurl = ''
    try:
      syssettings = SystemSettingsData.objects.all()
      
      if(len(syssettings) > 0):
         data = json.loads(syssettings[0].data.replace("'", "\""))
         
         if 'tlgurl' in data:
            tlgurl = data['tlgurl']
      usersettingsdata = UserSettingsData.objects.get(userid=request.user)
      data = json.loads(usersettingsdata.data.replace("'", "\""))
      
    except UserSettingsData.DoesNotExist:
      msg = 'Settings does not exist'
    context = {        
        'userid': request.user.id,
        'data': data,
        'msg' : msg,
        'tlgactive':request.user.tlgactive,
        'tlgurl':tlgurl
    }
    
    return render(request, 'pages/setting.html', context)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def user_settings(request, userid):
    msg = ''
    data = None
    coins=""
    try:
      user = CustomUser.objects.get(id=userid)
      usersettingsdata = UserSettingsData.objects.get(userid=userid)
      data = json.loads(usersettingsdata.data.replace("'", "\""))
      useradsettingsdata = UserAdvancedSettingsData.objects.get(userid=userid)
      addata = json.loads(useradsettingsdata.data.replace("'", "\""))
      sm = SettingsModule(settingdata=addata)
      
      expression = sm.getExpression()
      expression = " ".join(expression.split())
      if "coins" in data[0]:
        coins = data[0]['coins']
    except UserSettingsData.DoesNotExist:
      msg = 'Settings does not exist'
    context = {        
        'data': data,
        'coins':coins,
        'msg' : msg,
        'username': user.username,
        'isadtlg':useradsettingsdata.istlg,
        'expression':expression,

    }
    
    return render(request, 'pages/usersettings.html', context)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def user_advanced_settings(request, userid):
    
    treedata = None
    expression = None
    istlg = 0
    coins = ""
    try:
      user = CustomUser.objects.get(id=userid)
      advancedsettingsdata = UserAdvancedSettingsData.objects.get(userid=userid)
      
      data = json.loads(advancedsettingsdata.data.replace("'", "\""))
      sm = SettingsModule(settingdata=data)
      treedata = sm.getTreeData()
      expression = sm.getExpression()
      expression = " ".join(expression.split())
      istlg = advancedsettingsdata.istlg
      if "coins" in data[0]:
         coins = data[0]['coins']
    except UserAdvancedSettingsData.DoesNotExist:
      try:
          
          sm = SettingsModule()
          data = sm.getRawData()
          advancedsettingsdata = UserAdvancedSettingsData()
          advancedsettingsdata.data = str(data)
          advancedsettingsdata.userid = user
          advancedsettingsdata.save()
          treedata = sm.getTreeData()
          expression = sm.getExpression()
          expression = " ".join(expression.split())
      except UserSettingsData.DoesNotExist:
          data = []
    context = {        
        'data': treedata,
        'coins':coins,
        'istlg': str(istlg),
        'expression':expression
    }
    
    return JsonResponse (context, status = 200)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def set_ad_tlg_settings(request):
    
    value = request.GET.get('value')
    msg = "OK"
    try:
      
      advancedsettingsdata = UserAdvancedSettingsData.objects.get(userid=request.user)
      advancedsettingsdata.istlg = int(value)
      advancedsettingsdata.save()
      
    except UserAdvancedSettingsData.DoesNotExist:
      msg = "Error"
    
    context = {        
        'msg': msg,
    }
    
    return JsonResponse (context, status = 200)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def save_ad_coins(request):
    
    value = request.GET.get('value')
    msg = "OK"
    try:
      
      advancedsettingsdata = UserAdvancedSettingsData.objects.get(userid=request.user)
      data = json.loads(advancedsettingsdata.data.replace("'", "\""))
      settingsdata = data[0]
      data[0]['coins'] = value
      advancedsettingsdata.data = str(data)
      advancedsettingsdata.save()
      
    except UserAdvancedSettingsData.DoesNotExist:
      msg = "Error"
    
    context = {        
        'msg': msg,
    }
    
    return JsonResponse (context, status = 200)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def action_advanced_settings(request):
    
    action = request.GET.get('action')
    print(request.GET)
    msg = "OK"
    try:
      
      advancedsettingsdata = UserAdvancedSettingsData.objects.get(userid=request.user)
      
      data = json.loads(advancedsettingsdata.data.replace("'", "\""))
      sm = SettingsModule(settingdata=data)
      if action == '1' : # change operator
        result = sm.changeGroupOperator(request.GET.get('nodeId'),request.GET.get('op'))
        if result == 1:
          rawdata = sm.getRawData()
          advancedsettingsdata.data = str(rawdata)
          advancedsettingsdata.save()
          msg = "Changed group operator successfully."
        else:
          msg = "Change group operator error" 
      if action == '2' : # add group
        result = sm.addGroup(request.GET.get('nodeId'),request.GET.get('op'))
        if result == 1:
          rawdata = sm.getRawData()
          advancedsettingsdata.data = str(rawdata)
          advancedsettingsdata.save()
          msg = "Add group successfully."
        else:
          msg = "Add group error" 
      if action == '3' : # delete group
        result = sm.deleteGroup(request.GET.get('nodeId'))
        if result == 1:
          rawdata = sm.getRawData()
          advancedsettingsdata.data = str(rawdata)
          advancedsettingsdata.save()
          msg = "Delete group successfully."
        else:
          msg = "Delete group error"
      if action == '4' : # add condition
        result = sm.addCondition(request.GET.get('nodeId'),request.GET.get('cond_type'),request.GET.get('glt'),request.GET.get('cvalue'))
        if result == 1:
          rawdata = sm.getRawData()
          advancedsettingsdata.data = str(rawdata)
          advancedsettingsdata.save()
          msg = "Add Condition successfully."
        else:
          msg = "Add Condition error" 
      if action == '5' : # change condition
        result = sm.changeCondition(request.GET.get('nodeId'),request.GET.get('cond_type'),request.GET.get('glt'),request.GET.get('cvalue'))
        if result == 1:
          rawdata = sm.getRawData()
          advancedsettingsdata.data = str(rawdata)
          advancedsettingsdata.save()
          msg = "Change Condition successfully."
        else:
          msg = "Change Condition error"
      if action == '6' : # delete condition
        result = sm.deleteCondition(request.GET.get('nodeId'))
        if result == 1:
          rawdata = sm.getRawData()
          advancedsettingsdata.data = str(rawdata)
          advancedsettingsdata.save()
          msg = "Delete Condition successfully."
        else:
          msg = "Delete Condition error" 
      if action == '7' : # delete condition
        result = sm.makeConditionToGroup(request.GET.get('nodeId'),request.GET.get('op'))
        if result == 1:
          rawdata = sm.getRawData()
          advancedsettingsdata.data = str(rawdata)
          advancedsettingsdata.save()
          msg = "Make Condition to Group successfully."
        else:
          msg = "Make Condition to Group error" 
    except UserAdvancedSettingsData.DoesNotExist:
      msg = "Error"
    
    context = {        
        'msg': msg,
    }
    
    return JsonResponse (context, status = 200)
@login_required(login_url='/accounts/auth-signin')
def admin_usernotify(request, userid):
    
    data = []
    try:
      user = CustomUser.objects.get(id=userid)
      usersettingsdata = UserSettingsData.objects.get(userid=userid)
      data = json.loads(usersettingsdata.data.replace("'", "\""))
    except UserSettingsData.DoesNotExist:
      msg = 'Settings does not exist'
    context = {        
        'data': data,
        'username': user.username,
        'user_id':userid
        
    }
    
    return render(request, 'pages/admin_usernotify.html', context)
@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def usernotify(request, userid):
    
    data = []
    try:
      user = CustomUser.objects.get(id=userid)
      usersettingsdata = UserSettingsData.objects.get(userid=userid)
      data = json.loads(usersettingsdata.data.replace("'", "\""))
    except UserSettingsData.DoesNotExist:
      msg = 'Settings does not exist'
    context = {        
        'data': data,
        'username': user.username,
        'user_id':userid
        
    }
    
    return render(request, 'pages/usernotify.html', context)
@login_required(login_url='admin/accounts/auth-signin')
def user_console(request):
    
    
    context = {        
        'type': "Console",

        
    }
    
    return render(request, 'admin/user.html', context)
@login_required(login_url='admin/accounts/auth-signin')
def user_website(request):
    
    
    context = {        
        'type': "Website",

        
    }
    
    return render(request, 'admin/user.html', context)
@login_required(login_url='admin/accounts/auth-signin')
def system_setting(request):
    systemsettingsdatas = SystemSettingsData.objects.all()
    data = None
    if(len(systemsettingsdatas) > 0):
        
        systemsettingsdata = systemsettingsdatas[0]
        data = json.loads(systemsettingsdata.data.replace("'", "\"")),
       
    
    context = {        
        'msg': "",
        'data':data[0],

        
    }
    
    return render(request, 'admin/systemsetting.html', context)

@login_required(login_url='admin/accounts/auth-signin')
def save_system_settings(request):
    msg = "Saved your settings."
    if request.method == 'POST':
      settingsData = {}
      if len(request.POST.keys()) > 1:
        for key in request.POST.keys():
          if key != 'csrfmiddlewaretoken':
              
            if request.POST[key] != '':
              settingsData[key] = request.POST[key]
              
              
        
        systemsettingsdatas = SystemSettingsData.objects.all()
        if(len(systemsettingsdatas) > 0):
            systemsettingsdata = systemsettingsdatas[0]
            systemsettingsdata.data = str(settingsData)
            systemsettingsdata.save() 
        else:
           
            systemsettingsdata = SystemSettingsData()
            
            systemsettingsdata.data = str(settingsData)
            systemsettingsdata.save()
            
      

      # print(request.POST.get('m3'))
      
    
    
    context = {  
        'data': json.loads(systemsettingsdata.data.replace("'", "\"")),
        
        'msg' : msg
    }
    return render(request, 'admin/systemsetting.html', context)

@login_required(login_url='/accounts/auth-signin')
@user_passes_test(is_user_active, login_url='/accounts/auth-signin')
def records(request):
    
    return render(request, 'pages/records.html')
def aboutus(request):
    context = {  
        'userid': request.user.id,
    }
    return render(request, 'pages/aboutus.html', context)
def abouttlgnoti(request):
    
    return render(request, 'pages/abouttlgnoti.html')
@login_required(login_url='admin/accounts/auth-signin')
def active_users(request):
  # Retrieve active session keys
  
  return render(request, 'admin/usermonitor.html')
@login_required(login_url='admin/accounts/auth-signin')
def error_log(request):
  # Retrieve active session keys
  
  return render(request, 'admin/error_log.html')
@login_required(login_url='admin/accounts/auth-signin')
def get_active_users(request):
  # sessions = Session.objects.filter(expire_date__gt=timezone.now())
  # user_id_list = []
  # # build list of user ids from query
  # for session in sessions:
  #     data = session.get_decoded()
  #     # if the user is authenticated
  #     if data.get('_auth_user_id'):
  #         user_id_list.append(data.get('_auth_user_id'))

  # # gather the logged in people from the list of pks
  # logged_in_users = CustomUser.objects.filter(id__in=user_id_list)
  # list_of_logged_in_users = [{user.id: user.username} for user in logged_in_users]

  # # Query all logged in staff users based on id list
  # all_staff_users = CustomUser.objects.filter(is_active=True, is_superuser=False)
  # logged_out_users = list()
  # # for some reason exclude() would not work correctly, so I did this the long way.
  # for user in all_staff_users:
  #     if user not in logged_in_users:
  #         logged_out_users.append(user)
  # list_of_logged_out_users = [{user.id: user.username} for user in logged_out_users]

  # # return the ajax response
  # data = {
  #     'logged_in_users': list_of_logged_in_users,
  #     'logged_out_users': list_of_logged_out_users,
  # }
  # print(data)
  

  active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Extract user IDs from active session keys
  user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions]

    # Retrieve user data for active users based on user IDs
  active_users = CustomUser.objects.filter(id__in=user_ids)

    # Pass the active users to the template
  data = []
  i = 0
  
  for user in active_users:
     
      if user.is_active and user.is_login:
        
        userdata = {}
        userdata['no'] = (i+1)
        userdata['username'] = user.username
        userdata['type'] = user.is_staff
        userdata['id'] = user.id
        userdata['active'] = 1
        usersettings = UserSettingsData.objects.filter(userid=user.id)
        if(len(usersettings)>0):
          sdata = json.loads(usersettings[0].data.replace("'", "\""))        
          userdata['istlg'] = int(sdata['tlg'])
        else:
          userdata['istlg'] = 0
        data.append(userdata)
        i+=1
  context = {'data': data}
  return JsonResponse (context, status = 200)
@login_required(login_url='admin/accounts/auth-signin')
def get_error_log(request):
  logs = ErrorLog.objects.all()
  data = []
  i = 0
  
  for log in logs:
     
    
    logdata = {}
    logdata['no'] = (i+1)
    logdata['code'] = log.code
    logdata['type'] = log.type
    logdata['data'] = log.data
    logdata['created_on'] = log.created_on
    data.append(logdata)
    i+=1
  context = {'data': data}
  return JsonResponse (context, status = 200)

@login_required(login_url='admin/accounts/auth-signin')
def set_deactive_user(request):
  user_to_logout = CustomUser.objects.get(id=request.GET.get('userid'))
  user_to_logout.is_active = False
  user_to_logout.is_login = 0
  user_to_logout.save()

  active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Extract user IDs from active session keys
  user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions]

    # Retrieve user data for active users based on user IDs
  active_users = CustomUser.objects.filter(id__in=user_ids)

    # Pass the active users to the template
  data = []
  i = 0
  
  for user in active_users:
     
      if user.is_active and user.is_login:
        userdata = {}
        userdata['no'] = (i+1)
        userdata['username'] = user.username
        userdata['type'] = user.is_staff
        userdata['id'] = user.id
        userdata['active'] = 1
        data.append(userdata)
        i+=1
  context = {'data': data}
  return JsonResponse (context, status = 200)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/accounts/auth-signin/')
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')