from django.contrib import admin, messages
from django.utils.html import format_html
from django.conf import settings
from django.contrib.auth import get_user_model
from django import forms
from django.db import transaction
from django.shortcuts import render
from django.urls import path,reverse
from .models import Account, Balance, DepositTransaction, WithdrawTransaction, WalletAddress, MinimumAmount,InvestmentPlan,SubscriptionPlan,User_Investment,User_subscription_investment

class WalletAddressForm(forms.ModelForm):
    class Meta:
        model = WalletAddress
        fields = ['wallet_type', 'address']

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    actions = ['delete_accounts_with_balances']

    def delete_model(self, request, obj):
        Balance.objects.filter(user=obj).delete()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            Balance.objects.filter(user=obj).delete()
        super().delete_queryset(request, queryset)

    def delete_accounts_with_balances(self, request, queryset):
        for obj in queryset:
            Balance.objects.filter(user=obj).delete()
        queryset.delete()
    delete_accounts_with_balances.short_description = "Delete selected accounts and their related balances"

admin.site.register(Account, AccountAdmin)

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'btc_balance', 'eth_balance', 'usdt_balance', 'ltc_balance', 'trx_balance', 'bch_balance')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['user']
        return []

    def has_add_permission(self, request, obj=None):
        return False  # Prevents adding new balances from the admin

    def has_delete_permission(self, request, obj=None):
        return True  # Allow deleting balances from the admin
    
admin.site.register(Balance, BalanceAdmin)


class WalletAddressAdmin(admin.ModelAdmin):
    list_display = ('wallet_type', 'address')
    form = WalletAddressForm

admin.site.register(WalletAddress, WalletAddressAdmin)

class MinimumAmountAdmin(admin.ModelAdmin):
    list_display = ('wallet_type', 'min_deposit', 'min_withdrawal')

admin.site.register(MinimumAmount, MinimumAmountAdmin)  



class DepositTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'wallet', 'date', 'status', 'confirm_button')

    def confirm_button(self, obj):
        if obj.status == 'Pending':
            return format_html('<button type="button" class="button" onclick="window.location.href=\'{}\';">Confirm</button>',
                               reverse('confirm_deposit', args=[obj.id]))
        elif obj.status == 'Completed':
            return 'Completed'
        return ''

    confirm_button.short_description = 'Confirm'

    

    def wallet(self, obj):
        return obj.wallet.capitalize()

    wallet.short_description = 'Wallet'

    @admin.action(description='Confirm selected deposits')
    @transaction.atomic
    def confirm_deposit(self, request, queryset):
        for deposit in queryset:
            if deposit.status == 'Pending':
                deposit.status = 'Completed'
                deposit.save()

                # Credit user's balance based on wallet type
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
                        # Handle any other wallet types here
                        pass
                    balance.save()
                    messages.success(request, f'Amount credited to {wallet_type} balance successfully.')
                except Balance.DoesNotExist:
                    messages.error(request, 'User balance not found.')

            else:
                messages.error(request, f'Deposit with ID {deposit.id} is already completed.')


admin.site.register(DepositTransaction, DepositTransactionAdmin)



class WithdrawTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'wallet','wallet_address','date', 'status', 'confirm_button')

    def confirm_button(self, obj):
        if obj.status == 'Pending':
            return format_html('<button type="button" class="button" onclick="window.location.href=\'{}\';">Confirm</button>',
                               f'/accounts/confirm_withdraw/{obj.id}/')
        return 'Completed'

    confirm_button.short_description = 'Confirm'


    def wallet(self, obj):
        return obj.wallet.capitalize()

    wallet.short_description = 'Wallet'

admin.site.register(WithdrawTransaction, WithdrawTransactionAdmin)




admin.site.register(InvestmentPlan)
admin.site.register(SubscriptionPlan)
admin.site.register(User_Investment)
admin.site.register(User_subscription_investment)
