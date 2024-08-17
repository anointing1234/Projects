# Generated by Django 5.0.6 on 2024-07-07 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_walletaddress_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinimumAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_type', models.CharField(choices=[('USD', 'USD'), ('ETH', 'ETH'), ('BTC', 'BTC'), ('LTC', 'LTC'), ('TRX', 'TRX'), ('BCH', 'BCH')], max_length=3, unique=True)),
                ('min_deposit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_withdrawal', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
