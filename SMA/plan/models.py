from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import validate_rut, validate_phone
# Create your models here.


class AuditableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario_creador = models.ForeignKey(
        'CustomUser',
        related_name='%(class)s_creados',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

class Plan(AuditableModel):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    fecha_registro = models.DateField()
    comuna = models.ForeignKey(
        'Comuna',
        on_delete=models.CASCADE
    )
    estado = models.BooleanField()

    def __str__(self):
        return f"{self.nombre} {self.codigo} {self.estado}"

class Medida(AuditableModel):
    indicador = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    formula_calculo = models.TextField(
        null=False, 
        blank=False)
    descripcion = models.TextField()
    tipo_medida = models.ForeignKey(
        'TipoMedida',
        on_delete=models.CASCADE
    )
    organismo_sectorial = models.ForeignKey(
        'OrganismoSectorial',
        on_delete=models.CASCADE
        )
    plan = models.ForeignKey(
        'Plan',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f"{self.nombre} {self.descripcion}  {self.plan.nombre} "


class OrganismoSectorial(AuditableModel):
    nombre = models.CharField(max_length=50)
    sigla = models.CharField(max_length=50, unique=True, blank=False)
    descripcion = models.TextField()
    comuna = models.ForeignKey(
        'Comuna',
        on_delete=models.CASCADE
    )
    

    def __str__(self):
        return f"{self.nombre} {self.sigla}"
    
class TipoMedida(AuditableModel):
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.descripcion}"
    

class Documento(AuditableModel):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField(auto_now=True)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    archivo = models.FileField(upload_to='documentos/')
    reporte = models.ForeignKey(
        'Reporte',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.nombre} {self.descripcion} {self.medida.nombre}"
class CustomUser(AbstractUser):
    USERNAME_FIELD = 'rut' #para que los usuarios se logeen con el rut
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] #datos basicos requeridos al crear user por shell
    telefono = models.CharField(max_length=20,validators=[validate_phone], blank=True)
    rut = models.CharField( 
        max_length=12,
        unique=True,
        validators=[validate_rut],  # Validación personalizada
        error_messages={
            'unique': 'Ya existe un usuario con este RUT registrado.'
        }
    )
    organismo_sectorial = models.ForeignKey(
        'OrganismoSectorial',
        on_delete=models.SET_NULL,
        null=True,  # permite que usuarios no tengan organismo
        blank=True  # permite que  sea opcional
    )

class Reporte(AuditableModel):
    fecha = models.DateField()
    resultado = models.TextField()
    unidad_fizcalizable = models.CharField()
    descripcion = models.TextField(null=True)
    usuario = models.ForeignKey(
    'plan.CustomUser',  #hacemos referencia a users, pero desde nuestro custom
    on_delete=models.CASCADE
)
    medida = models.ForeignKey('Medida', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} {self.descripcion} {self.medida.nombre}"
    

class Comuna(models.Model):
    nombre = models.CharField()

    def __str__(self) -> str:
        return f"{self.nombre}"
    