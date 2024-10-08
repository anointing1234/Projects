# Generated by Django 5.0.6 on 2024-07-07 05:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('fullname', models.CharField(max_length=200)),
                ('phone', models.CharField(default='Not set', max_length=15)),
                ('country', models.CharField(default='Not set', max_length=50)),
                ('profile_picture', models.ImageField(upload_to='profile_pics/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btc_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('eth_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('usdt_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('ltc_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('trx_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('bch_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepositTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('Deposit', 'Deposit')], default='Deposit', max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wallet', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('Withdraw', 'Withdraw')], default='Withdraw', max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wallet', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_type', models.CharField(choices=[('USD', 'USD'), ('ETH', 'ETH'), ('BTC', 'BTC'), ('LTC', 'LTC'), ('TRX', 'TRX'), ('BCH', 'BCH')], max_length=3)),
                ('address', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'wallet_type')},
            },
        ),
    ]
