# Generated by Django 3.0.8 on 2021-09-24 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0005_auto_20210805_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='RubroInformdetall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informdetall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.InformDetall')),
                ('rubro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Rubro')),
            ],
        ),
        migrations.CreateModel(
            name='RubroInform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inform', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Inform')),
                ('rubro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Rubro')),
            ],
        ),
    ]