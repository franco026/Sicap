# Generated by Django 3.0.8 on 2022-02-21 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0030_auto_20220220_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ccpet',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]