# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-05 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_larvarios', '0008_auto_20170205_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medidalarva',
            name='estadio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_larvarios.Estadio'),
        ),
    ]