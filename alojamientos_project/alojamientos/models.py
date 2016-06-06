from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Alojamiento (models.Model):
	nombre = models.CharField(max_length = 100, default = "")
	language = models.CharField(max_length = 20 , default = "")
	descripcion = models.CharField(max_length = 5000 , default = "")
	email = models.CharField(max_length = 100, default = "")
	phone = models.CharField(max_length = 50, default = "")
	fax = models.CharField(max_length = 50, default = "")
	web = models.CharField(max_length = 100, default = "")
	categoria = models.CharField(max_length = 50, default = "")
	subcategoria = models.CharField(max_length = 50, default = "")
	address = models.CharField(max_length = 100 , default = "")
	latitude = models.CharField(max_length = 30 , default = "")
	longitude = models.CharField(max_length = 30 , default = "")
	numcomentarios = models.IntegerField (default=0)
	img = models.URLField( max_length=500, default="") 
	fecha = models.CharField(max_length = 100, default = "")

class Imagen (models.Model) :
	imagen = models.URLField( max_length=500, default="") 
	fid = models.ForeignKey(Alojamiento)

class Usuario(models.Model):
	nombre = models.CharField(max_length = 100, default = "")
	nombre_pagina = models.CharField(max_length = 100, default = "")
	tam_fuente = models.CharField (max_length = 50, default = "")
	col_fuente = models.CharField(max_length = 50, default = "")

class Comentario(models.Model) :
	hotel = models.CharField(max_length = 100, default = "")
	usuario = models.CharField(max_length = 100, default = "")
	text = models.CharField(max_length=1000, default="")
	fecha = models.CharField(max_length = 100, default = "")

class HotelAñadido(models.Model) :
	hotel = models.CharField(max_length = 100, default = "")
	usuario = models.CharField(max_length = 100, default = "")
