# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-20 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_maduracion', '0004_auto_20170820_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maduracion',
            name='copula',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
        migrations.AlterField(
            model_name='maduracion',
            name='descarte',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
        migrations.AlterField(
            model_name='maduracion',
            name='factura_nauplios',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
        migrations.AlterField(
            model_name='maduracion',
            name='nauplio',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
        migrations.AlterField(
            model_name='maduracion',
            name='ovas',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
    ]
