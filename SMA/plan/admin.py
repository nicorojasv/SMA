from django.contrib import admin
#models
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento,Informe,CustomUser


admin.site.register(Plan)
admin.site.register(Medida)
admin.site.register(OrganismoSectorial)
admin.site.register(TipoMedida)
admin.site.register(Documento)
admin.site.register(Informe)
admin.site.register(CustomUser)
