from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento, CustomUser, Informe

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'fecha_registro', 'comuna', 'estado')
    list_filter = ('fecha_registro', 'codigo')
    search_fields = ('codigo', 'nombre', 'comuna')
    ordering = ('-fecha_registro',)
    list_per_page = 20

@admin.register(Medida)
class MedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'indicador', 'id_plan', 'id_organismo_sectorial')
    list_filter = ( 'id_organismo_sectorial', 'id_plan')
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
    list_display = ('nombre', 'fecha', 'id_informe')
    list_filter = ('id_informe', 'fecha')
    search_fields = ('nombre', )

class CustomUserAdmin(UserAdmin):
    list_display = ('rut',  'first_name', 'last_name', 'id_organismo_sectorial',)
    list_filter = ('is_active', 'id_organismo_sectorial')
    search_fields = ('rut', 'first_name', 'last_name')
    ordering = ('rut',)
   

@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'unidad_fizcalizable', 'id_medida')
    list_filter = ('fecha', 'id_usuario', 'id_medida')
    search_fields = ('unidad_fizcalizable', 'id_medida', )
    ordering = ('-fecha',)

admin.site.register(CustomUser, CustomUserAdmin)