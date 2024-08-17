from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404 
# from .views import confirm_deposit, confirm_withdraw


urlpatterns = [
    path('signup', views.Signup, name='signup'),
    path('Login', views.Login, name='Login'),  
    path('logout', views.logout, name='logout'),  
    path('register', views.registration_view, name='register'),
    path('signin', views.login_view, name='signin'),# Make sure the name matches your template
    path('update', views.profile_view, name='update'),
    path('update-pic/', views.update_profile_picture, name='update_profile_picture'),
    path('get_wallet_address/', views.get_wallet_address, name='get_wallet_address'),
    path('deposit_submit/', views.deposit_submit, name='deposit_submit'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('confirm_deposit/<int:deposit_id>/', views.confirm_deposit, name='confirm_deposit'),
    path('confirm_withdraw/<int:withdraw_id>/', views.confirm_withdraw, name='confirm_withdraw'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_withdrawal_password/', views.update_withdrawal_password, name='update_withdrawal_password'),
    path('check_withdraw_password/', views.check_withdraw_password, name='check_withdraw_password'),
    path('withdraw_submit/', views.withdraw_submit, name='withdraw_submit'),
    path('verify_email/',views.verify_email, name='verify_email'),
    path('send_reset_password_link/',views.send_reset_password_link, name='send_reset_password_link'),
    path('invest/', views.invest, name='invest'),
    path('check-active-investment/',views.check_active_investment, name='check_active_investment'),
    path('invest_subscription/',views.invest_subscription, name='invest_subscription'),
    path('sub_check_active_investment/',views.sub_check_active_investment, name='sub_check_active_investment'), 
    path('get-balances/',views.get_balances, name='get_balances'),
    path('update_balances/',views.update_balances, name='update_balances'),
    path('contact-support/',views.contact_support, name='contact_support')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
  
 