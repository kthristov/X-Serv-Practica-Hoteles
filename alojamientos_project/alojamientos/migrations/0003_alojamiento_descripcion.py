# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-22 04:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alojamientos', '0002_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='descripcion',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
