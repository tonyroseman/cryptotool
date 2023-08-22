from django.urls import path
from home import views
from django.contrib.auth import views as auth_views
from django.urls import include


urlpatterns = [
    #pages
    path('', views.index, name = 'index'),
    
    path('icon-feather/', views.icon_feather, name = 'icon_feather'),
    path('records/', views.records, name = 'records'),
    
    path('setting_page/', views.setting_page, name = 'setting_page'),
    path('save_settings/', views.save_settings, name = 'save_settings'),
    path('user-profile/', views.user_profile, name = 'user_profile'),
    path('get_coindata_all/', views.get_coindata_all, name = 'get_coindata_all'),
    path('send_telegram_message/', views.send_telegram_message, name = 'send_telegram_message'),
    
    path('get_coindata_user/', views.get_coindata_user, name = 'get_coindata_user'),
    path('accounts/auth-signup/', views.auth_signup, name = 'auth_signup'),
    path('accounts/auth-signin/', views.AuthSignin.as_view(), name='auth_signin'),
    path('accounts/forgot-password/', views.UserPasswordResetView.as_view(), name='forgot_password'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('accounts/logout/', views.user_logout_view, name='logout'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done" ),

    
]


