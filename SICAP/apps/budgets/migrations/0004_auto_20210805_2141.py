# Generated by Django 3.0.8 on 2021-08-06 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_rubromovement_movement'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='agreementNameAg',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='rubrobalanceoperation',
            name='agreement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Agreement'),
        ),
        migrations.AddField(
            model_name='rubrobalanceoperation',
            name='agreementNameAg',
            field=models.BigIntegerField(null=True),
        ),
    ]
