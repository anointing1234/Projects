# Generated by Django 5.0.6 on 2024-07-09 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_withdraw_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='bch_balance',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='balance',
            name='btc_balance',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='balance',
            name='eth_balance',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='balance',
            name='ltc_balance',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='balance',
            name='trx_balance',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='balance',
            name='usdt_balance',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=15),
        ),
    ]
