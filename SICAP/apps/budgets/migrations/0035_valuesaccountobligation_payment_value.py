# Generated by Django 3.0.8 on 2022-03-16 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0034_auto_20220314_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='valuesaccountobligation',
            name='payment_value',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
