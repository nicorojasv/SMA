from rest_framework import serializers
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento,Informe,CustomUser

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'

class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'

class TipoMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMedida
        fields = '__all__'

class InformeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informe
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'




        
        