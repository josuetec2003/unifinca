# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-11 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_general', '0002_modeltest'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatoParametroAgua',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.CharField(max_length=15)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
                ('ph', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='pH')),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('oxigeno', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('salinidad', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('origen_agua', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_general.OrigenAgua')),
            ],
            options={
                'ordering': ['-fecha_ingreso', 'departamento'],
            },
        ),
    ]