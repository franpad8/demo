from django.db import models

class cliente(models.Model):
	nombre	= models.CharField(max_length=200)
	apellidos 	= models.CharField(max_length=200)
	status 	= models.BooleanField(default=True)

	def __unicode__(self):
		nombreCompleto = "%s %s"%(self.nombre, self.apellidos)
		return nombreCompleto

class categoria_producto(models.Model):
	nombre = models.CharField(max_length=200)
	descripcion = models.TextField(max_length=300)

	def __unicode__(self):
		return self.nombre

class producto(models.Model):

	def url(self, filename):
		ruta = "MultimediaData/Users/%s/%s"%(self.nombre, filename)
		return ruta

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(max_length=300)
	status = models.BooleanField(default=True)
	imagen = models.ImageField(upload_to=url)
	precio = models.DecimalField(max_digits=8, decimal_places=2)
	stock = models.IntegerField()
	categoria = models.ManyToManyField(categoria_producto, null=True, blank=True)

	def __unicode__(self):
		return self.nombre
