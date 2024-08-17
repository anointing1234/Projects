from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Balance
from accounts.models import InvestmentPlan,SubscriptionPlan,User_Investment,DepositTransaction, WithdrawTransaction,User_subscription_investment
from django.db.models import Sum

def home(request):
    return render(request, 'home/index.html')

def indices(request):
    return render(request, 'home/indices.html')

def index(request):
    return render(request, 'home/index.html')

def mt5(request):
    return render(request, 'home/mt5.html')

def crypto_investment(request):
    return render(request, 'home/Crypto_investment.html')

def buy_crypto(request):
    return render(request, 'home/buy_crypto.html')

def commodities(request):
    return render(request, 'home/commodities.html')

def forex_investment(request):
    return render(request, 'home/forex_investment.html')

def forex(request):
    return render(request, 'home/forex.html')

def Contacts(request):
    return render(request, 'home/contacts.html')

@login_required(login_url='/')
def dashboard(request):
    user = request.user

    # Get the active investment
    active_investment = User_Investment.objects.filter(user=user, status='active').first()
    
    sub_active_investment = User_subscription_investment.objects.filter(user=user, status='active').first()


    # Get the most recent deposit transaction
    recent_deposit = DepositTransaction.objects.filter(user=user).order_by('-date').first()

    # Get the most recent withdraw transaction
    recent_withdraw = WithdrawTransaction.objects.filter(user=user).order_by('-date').first()

    # Determine which transaction to display
    recent_transaction = recent_deposit if (recent_deposit and (not recent_withdraw or recent_deposit.date > recent_withdraw.date)) else recent_withdraw

    # Calculate total deposits, total withdrawals, and total transactions
    total_deposits = DepositTransaction.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_withdrawals = WithdrawTransaction.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_transactions = total_deposits + total_withdrawals

    # Prepare context
    context = {
        "investment_plans": InvestmentPlan.objects.all(),
        "active_investment": active_investment,
        "sub_active_investment" : sub_active_investment,
        "recent_transaction": recent_transaction,
        "total_transactions": total_transactions,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='/')
def crypto_exchange(request):
    return render(request, 'dashboard/crypto_exchange.html')

@login_required(login_url='/')
def Profile(request):
    return render(request, 'dashboard/Profile.html')

@login_required(login_url='/')
def Crypto_plan(request):
    print("crypto_plans_view called")
    plans = InvestmentPlan.objects.all()
    print("Plans:", plans) 
    return render(request, 'dashboard/Crypto_plans.html',{'plans': plans})

@login_required(login_url='/')
def subscription_plan(request):
    print("subcription_view called")
    sub_plan = SubscriptionPlan.objects.all()
    print("sub_plan:", sub_plan) 
    return render(request, 'dashboard/subscription_plans.html',{'sub_plan': sub_plan})



@login_required(login_url='/')
def wallet(request):
    return render(request, 'dashboard/wallet.html')

@login_required(login_url='/')
def settings(request):
    return render(request, 'dashboard/settings.html')

@login_required(login_url='/')
def contact_support(request):
    return render(request, 'dashboard/contact_support.html')

@login_required(login_url='/')
def deposite(request):
    return render(request, 'dashboard/deposite.html')

@login_required(login_url='/')
def withdraw_page(request):
    return render(request, 'dashboard/withdraw.html')

def custom_404(request, exception):
    return render(request, 'page_not_found.html', status=404)




