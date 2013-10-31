from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.apps.ventas.forms import addProductForm
from demo.apps.ventas.models import producto
from django.http import HttpResponseRedirect

def add_product_view(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = addProductForm(request.POST, request.FILES)
			info = "Inicializando"
			if form.is_valid():
				nombre = form.cleaned_data["nombre"]
				descripcion = form.cleaned_data["descripcion"]
				imagen = form.cleaned_data["imagen"] #Esto se obtiene con el request.FILES
				precio = form.cleaned_data["precio"]
				stock = form.cleaned_data["stock"]
				p = producto()
				p.nombre = nombre
				p.descripcion = descripcion

				if p.imagen: #Si existe la imagen, la cargamos.
					p.imagen = imagen
				p.precio = precio
				p.stock = stock
				p.status = True
				p.save() # Guardar la informacion
				info = "Se guardo satisfactoriamente..."
			else:
				info = "Informacion con datos incorrectos"

			form = addProductForm()
			ctx = {"form":form, "informacion":info}
			return render_to_response('ventas/addProducto.html', ctx, context_instance=RequestContext(request))
		else:
			form = addProductForm()
			ctx = {'form':form}
			return render_to_response('ventas/addProducto.html', ctx, context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect("/")

def edit_product_view(request, id_prod):
	if request.user.is_authenticated():
		p = producto.objects.get(id=id_prod)
		if request.method == 'POST':
			form = addProductForm(request.POST, request.FILES)
			if form.is_valid():
				nombre = form.cleaned_data["nombre"]
				descripcion = form.cleaned_data["descripcion"]
				imagen = form.cleaned_data["imagen"] #Esto se obtiene con el request.FILES
				precio = form.cleaned_data["precio"]
				stock = form.cleaned_data["stock"]
				p.nombre = nombre
				p.descripcion = descripcion

				if imagen: #Si existe la imagen, la cargamos.
					p.imagen = imagen
				p.precio = precio
				p.stock = stock
				p.save()
				return HttpResponseRedirect('/producto/%s/'%p.id)
				
			else:
				ctx = {"form":form, "informacion":info}
				info = "Informacion con datos incorrectos"
				return render_to_response('ventas/editProducto.html', ctx, context_instance=RequestContext(request))
				
			

		else:
			form = addProductForm(initial={'nombre':p.nombre,
										  'descripcion':p.descripcion,
										  'precio':p.precio,
										  'stock':p.stock})
			ctx={"form":form, "producto":p}
			return render_to_response('ventas/editProducto.html', ctx, context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect("/")
