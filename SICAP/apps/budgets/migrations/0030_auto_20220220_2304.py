# Generated by Django 3.0.8 on 2022-02-21 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0029_ccpet_accountperiod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ccpet',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
