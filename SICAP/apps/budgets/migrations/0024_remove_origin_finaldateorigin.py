# Generated by Django 3.0.8 on 2022-01-16 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0023_closedperiod_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='origin',
            name='finalDateOrigin',
        ),
    ]
