# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-04 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alojamientos', '0004_auto_20160603_0236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel', models.CharField(default='', max_length=100)),
                ('usuario', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=100)),
                ('tam_fuente', models.IntegerField(default=0)),
                ('col_fuente', models.CharField(default='', max_length=50)),
            ],
        ),
    ]