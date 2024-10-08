# Generated by Django 5.0.7 on 2024-08-03 16:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_user_investment'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_subscription_investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_invested', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_invested', models.DateTimeField(auto_now_add=True)),
                ('expected_return', models.DecimalField(decimal_places=2, max_digits=5)),
                ('duration_months', models.IntegerField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], max_length=10)),
                ('Sub_investment_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.investmentplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
