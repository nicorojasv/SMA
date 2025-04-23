from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento, CustomUser, Reporte, Comuna

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Plan. Hereda de `admin.ModelAdmin` para personalizar la interfaz de administración.

    Atributos:
        - list_display: Campos a mostrar en la lista de planes.
        - list_filter: Filtros disponibles en la barra lateral.
        - search_fields: Campos que se pueden buscar.
        - ordering: Orden predeterminado de los registros.
        - list_per_page: Cantidad de registros por página. Se establece en 20.
    """
    list_display = ('codigo', 'nombre', 'fecha_registro', 'comuna', 'estado')
    list_filter = ('fecha_registro', 'codigo')
    search_fields = ('codigo', 'nombre', 'comuna')
    ordering = ('-fecha_registro',)
    list_per_page = 20

@admin.register(Medida)
class MedidaAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Medida. Hereda de `admin.ModelAdmin` para personalizar la interfaz de administración.

    Atributos:
        - list_display: Campos a mostrar en la lista de medidas.
        - list_filter: Filtros disponibles en la barra lateral.
        - search_fields: Campos que se pueden buscar.
        - ordering: Orden predeterminado de los registros.
    """
    list_display = ('nombre', 'indicador', 'plan', 'organismo_sectorial')
    list_filter = ('organismo_sectorial', 'plan')
    search_fields = ('nombre',)

@admin.register(OrganismoSectorial)
class OrganismoSectorialAdmin(admin.ModelAdmin):
    """
    Admin para el modelo OrganismoSectorial. Hereda de `admin.ModelAdmin` para personalizar la interfaz de administración.

    Atributos:
        - list_display: Campos a mostrar en la lista de organismos sectoriales.
        - search_fields: Campos que se pueden buscar.
        - ordering: Orden predeterminado de los registros.
    """
    list_display = ('nombre', 'sigla')
    search_fields = ('nombre', 'sigla')
    ordering = ('nombre',)

@admin.register(TipoMedida)
class TipoMedidaAdmin(admin.ModelAdmin):
    """
    Admin para el modelo TipoMedida. Hereda de `admin.ModelAdmin` para personalizar la interfaz de administración.

    Atributos:
        - list_display: Campos a mostrar en la lista de tipos de medida.
        - search_fields: Campos que se pueden buscar.
    """
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Documento. Hereda de `admin.ModelAdmin` para personalizar la interfaz de administración.

    Atributos:
        - list_display: Campos a mostrar en la lista de documentos.
        - list_filter: Filtros disponibles en la barra lateral.
        - search_fields: Campos que se pueden buscar.
    """
    list_display = ('nombre', 'fecha', 'reporte')
    list_filter = ('reporte', 'fecha')
    search_fields = ('nombre',)

class CustomUserAdmin(UserAdmin):
    """
    Admin para el modelo CustomUser. Hereda de `UserAdmin` para personalizar la interfaz de administración.

    Atributos:
        - list_display: Campos a mostrar en la lista de usuarios. 
        - list_filter: Filtros disponibles en la barra lateral. 
        - search_fields: Campos que se pueden buscar. 
        - ordering: Orden predeterminado de los registros. Ordena por RUT.
        - add_fieldsets: Campos a mostrar al agregar un nuevo usuario. 
        - fieldsets: Campos a mostrar al editar un usuario existente. 
            Permite editar permisos y fechas importantes.
    """
    list_display = ('rut', 'first_name', 'last_name', 'organismo_sectorial',)
    list_filter = ('is_active', 'organismo_sectorial')
    search_fields = ('rut', 'first_name', 'last_name')
    ordering = ('rut',)

    add_fieldsets = (
        (None, {
            'fields': ('rut', 'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'telefono', 'organismo_sectorial')
        }),
    )

    fieldsets = (
        (None, {
            'fields': ('rut', 'username', 'password', 'first_name', 'last_name', 'email', 'telefono', 'organismo_sectorial')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Reporte. Hereda de `admin.ModelAdmin` para personalizar la interfaz de administración.

    Atributos:
        - list_display: Campos a mostrar en la lista de reportes.
        - list_filter: Filtros disponibles en la barra lateral.
        - search_fields: Campos que se pueden buscar.
        - ordering: Orden predeterminado de los registros.
    """
    list_display = ('fecha', 'unidad_fizcalizable', 'medida')
    list_filter = ('fecha', 'usuario', 'medida')
    search_fields = ('unidad_fizcalizable',)
    ordering = ('-fecha',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Comuna)