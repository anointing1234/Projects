from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.html import strip_tags
from django.contrib.auth import login,authenticate
from accounts.forms import RegistrationForm,AccountAuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .forms import ProfilePictureForm,ContactForm
from .models import WalletAddress,Account
from django.db.models.signals import post_save
from django.http import JsonResponse
from .models import WalletAddress,MinimumAmount,DepositTransaction, WithdrawTransaction, Balance, InvestmentPlan,SubscriptionPlan,User_Investment,User_subscription_investment
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
import json
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
import os
from django.conf import settings
import shutil
from requests.exceptions import ConnectionError
import requests 





def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            confirm_password = form.cleaned_data.get('password2')
            if raw_password == confirm_password:
                account = authenticate(email=user.email, password=raw_password)
                if account is not None:
                    login(request, account)
                    messages.success(request, 'Registration successful. You can now log in.')
                    return render(request, 'registeration/signup.html', {'form': form, 'registration_success': True})
                else:
                    messages.error(request, 'Authentication failed. Please try again.')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'registeration/signup.html', context)

def Signup(request):
    form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'registeration/signup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return render(request, 'registeration/login.html', {'form': form, 'login_success': True})
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = AccountAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'registeration/login.html', context)

def Login(request):
    form = AccountAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'registeration/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))


def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully!')
            return redirect(reverse('Profile'))  # Change 'profile' to the name of your profile URL
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {strip_tags(error)}")
    else:
        form = ProfileUpdateForm(instance=request.user)
        
    return render(request,'dashboard/profile.html', {'form': form})


def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            print("Form is valid")
            # Delete the old profile picture
            if request.user.profile_picture:
                print("Old profile picture exists")
                old_picture_path = os.path.join(settings.MEDIA_ROOT, str(request.user.profile_picture))
                print("Old picture path:", old_picture_path)
                try:
                    shutil.rmtree(os.path.dirname(old_picture_path))
                    print("Old picture file deleted")
                except OSError as e:
                    print("Error deleting file:", e)
                    print("Error details:", e.filename, e.strerror)
                except Exception as e:
                    print("Unexpected error:", e)
            # Save the new profile picture
            profile_picture = form.save(commit=False)
            profile_picture.profile_picture = request.FILES['profile_picture']
            profile_picture.save()
            print("New profile picture saved")
            return redirect(reverse('Profile'))
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = ProfilePictureForm(instance=request.user)
        return render(request, 'update_profile_picture.html', {'form': form})
    return redirect(reverse('Profile'))




def get_wallet_address(request):
    if request.method == 'GET':
        wallet_type = request.GET.get('wallet')
        try:
            wallet_address = WalletAddress.objects.get(wallet_type=wallet_type)
            try:
                min_amount = MinimumAmount.objects.get(wallet_type=wallet_type)
                response_data = {
                    'wallet_address': wallet_address.address,
                    'min_deposit': float(min_amount.min_deposit),
                    'min_withdrawal': float(min_amount.min_withdrawal)
                }
                return JsonResponse(response_data)
            except MinimumAmount.DoesNotExist:
                return JsonResponse({'error': 'Minimum amount not set for this wallet type'}, status=404)
        except WalletAddress.DoesNotExist:
            return JsonResponse({'error': 'Wallet address not found'}, status=404)

def deposit_submit(request):
    amount = request.POST.get('amount')
    wallet = request.POST.get('wallet')
    deposit_type = request.POST.get('type')  # Ensure 'type' matches the name attribute in your form

    # Validate and process the deposit (example validation, adjust as per your needs)
    if amount and wallet:
        try:
            deposit = DepositTransaction.objects.create(
                user=request.user,
                transaction_type=deposit_type,
                amount=amount,
                wallet=wallet,
                status='Pending'  # Assuming new deposits start as pending
            )
            deposit.save()
            return JsonResponse({'status': 'success', 'message': 'Deposit request submitted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid data submitted'})      






def transactions_view(request):
    withdraw_transactions = WithdrawTransaction.objects.filter(user=request.user)
    deposit_transactions = DepositTransaction.objects.filter(user=request.user)
    
    context = {
        'withdraw_transactions': withdraw_transactions,
        'deposit_transactions': deposit_transactions,
    }
    return render(request, reverse('dashboard'), context)



@login_required
def confirm_deposit(request, deposit_id):
    deposit = get_object_or_404(DepositTransaction, id=deposit_id, status='Pending')
    deposit.status = 'Completed'
    deposit.save()

    user = deposit.user
    amount = deposit.amount
    wallet_type = deposit.wallet

    try:
        balance = Balance.objects.get(user=user)
        if wallet_type == 'USD':
            balance.usdt_balance += amount
        elif wallet_type == 'ETH':
            balance.eth_balance += amount
        elif wallet_type == 'BTC':
            balance.btc_balance += amount
        elif wallet_type == 'LTC':
            balance.ltc_balance += amount
        elif wallet_type == 'TRX':
            balance.trx_balance += amount
        elif wallet_type == 'BCH':
            balance.bch_balance += amount
        else:
            pass
        balance.save()
        messages.success(request, f'Amount credited to {wallet_type} balance successfully.')
    except Balance.DoesNotExist:
        messages.error(request, 'User balance not found.')

    return redirect('admin:accounts_deposittransaction_changelist')





@login_required
def confirm_withdraw(request, withdraw_id):
    withdraw = get_object_or_404(WithdrawTransaction, id=withdraw_id, status='Pending')
    withdraw.status = 'Completed'
    withdraw.save()
    messages.success(request, f'Withdraw with ID {withdraw.id} completed successfully.')
    return redirect('admin:accounts_withdrawtransaction_changelist')




@login_required
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        
        if not user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect.'}, status=400)
        
        if new_password != confirm_password:
            return JsonResponse({'error': 'New passwords do not match.'}, status=400)
        
        user.update_password(new_password)
        return JsonResponse({'success': 'Password updated successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_protect
@login_required
def update_withdrawal_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_withdrawal_password = data.get('new_withdrawal_password')
            confirm_withdrawal_password = data.get('confirm_withdrawal_password')
            
            if not new_withdrawal_password or not confirm_withdrawal_password:
                return JsonResponse({'error': 'Both password fields are required.'}, status=400)
            
            if new_withdrawal_password != confirm_withdrawal_password:
                return JsonResponse({'error': 'New withdrawal passwords do not match.'}, status=400)
            
            user = request.user
            hashed_password = make_password(new_withdrawal_password)  # Hash the new password
            user.withdraw_password = hashed_password
            user.save()
            
            return JsonResponse({'success': 'Withdrawal password updated successfully!'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)



@csrf_protect
@login_required
def check_withdraw_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        withdraw_password = data.get('withdraw_password')
        
        user = request.user
        hashed_withdraw_password = user.withdraw_password
        
        if check_password(withdraw_password, hashed_withdraw_password):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)  
 

@login_required
def withdraw_submit(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        wallet = request.POST.get('wallet')
        wallet_address = request.POST.get('wallet_address')
        transaction_type = request.POST.get('type')

        try:
            # Retrieve the user's balance object
            balance = get_object_or_404(Balance, user=request.user)

            # Determine which balance to update
            if wallet == 'USD':
                if balance.usdt_balance >= amount:
                    balance.usdt_balance -= amount
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
            elif wallet == 'ETH':
                if balance.eth_balance >= amount:
                    balance.eth_balance -= amount
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
            elif wallet == 'BTC':
                if balance.btc_balance >= amount:
                    balance.btc_balance -= amount
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
            elif wallet == 'LTC':
                if balance.ltc_balance >= amount:
                    balance.ltc_balance -= amount
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
            elif wallet == 'TRX':
                if balance.trx_balance >= amount:
                    balance.trx_balance -= amount
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
            elif wallet == 'BCH':
                if balance.bch_balance >= amount:
                    balance.bch_balance -= amount
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid wallet type'})

            # Save the updated balance
            balance.save()

            # Record the withdrawal transaction
            withdrawal = WithdrawTransaction.objects.create(
                user=request.user,
                transaction_type=transaction_type,
                amount=amount,
                wallet=wallet,
                wallet_address=wallet_address,
                status='Pending'
            )
            withdrawal.save()

            return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_protect
def verify_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        user_exists = Account.objects.filter(email=email).exists()
        return JsonResponse({'exists': user_exists})

@csrf_protect
def send_reset_password_link(request):
    if request.method == 'POST':
        try:
            # Check for internet connection by making a request to a reliable URL
            requests.get("http://www.google.com", timeout=5)
        except ConnectionError:
            return JsonResponse({'status': 'error', 'message': 'No internet connection'}, status=500)
        data = json.loads(request.body)
        email = data.get('email')
        user = Account.objects.filter(email=email).first()
        if user:
            try:
                send_mail(
                    'Password Reset Request',
                    'Here is the link to reset your password: http://127.0.0.1:8000/password_reset/password_reset.html',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



@csrf_protect
def invest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        amount = Decimal(data.get('amount'))
        user = request.user
        update_existing = data.get('update_existing', False)  # Flag to determine if we should update the existing investment

        plan = get_object_or_404(InvestmentPlan, id=plan_id)
        user_balance = Balance.objects.get(user=user)

        # Map plan types to the correct balance fields
        balance_fields = {
            "USD": "usdt_balance",
            "ETH": "eth_balance",
            "BTC": "btc_balance",
            "LTC": "ltc_balance",
            "TRX": "trx_balance",
            "BCH": "bch_balance",
        }

        balance_field = balance_fields.get(plan.plan_type)

        if not balance_field:
            return JsonResponse({'success': False, 'message': "Invalid investment plan type."})

        current_balance = getattr(user_balance, balance_field)

        if amount < plan.investment_amount_min or amount > plan.investment_amount_max:
            return JsonResponse({'success': False, 'message': f"Amount must be between {plan.investment_amount_min} and {plan.investment_amount_max}"})

        if amount > current_balance:
            return JsonResponse({'success': False, 'message': "Insufficient balance for this investment."})

        # Check for an existing active investment
        active_investment = User_Investment.objects.filter(user=user, status='active').first()

        if active_investment and not update_existing:
            # Respond to the client to prompt the user for confirmation
            return JsonResponse({
                'success': False,
                'confirm_update': True,
                'message': 'You already have an active investment plan. Do you want to update it?'
            })

        if active_investment and update_existing:
            # Update the existing active investment
            active_investment.amount_invested = amount
            active_investment.investment_plan = plan
            active_investment.expected_return = plan.expected_profit_min
            active_investment.duration_months = plan.duration_min_months
            active_investment.save()
            investment_message = "Successfully updated your active investment."
        else:
            # Create a new investment record
            User_Investment.objects.create(
                user=user,
                investment_plan=plan,
                amount_invested=amount,
                expected_return=plan.expected_profit_min,  # Example: set the expected return to the minimum expected profit
                duration_months=plan.duration_min_months,  # Example: set the duration to the minimum duration
                status='active'
            )
            investment_message = f"Successfully invested {amount} in {plan.plan_type}."

        # Deduct amount from user's balance
        setattr(user_balance, balance_field, current_balance - amount)
        user_balance.save()

        return JsonResponse({'success': True, 'message': investment_message})

    return JsonResponse({'success': False, 'message': "Invalid request method."})


@csrf_protect

def invest_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        amount = Decimal(data.get('amount'))
        plan_type = data.get('plan_type')
        user = request.user
        update_existing = data.get('update_existing', False)  # Flag to determine if we should update the existing investment

        # Get the SubscriptionPlan instance
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        user_balance = get_object_or_404(Balance, user=user)  # Ensure we get the user's balance

        # Map plan types to the correct balance field
        balance_fields = {
            "EUR/USD": "usdt_balance",
            "USD/JPY": "usdt_balance",
            "GBP/USD": "usdt_balance",
            "USD/CAD": "usdt_balance",
        }

        balance_field = balance_fields.get(plan.plan_name)

        if not balance_field:
            return JsonResponse({'success': False, 'message': "Invalid investment plan type."})

        current_balance = getattr(user_balance, balance_field)

        if amount < plan.investment_amount_min or amount > plan.investment_amount_max:
            return JsonResponse({'success': False, 'message': f"Amount must be between {plan.investment_amount_min} and {plan.investment_amount_max}"})

        if amount > current_balance:
            return JsonResponse({'success': False, 'message': "Insufficient balance for this investment."})

        # Check for an existing active investment
        active_investment = User_subscription_investment.objects.filter(user=user, investment_plan=plan, status='active').first()

        if active_investment and not update_existing:
            # Respond to the client to prompt the user for confirmation
            return JsonResponse({
                'success': False,
                'confirm_update': True,
                'message': 'You already have an active investment plan. Do you want to update it?'
            })

        if active_investment and update_existing:
            # Update the existing active investment
            active_investment.amount_invested = amount
            active_investment.expected_return = plan.expected_profit_min
            active_investment.duration_months = plan.duration_min_months
            active_investment.save()
            investment_message = "Successfully updated your active investment."
        else:
            # Create a new investment record
            User_subscription_investment.objects.create(
                user=user,
                investment_plan=plan,
                amount_invested=amount,
                expected_return=plan.expected_profit_min,  # Example: set the expected return to the minimum expected profit
                duration_months=plan.duration_min_months,  # Example: set the duration to the minimum duration
                status='active'
            )
            investment_message = f"Successfully invested {amount} in {plan.plan_name}."

        # Deduct amount from user's balance
        setattr(user_balance, balance_field, current_balance - amount)
        user_balance.save()

        return JsonResponse({'success': True, 'message': investment_message})

    return JsonResponse({'success': False, 'message': "Invalid request method."})

@csrf_protect
def check_active_investment(request):
    user = request.user
    active_investment = User_Investment.objects.filter(user=user, status='active').exists()
    return JsonResponse({'active_investment': active_investment})


@csrf_protect
def sub_check_active_investment(request):
    user = request.user
    active_investment = User_subscription_investment.objects.filter(user=user, status='active').first()
    return JsonResponse({'active_investment': active_investment is not None})

@csrf_protect
def get_balances(request):
    try:
        balance = Balance.objects.get(user=request.user)
        balances = {
            'BTC': float(balance.btc_balance),
            'ETH': float(balance.eth_balance),
            'USDT': float(balance.usdt_balance),
            'LTC': float(balance.ltc_balance),
            'TRX': float(balance.trx_balance),
            'BCH': float(balance.bch_balance),
        }
        return JsonResponse(balances)
    except Balance.DoesNotExist:
        return JsonResponse({'error': 'Balance not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
    
@csrf_protect
def update_balances(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user  # Ensure user is authenticated
            
            # Fetch the user's balance
            balance = Balance.objects.get(user=user)
            
            # Update the user's balances
            balance.btc_balance = data.get('BTC', balance.btc_balance)
            balance.eth_balance = data.get('ETH', balance.eth_balance)
            balance.usdt_balance = data.get('USDT', balance.usdt_balance)
            balance.ltc_balance = data.get('LTC', balance.ltc_balance)
            balance.trx_balance = data.get('TRX', balance.trx_balance)
            balance.bch_balance = data.get('BCH', balance.bch_balance)
            balance.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error updating balances: {e}")  # Log error for debugging
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_protect
def contact_support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Email = form.cleaned_data['email']
            Subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email_content = f"email = {Email},message = {message}"
                
            try:
                send_mail(
                    Subject,
                    email_content,
                    Email,
                    ['yakubudestiny9@gmail.com'],  # Recipient email
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again later.')
            
            return redirect('contact_support')
    else:
        form = ContactForm()
    
    return render(request, 'dashboard/contact_support.html', {'form': form})



def custom_404(request, exception):
    return render(request, 'page_not_found.html', status=404)    