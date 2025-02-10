from rest_framework import viewsets
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
class OrganismoSectorialViewSet(viewsets.ModelViewSet):  # Cambiado de MethodMapper
    queryset = OrganismoSectorial.objects.all()
    serializer_class = OrganismoSectorialSerializer

class TipoMedidaViewSet(viewsets.ModelViewSet):  # Cambiado de MethodMapper
    queryset = TipoMedida.objects.all()
    serializer_class = TipoMedidaSerializer

class DocumentoViewSet(viewsets.ModelViewSet):  # Cambiado de MethodMapper
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class InformeViewSet(viewsets.ModelViewSet):  # Cambiado de MethodMapper
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer

class CustomUserViewSet(viewsets.ModelViewSet):  # Cambiado de MethodMapper
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer