#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import urllib
import xml.sax

from  alojamientos.models import Alojamiento, Imagen, Comentario, Usuario

# Create your views here.

class InkscapeSvgHandler(xml.sax.ContentHandler):

	def __init__ (self):
        	self.alojamiento = None
        	self.current = ""
        	self.lang = ""
        	self.n = 0 # traza

	def startElement(self, name, attrs):
		self.current = name 

		if name == 'service':
			self.alojamiento = Alojamiento()
			self.alojamiento.save()

		if name == 'item' :
			if attrs['name'] == 'Categoria' :
				self.current = 'Categoria'

			if attrs['name'] == 'SubCategoria':
				self.current = 'SubCategoria'

	def characters(self, content):

		# basicData
		if self.current == 'name' :
			self.n = self.n + 1  # traza
			print (self.n)
			print (self.lang)
			self.alojamiento.nombre = content 

		if self.current == 'language' :
			self.lang = content 
			self.alojamiento.language = content

		if self.current == 'body' :
			self.alojamiento.descripcion = content or ""

		if self.current == 'email' :
			self.alojamiento.email = content or ""

		if self.current == 'phone' : 
			self.alojamiento.phone = content or ""

		if self.current == 'web' :
			self.alojamiento.web = content or ""

		if self.current == 'Categoria' :
			self.alojamiento.categoria = content  or ""

		if self.current == 'SubCategoria' :
			self.alojamiento.subcategoria = content or ""
			self.alojamiento.save()

		if self.current == 'address' :
			self.alojamiento.address = content or ""

		if self.current == 'latitude' :
			self.alojamiento.latitude = content  or ""

		if self.current == 'longitude' :
			self.alojamiento.longitude = content  or ""


		# Imagenes
		if self.current == 'url' and self.lang == 'es' :
			self.alojamiento.save()
			Imagen(imagen = content, fid = self.alojamiento ).save()
			
 
	def endElement (self, name):
        	if name =='service':
                	self.alojamiento.save()


def index(request) :

	if request.user.is_authenticated():
		check_user(request.user)

	alojamientos = Alojamiento.objects.filter(language='es')
	if (len(alojamientos) == 0 ) :
		fill_DB()
		alojamientos = Alojamiento.objects.all() 

	context = {}
	 
	alojamientos = Alojamiento.objects.filter(numcomentarios__gt=0).order_by('-numcomentarios')[0:10]
	for i in range(len(alojamientos)) :
		imagenes = Imagen.objects.filter(fid=alojamientos[i].id)
		alojamientos[i].img= imagenes[0]

	users = Usuario.objects.all()

	context['alojamientos'] = alojamientos
	context['usuarios'] = users 

	usuario = None 
	try :
		usuario = Usuario.objects.get(nombre=request.user)
	except :
		print ("No user")

	context['usuario'] = usuario

	return render(request, 'index.html', context)


@csrf_exempt
def lista_alojamientos(request) :
	context = {} 

	if request.method == 'GET':
		context['lista']  = Alojamiento.objects.filter(language='es') 

	if request.method == 'POST':
		cat = request.POST.get('categoria', '')
		subcat= request.POST.get('subcategoria', '')
		if(subcat == '-') :
			subcat = ""
		context['lista'] = Alojamiento.objects.filter(categoria=cat , subcategoria__contains=subcat )

	usuario = None 
	try :
		usuario = Usuario.objects.get(nombre=request.user)
	except :
		print ("No user")

	context['usuario'] = usuario
	return render(request, 'alojamientos.html' , context)

@csrf_exempt
def alojamiento  (request , id_aloj) :

	lang = 'es'
	context = {} 

	context['todos'] = Alojamiento.objects.filter(nombre=id_aloj)
	alojamiento =Alojamiento.objects.get(nombre=id_aloj , language="es") 
	
	imagenes = Imagen.objects.filter(fid=alojamiento.id)
	if (len(imagenes) > 5) :
		imagenes = imagenes[0:5]
	context['imagenes'] =  imagenes

	if request.method == 'POST': 
		usuario = request.user
		lang = request.POST.get('lang', '')
		try : 
			Comentario.objects.get(hotel=id_aloj , usuario=usuario)
		except :
			comentario = request.POST.get('comentario', '')
			if (comentario != '') :
				fecha = datetime.now().strftime('%Y-%m-%d ....  %H : %M')  
				Comentario(hotel=id_aloj , usuario=usuario , text=comentario , fecha=fecha ).save() 
				n = alojamiento.numcomentarios + 1
				alojamiento.numcomentarios = n 
				alojamiento.save()

	context['alojamiento'] = Alojamiento.objects.get(nombre=id_aloj , language=lang)
	comentarios = Comentario.objects.filter(hotel=id_aloj)
	context['comentarios'] = comentarios

	usuario = None 
	try :
		usuario = Usuario.objects.get(nombre=request.user)
	except :
		print ("No user")

	context['usuario'] = usuario

	return render(request, 'info_alojamiento.html' , context )
@csrf_exempt
def pagina (request , id_user) :
	context = {}
	arry = [] 
	user_page = Usuario.objects.get(nombre=id_user )
	usuario = None 
	try :
		usuario = Usuario.objects.get(nombre=request.user)
	except :
		print ("No user")

	if str(id_user) == str(request.user) :
		if request.method == 'POST': 

			color = request.POST.get('color', '')
			if color != "" :
				usuario.col_fuente = color 

			tam = request.POST.get('tam', '')
			if tam != "" :
				usuario.tam_fuente = tam 

			pag_name = request.POST.get('name', '')
			if pag_name != "" :
				usuario.nombre_pagina = pag_name 

			usuario.save()

	comentarios = Comentario.objects.filter(usuario=id_user)

	for com in comentarios :
		aloj = Alojamiento.objects.get(nombre=com.hotel , language='es') 
		aloj.fecha = com.fecha
		arry.append( aloj )

	for i in range(len(arry)) :
		imagenes = Imagen.objects.filter(fid=arry[i].id)
		arry[i].img= imagenes[0]

	context['alojamientos'] = arry
	context['usuario'] = usuario
	context['user_page'] = user_page
	return render(request , 'personal.html' , context )

def xmlreq (request , id_user) :
	context = {}
	arry = [] 

	comentarios = Comentario.objects.filter(usuario=id_user)

	for com in comentarios :
		arry.append( Alojamiento.objects.get(nombre=com.hotel , language='es') )

	context['alojamientos'] = arry
	return render(request , 'personal.xml' , context )

def about (request) :
	context = {}
	usuario = None 
	try :
		usuario = Usuario.objects.get(nombre=request.user)
	except :
		print ("No user")

	context['usuario'] = usuario
	return render(request, 'about.html' , context )

# Funciones auxiliares
def check_user(user) :
	found = False 
	usuarios = Usuario.objects.all() 

	for us in usuarios :
		if str(us.nombre) == str(user):
			found = True
			break 

	if found == False:
		Usuario(nombre=user).save()

	return


# Funciones para la base de datos
def fill_DB() :
	flush_DB()

	file = urllib.request.urlopen('http://cursosweb.github.io/etc/alojamientos_es.xml')
	parser = xml.sax.make_parser()
	parser.setContentHandler(InkscapeSvgHandler())
	parser.parse(file)
	file.close()

	file = urllib.request.urlopen('http://cursosweb.github.io/etc/alojamientos_en.xml')
	parser = xml.sax.make_parser()
	parser.setContentHandler(InkscapeSvgHandler())
	parser.parse(file)
	file.close()

	file = urllib.request.urlopen('http://cursosweb.github.io/etc/alojamientos_fr.xml')
	parser = xml.sax.make_parser()
	parser.setContentHandler(InkscapeSvgHandler())
	parser.parse(file)
	file.close()

def flush_DB() :
	Alojamiento.objects.all().delete() 
	Imagen.objects.all().delete()
	Comentario.objects.all().delete()
	Usuario.objects.all().delete()
