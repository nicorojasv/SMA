from rest_framework import serializers
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento, Reporte, CustomUser
from .utils import validate_rut, validate_phone

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        extra_kwargs = {
            'codigo': {'error_messages': {'blank': 'El código del plan no puede estar vacío'}},
            'nombre': {'error_messages': {'blank': 'El nombre del plan no puede estar vacío'}},
            'estado': {'error_messages': {'null': 'El estado es requerido'}},
            'comuna': {'error_messages': {'null': 'La comuna es requerida'}},
        }
    
    def validate_codigo(self, value):
        if not value.strip():
            raise serializers.ValidationError("El código del plan no puede estar vacío")
        if len(value) > 50:
            raise serializers.ValidationError("El código del plan no puede exceder los 50 caracteres")
        return value
    
    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre del plan no puede estar vacío")
        if len(value) > 50:
            raise serializers.ValidationError("El nombre del plan no puede exceder los 50 caracteres")
        return value
    
    def validate_fecha_registro(self, value):
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("La fecha de registro del plan no puede ser superior a la fecha actual")
        return value
    
    def validate(self, data):
        if data.get('estado') is None:
            raise serializers.ValidationError("El estado es requerido")
        if not data.get('comuna'):
            raise serializers.ValidationError("La comuna es requerida")
        return data

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'
        extra_kwargs = {
            'indicador': {'error_messages': {'blank': 'El indicador no puede estar vacío'}},
            'nombre': {'error_messages': {'blank': 'El nombre no puede estar vacío'}},
            'formula_calculo': {'error_messages': {'blank': 'La fórmula de cálculo no puede estar vacía'}},
            'descripcion': {'error_messages': {'blank': 'La descripción no puede estar vacía'}},
            'tipo_medida': {'error_messages': {'null': 'El tipo de medida es requerido'}},
            'organismo_sectorial': {'error_messages': {'null': 'El organismo sectorial es requerido'}},
            'plan': {'error_messages': {'null': 'El plan es requerido'}},
        }
    
    def validate_indicador(self, value):
        if not value.strip():
            raise serializers.ValidationError("El indicador no puede estar vacío")
        if len(value) > 100:
            raise serializers.ValidationError("El indicador no puede exceder los 100 caracteres")
        return value
    
    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        if len(value) > 100:
            raise serializers.ValidationError("El nombre no puede exceder los 100 caracteres")
        return value
    
    def validate_formula_calculo(self, value):
        if not value.strip():
            raise serializers.ValidationError("La fórmula de cálculo no puede estar vacía")
        return value
    
    def validate_descripcion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La descripción no puede estar vacía")
        return value
    
    def validate(self, data):
        if not data.get('tipo_medida'):
            raise serializers.ValidationError("El tipo de medida es requerido")
        if not data.get('organismo_sectorial'):
            raise serializers.ValidationError("El organismo sectorial es requerido")
        if not data.get('plan'):
            raise serializers.ValidationError("El plan es requerido")
        return data

class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = '__all__'
        extra_kwargs = {
            'nombre': {'error_messages': {'blank': 'El nombre no puede estar vacío'}},
            'sigla': {'error_messages': {'blank': 'La sigla no puede estar vacía'}},
            'descripcion': {'error_messages': {'blank': 'La descripción no puede estar vacía'}},
            'comuna': {'error_messages': {'null': 'La comuna es requerida'}},
        }
    
    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        if len(value) > 50:
            raise serializers.ValidationError("El nombre no puede exceder los 50 caracteres")
        return value
    
    def validate_sigla(self, value):
        if not value.strip():
            raise serializers.ValidationError("La sigla no puede estar vacía")
        if len(value) > 50:
            raise serializers.ValidationError("La sigla no puede exceder los 50 caracteres")
        return value
    
    def validate_descripcion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La descripción no puede estar vacía")
        return value
    
    def validate(self, data):
        if not data.get('comuna'):
            raise serializers.ValidationError("La comuna es requerida")
        return data

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
        extra_kwargs = {
            'nombre': {'error_messages': {'blank': 'El nombre no puede estar vacío'}},
            'descripcion': {'error_messages': {'blank': 'La descripción no puede estar vacía'}},
            'archivo': {'error_messages': {'blank': 'Debe proporcionar un archivo'}},
            'reporte': {'error_messages': {'null': 'El reporte es requerido'}},
        }
    
    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        # La longitud máxima ya está manejada por el modelo (max_length=50)
        if len(value) > 50:
            raise serializers.ValidationError("El nombre no puede exceder los 50 caracteres")
        return value
    
    def validate_descripcion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La descripción no puede estar vacía")
        return value
    
    def validate_archivo(self, value):
        if not value:
            raise serializers.ValidationError("Debe proporcionar un archivo")
        allowed_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png']
        ext = value.name.lower()
        if not any(ext.endswith(e) for e in allowed_extensions):
            raise serializers.ValidationError("Formato de archivo no permitido. Use: PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG, PNG")
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("El archivo no puede ser mayor a 10MB")
        return value
    
    def validate(self, data):
        if not data.get('reporte'):
            raise serializers.ValidationError("El reporte es requerido")
        return data

class TipoMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMedida
        fields = '__all__'
        extra_kwargs = {
            'nombre': {'error_messages': {'blank': 'El nombre no puede estar vacío'}},
            'descripcion': {'error_messages': {'blank': 'La descripción no puede estar vacía'}},
        }
    
    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        if len(value) > 50:
            raise serializers.ValidationError("El nombre no puede exceder los 50 caracteres")
        return value
    
    def validate_descripcion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La descripción no puede estar vacía")
        return value

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'
        extra_kwargs = {
            'resultado': {'error_messages': {'blank': 'El resultado no puede estar vacío'}},
            'unidad_fizcalizable': {'error_messages': {'blank': 'La unidad fiscalizable no puede estar vacía'}},
            'medida': {'error_messages': {'null': 'La medida es requerida'}},
            'usuario': {'error_messages': {'null': 'El usuario es requerido'}},
        }
    
    def validate_fecha(self, value):
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("La fecha no puede ser futura")
        return value
    
    def validate_resultado(self, value):
        if not value.strip():
            raise serializers.ValidationError("El resultado no puede estar vacío")
        return value
    
    def validate_unidad_fizcalizable(self, value):
        if not value.strip():
            raise serializers.ValidationError("La unidad fiscalizable no puede estar vacía")
        return value
    
    def validate(self, data):
        if not data.get('medida'):
            raise serializers.ValidationError("La medida es requerida")
        if not data.get('usuario'):
            raise serializers.ValidationError("El usuario es requerido")
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'rut': {'error_messages': {'blank': 'El RUT no puede estar vacío'}},
            'telefono': {'error_messages': {'blank': 'El teléfono no puede estar vacío'}},
            'email': {'error_messages': {'blank': 'El email no puede estar vacío'}},
            'username': {'error_messages': {'blank': 'El nombre de usuario no puede estar vacío'}},
            'first_name': {'error_messages': {'blank': 'El nombre no puede estar vacío'}},
            'last_name': {'error_messages': {'blank': 'El apellido no puede estar vacío'}},
        }
    
    def validate_rut(self, value):
        try:
            validate_rut(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def validate_telefono(self, value):
        try:
            validate_phone(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def validate_email(self, value):
        if not value.strip():
            raise serializers.ValidationError("El email no puede estar vacío")
        return value
    
    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre de usuario no puede estar vacío")
        return value
    
    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value
    
    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido no puede estar vacío")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user