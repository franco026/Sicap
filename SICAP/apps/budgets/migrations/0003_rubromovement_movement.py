# Generated by Django 3.0.8 on 2021-07-24 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_remove_rubromovement_movement'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubromovement',
            name='movement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Movement'),
        ),
    ]
