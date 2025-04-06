from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento, CustomUser, Reporte

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'fecha_registro', 'comuna', 'estado')
    list_filter = ('fecha_registro', 'codigo')
    search_fields = ('codigo', 'nombre', 'comuna')
    ordering = ('-fecha_registro',)
    list_per_page = 20

@admin.register(Medida)
class MedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'indicador', 'plan', 'organismo_sectorial')
    list_filter = ('organismo_sectorial', 'plan')
    search_fields = ('nombre',)

@admin.register(OrganismoSectorial)
class OrganismoSectorialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sigla')
    search_fields = ('nombre', 'sigla')
    ordering = ('nombre',)

@admin.register(TipoMedida)
class TipoMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'reporte')
    list_filter = ('reporte', 'fecha')
    search_fields = ('nombre',)

class CustomUserAdmin(UserAdmin):
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
    list_display = ('fecha', 'unidad_fizcalizable', 'medida')
    list_filter = ('fecha', 'usuario', 'medida')
    search_fields = ('unidad_fizcalizable',)
    ordering = ('-fecha',)

admin.site.register(CustomUser, CustomUserAdmin)