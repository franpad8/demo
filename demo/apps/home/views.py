from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.apps.ventas.models import producto
from demo.apps.home.forms import ContactForm, LoginForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
# Paginacion en Django
from django.core.paginator import Paginator, EmptyPage, InvalidPage


def index_view(request):
	return render_to_response('home/index.html', context_instance=RequestContext(request))

def about_view(request):
	mensaje = "Esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje}
	return render_to_response('home/about.html', ctx, context_instance=RequestContext(request))

def productos_view(request, pagina):
	lista_prod = producto.objects.filter(status=True).order_by('id')
	paginator = Paginator(lista_prod, 3) # Cuantos prods quieres por paginas
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		productos = paginator.page(paginator.num_pages)
	ctx = {'productos':productos}
	return render_to_response('home/productos.html', ctx, context_instance=RequestContext(request))

def singleProducto_view(request, id_prod):
	prod = producto.objects.get(id=id_prod)
	cats = prod.categoria.all()
	ctx = {'producto': prod, 'categorias':cats}
	return render_to_response('home/SingleProducto.html', ctx, context_instance=RequestContext(request))	

def contacto_view(request):
	info_enviado = False # Definir si se envio la info o no
        email = ""
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']				
			titulo = formulario.cleaned_data['Titulo'] 
			texto = formulario.cleaned_data['Texto']

			# Configuracion enviando mensaje
			to_admin = 'franpad8@gmail.com'
			html_content = "Informacion recibida <br><br><br>***Mensaje***<br><br><br>%s"%(texto)
			msg = EmailMultiAlternatives('Correo de Contacto', html_content, 'from@server.com', [to_admin])
			msg.attach_alternative(html_content, 'text/html') #Definimos el contenido como html
			msg.send() #Enviamos el correo
	else:
		formulario = ContactForm()


	ctx = {'form': formulario, 'email':email, 'titulo':titulo, 'texto':texto, 'info_enviado':info_enviado}
	return render_to_response('home/contacto.html', ctx, context_instance=RequestContext(request))


def login_view(request):	
	mensaje=""
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data["username"]
				password = form.cleaned_data["password"]
				usuario = authenticate(username=username, password=password)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje="Usuario y/o password incorrecto"
		form = LoginForm()
		ctx = {"form":form, 'mensaje':mensaje}
		return render_to_response("home/login.html", ctx, context_instance=RequestContext(request)) 
	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")
