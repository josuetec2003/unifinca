# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-21 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_general', '0003_datoparametroagua'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datoparametroagua',
            name='fecha_ingreso',
            field=models.DateField(auto_now_add=True),
        ),
    ]
