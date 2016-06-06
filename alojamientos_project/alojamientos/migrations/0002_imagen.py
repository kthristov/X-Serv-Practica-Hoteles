# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-22 02:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alojamientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.URLField(default='', max_length=500)),
                ('fid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alojamientos.Alojamiento')),
            ],
        ),
    ]