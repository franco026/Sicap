# Generated by Django 3.0.8 on 2022-03-15 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0033_auto_20220225_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ccpet',
            name='accountPeriod',
        ),
        migrations.AddField(
            model_name='ccpet',
            name='bussines',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines'),
        ),
    ]
