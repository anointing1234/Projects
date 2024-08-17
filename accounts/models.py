from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.withdraw_password = self.make_random_password()
        user.save(using=self._db)
        
        # Create associated Balance entry
        Balance.objects.create(user=user)
        
        # Create associated DepositTransaction and WithdrawTransaction entries
        DepositTransaction.objects.create(user=user, amount=0.00, wallet='Default Wallet')
        WithdrawTransaction.objects.create(user=user, amount=0.00, wallet='Default Wallet', wallet_address='Default Address')
        
        
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, default='Not set')  # Default value
    country = models.CharField(max_length=50, default='Not set')  # Default value
    profile_picture = models.ImageField(upload_to='profile_pics/')
    withdraw_password = models.CharField(max_length=128, blank=True, null=True)  # Add this line

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def update_password(self, new_password):
        self.set_password(new_password)
        self.save()
    
    def update_withdrawal_password(self, new_withdrawal_password):
        self.withdraw_password = make_password(new_withdrawal_password)
        self.save()

class Balance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    btc_balance = models.DecimalField(max_digits=15, decimal_places=7, default=0.00)
    eth_balance = models.DecimalField(max_digits=15, decimal_places=7, default=0.00)
    usdt_balance = models.DecimalField(max_digits=15, decimal_places=7, default=0.00)
    ltc_balance = models.DecimalField(max_digits=15, decimal_places=7, default=0.00)
    trx_balance = models.DecimalField(max_digits=15, decimal_places=7, default=0.00)
    bch_balance = models.DecimalField(max_digits=15, decimal_places=7, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Balance"

class DepositTransaction(models.Model):
    TYPE_CHOICES = (
        ('Deposit', 'Deposit'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Deposit')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"

class WithdrawTransaction(models.Model):
    TYPE_CHOICES = (
        ('Withdraw', 'Withdraw'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Withdraw')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.CharField(max_length=100)
    wallet_address = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"

class WalletAddressManager(models.Manager):
    def create_wallet_for_all_users(self, wallet_type, address):
        User = get_user_model()
        for user in User.objects.all():
            # Check if a WalletAddress already exists for this user and wallet_type
            existing_address = self.filter(user=user, wallet_type=wallet_type).first()
            if not existing_address:
                # If it does not exist, create a new WalletAddress
                self.create(user=user, wallet_type=wallet_type, address=address)

class WalletAddress(models.Model):
    WALLET_CHOICES = [
        ('USD', 'USD'),
        ('ETH', 'ETH'),
        ('BTC', 'BTC'),
        ('LTC', 'LTC'),
        ('TRX', 'TRX'),
        ('BCH', 'BCH'),
    ]
    
    wallet_type = models.CharField(max_length=3, choices=WALLET_CHOICES)
    address = models.CharField(max_length=255, default='hsjdkldjskjljs')
    
    def __str__(self):
        return f"{self.wallet_type} - {self.address}"

class MinimumAmount(models.Model):
    WALLET_CHOICES = [
        ('USD', 'USD'),
        ('ETH', 'ETH'),
        ('BTC', 'BTC'),
        ('LTC', 'LTC'),
        ('TRX', 'TRX'),
        ('BCH', 'BCH'),
    ]

    wallet_type = models.CharField(max_length=3, choices=WALLET_CHOICES, unique=True)
    min_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    min_withdrawal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.wallet_type} - Min Deposit: {self.min_deposit} - Min Withdrawal: {self.min_withdrawal}"
    
    
    
    
    
    
class InvestmentPlan(models.Model):
    PLAN_CHOICES = [
        ('USD', 'USD Investment Plan'),
        ('ETH', 'ETH Investment Plan'),
        ('BTC', 'BTC Investment Plan'),
        ('LTC', 'LTC Investment Plan'),
        ('TRX', 'TRX Investment Plan'),
        ('BCH', 'BCH Investment Plan'),
    ]

    plan_type = models.CharField(max_length=3, choices=PLAN_CHOICES, unique=True)
    investment_amount_min = models.DecimalField(max_digits=10, decimal_places=2)
    investment_amount_max = models.DecimalField(max_digits=10, decimal_places=2)
    expected_profit_min = models.DecimalField(max_digits=5, decimal_places=2)
    expected_profit_max = models.DecimalField(max_digits=5, decimal_places=2)
    duration_min_months = models.IntegerField()
    duration_max_months = models.IntegerField()

    def __str__(self):
        return dict(self.PLAN_CHOICES).get(self.plan_type)
    




class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('EUR/USD', 'EUR/USD Plan'),
        ('USD/JPY', 'USD/JPY Plan'),
        ('GBP/USD', 'GBP/USD Plan'),
        ('USD/CAD', 'USD/CAD Plan'),
    ]

    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    investment_amount_min = models.DecimalField(max_digits=10, decimal_places=2)
    investment_amount_max = models.DecimalField(max_digits=10, decimal_places=2)
    expected_profit_min = models.DecimalField(max_digits=5, decimal_places=2)
    expected_profit_max = models.DecimalField(max_digits=5, decimal_places=2)
    duration_min_months = models.IntegerField()
    duration_max_months = models.IntegerField()

    def __str__(self):
        return dict(self.PLAN_CHOICES).get(self.plan_name)    
    
    
class User_Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
    date_invested = models.DateTimeField(auto_now_add=True)
    expected_return = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()
    status = models.CharField(max_length=10, choices=[
    ('active', 'Active'),
    ('completed', 'Completed'),
])
    def __str__(self):
        return f"{self.user.username} - {self.investment_plan} - {self.amount_invested} - {self.date_invested}"



class User_subscription_investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
    date_invested = models.DateTimeField(auto_now_add=True)
    expected_return = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()
    status = models.CharField(max_length=10, choices=[
    ('active', 'Active'),
    ('completed', 'Completed'),
])
    def __str__(self):
        return f"{self.user.username} - {self.investment_plan} - {self.amount_invested} - {self.date_invested}"    
    
