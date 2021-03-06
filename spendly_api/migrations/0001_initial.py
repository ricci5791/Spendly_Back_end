# Generated by Django 3.1.2 on 2020-10-25 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('currency_code', models.IntegerField(default=980)),
                ('type', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
                ('description', models.CharField(default='', max_length=100)),
                ('mcc', models.IntegerField(default=-1)),
                ('amount', models.IntegerField(default=0)),
                ('currency_code', models.IntegerField(default=980)),
                ('balance', models.IntegerField(default=0)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='spendly_api.account')),
            ],
        ),
    ]
