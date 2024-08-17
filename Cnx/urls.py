from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import handler404 

urlpatterns = [
    path('',views.home, name='home'),
    path('index', views.index, name='index'),
    path('indices',views.indices, name='indices'),
    path('mt5',views.mt5, name='mt5'),
    path('crypto_investment',views.crypto_investment, name='crypto_investment'),
    path('buy_crypto',views.buy_crypto, name='buy_crypto'),
    path('commodities',views.commodities, name='commodities'),
    path('forex',views.forex, name='forex'), 
    path('forex_investment',views.forex_investment, name='forex_investment'),
    path('Contacts',views.Contacts, name='Contacts'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('crypto_exchange',views.crypto_exchange, name='crypto_exchange'),
    path('Profile',views.Profile, name='Profile'),
    path('Crypto_plan',views.Crypto_plan, name='Crypto_plan'),
    path('subscription_plan',views.subscription_plan, name='subscription_plan'), 
    path('wallet',views.wallet, name='wallet'),  
    path('settings',views.settings, name='settings'), 
    path('contact_support',views.contact_support, name='contact_support'), 
    path('deposite',views.deposite, name='deposite'),
    path('withdraw_page',views.withdraw_page, name='withdraw_page'), 
    
        
]


