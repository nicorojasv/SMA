from rest_framework import viewsets
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
    queryset = Medida.objects.all()
    serializer_class = MedidaSerializer

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