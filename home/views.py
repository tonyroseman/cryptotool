from django.shortcuts import render, redirect
from home.forms import RegistrationForm,LoginForm,UserPasswordResetForm,UserSetPasswordForm,UserPasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# from verify_email.email_handler import send_verification_email

from django.contrib.auth.decorators import login_required
from coinmarketcapapi import CoinMarketCapAPI


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
    cmc = CoinMarketCapAPI()
  
    rep = cmc.cryptocurrency_info(symbol='BTC') # See methods below

    print(rep.data)                 # Whole repsonse payload
    print(rep.data["BTC"]["logo"])  # Some data in response
    print(rep.credit_count)         # API credits
    print(rep.total_elapsed)        # Request time in ms
    return render(request, 'pages/index.html')

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
    return render(request, 'pages/tbl_bootstrap.html')

# Chart & Maps
@login_required(login_url='/accounts/auth-signin')
def chart_apex(request):
    return render(request, 'pages/chart-apex.html')

@login_required(login_url='/accounts/auth-signin')
def map_google(request):
    return render(request, 'pages/map-google.html')

# Pages

@login_required(login_url='/accounts/auth-signin')
def user_profile(request):
    return render(request, 'pages/user-profile.html')
    
@login_required(login_url='/accounts/auth-signin')
def sample_page(request):
    return render(request, 'pages/sample-page.html')
