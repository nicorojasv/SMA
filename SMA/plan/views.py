from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento, Informe, CustomUser
from plan.serializers import (
    PlanSerializer, 
    MedidaSerializer, 
    OrganismoSectorialSerializer,
    TipoMedidaSerializer, 
    DocumentoSerializer, 
    InformeSerializer, 
    CustomUserSerializer
)

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class MedidaViewSet(viewsets.ModelViewSet):
    serializer_class = MedidaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        usuario = self.request.user
        
        # Si el usuario es superuser, retorna todas las medidas
        if usuario.is_superuser:
            return Medida.objects.all()
            
        # Si el usuario tiene un organismo sectorial asignado
        if usuario.id_organismo_sectorial:
            return Medida.objects.filter(
                id_organismo_sectorial=usuario.id_organismo_sectorial
            )
        
        # Si el usuario no tiene organismo y no es superuser
        return Medida.objects.none()
class OrganismoSectorialViewSet(viewsets.ModelViewSet):
    queryset = OrganismoSectorial.objects.all()
    serializer_class = OrganismoSectorialSerializer

class TipoMedidaViewSet(viewsets.ModelViewSet):
    queryset = TipoMedida.objects.all()
    serializer_class = TipoMedidaSerializer

    def validate_nombre(self, value):
        if not value:
            raise serializers.ValidationError("El campo nombre es Obligatorio ")
        return value

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class InformeViewSet(viewsets.ModelViewSet):
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer