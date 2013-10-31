from django.contrib import admin
from demo.apps.ventas.models import cliente, producto, categoria_producto

admin.site.register(cliente)
admin.site.register(producto)
admin.site.register(categoria_producto)
