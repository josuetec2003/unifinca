# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-25 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_larvarios', '0006_auto_20170110_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datoparametroagua',
            name='fecha_ingreso',
            field=models.DateField(auto_now_add=True),
        ),
    ]
