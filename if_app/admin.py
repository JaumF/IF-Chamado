from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'numero_celular', 'identificacao', 'is_staff', 'is_active')
    search_fields = ('email', 'nome')
    list_filter = ('identificacao', 'is_staff', 'is_active')

admin.site.register(Usuario, UsuarioAdmin)
