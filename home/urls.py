from django.urls import path
from home import views
from django.contrib.auth import views as auth_views
from django.urls import include


urlpatterns = [
    #pages
    path('', views.index, name = 'index'),
    
    path('icon-feather/', views.icon_feather, name = 'icon_feather'),
    path('records/', views.records, name = 'records'),
    path('aboutus/', views.aboutus, name = 'aboutus'),
    path('abouttlgnoti/', views.abouttlgnoti, name = 'abouttlgnoti'),
    
    path('admin/home/customuser/', views.user_website, name = 'user_website'),
    path('admin/users/activeusers/', views.active_users, name = 'active_users'),
    path('admin/error_log/', views.error_log, name = 'error_log'),
    path('get_active_users/', views.get_active_users, name = 'get_active_users'),
    path('get_error_log/', views.get_error_log, name = 'get_error_log'),
    path('set_deactive_user/', views.set_deactive_user, name = 'set_deactive_user'),
    path('setting_page/', views.setting_page, name = 'setting_page'),
    path('admin/users/console/', views.user_console, name = 'user_console'),
    path('admin/users/website/', views.user_website, name = 'user_website'),
    path('admin/system_setting', views.system_setting, name = 'system_setting'),
    path('save_settings/', views.save_settings, name = 'save_settings'),
    path('save_profile/', views.save_profile, name = 'save_profile'),
    path('save_system_settings/', views.save_system_settings, name = 'save_system_settings'),
    path('disable_telegram/', views.disable_telegram, name = 'disable_telegram'),
    path('user-profile/', views.user_profile, name = 'user_profile'),
    path('get_coindata_all/', views.get_coindata_all, name = 'get_coindata_all'),
    path('get_users/', views.get_users, name = 'get_users'),
    
    
    path('get_coindata_user/', views.get_coindata_user, name = 'get_coindata_user'),
    path('get_notifydata_user/', views.get_notifydata_user, name = 'get_notifydata_user'),
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
    path('usersettings/<int:userid>/', views.user_settings, name='user_settings'),
    path('admin_usernotify/<int:userid>/', views.admin_usernotify, name='admin_usernotify'),
    path('usernotify/<int:userid>/', views.usernotify, name='usernotify'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    
]


    

    
