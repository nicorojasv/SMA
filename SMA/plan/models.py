from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import validate_rut, validate_phone
# Create your models here.


class AuditableModel(models.Model):
    """
    Modelo abstracto base que agrega campos de auditoría comunes 
    a otros modelos que lo hereden.

    Atributos:
        - created_at (DateTimeField): Fecha y hora en que se creó el registro. Se asigna automáticamente al crear.
        - updated_at (DateTimeField): Fecha y hora de la última modificación del registro. Se actualiza automáticamente.
        - usuario_creador (ForeignKey): Referencia al usuario que creó el registro. Puede ser nulo o quedar en blanco.

    Meta:
        - abstract (bool): Indica que este modelo no se crea como tabla en la base de datos, 
        sino que debe ser heredado por otros modelos.
    """
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
    """
    Modelo que representa un plan en el sistema. Hereda de `AuditableModel`.

    Atributos:
        - codigo (CharField): Código único del plan.
        - nombre (CharField): Nombre del plan.
        - fecha_registro (DateField): Fecha en que se registró el plan.
        - comuna (ForeignKey): Clave foránea que hace referencia a la clase `Comuna`.
        - estado (BooleanField): Indica si el plan está activo o no.
    
    """
    
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
    """
    Modelo que representa una medida dentro de un plan. Hereda de `AuditableModel`.
    
    Atributos:
        - indicador (CharField): Indicador asociado a la medida.
        - nombre (CharField): Nombre de la medida.
        - formula_calculo (TextField): Fórmula para el cálculo de la medida. No puede ser nulo ni estar en blanco.
        - descripcion (TextField): Descripción de la medida.
        - tipo_medida (ForeignKey): Clave foránea que hace referencia a la clase `TipoMedida`.
        - organismo_sectorial (ForeignKey): Clave foránea que hace referencia a la clase `OrganismoSectorial`.
        - plan (ForeignKey): Clave foránea que hace referencia a la clase `Plan`.
    
    """
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
    """
    Modelo que representa un organismo sectorial. Hereda de `AuditableModel`.

    Atributos:
        - nombre (CharField): Nombre del organismo sectorial.
        - sigla (CharField): Sigla única del organismo sectorial. No puede estar en blanco.
        - descripcion (TextField): Descripción del organismo sectorial.
        - comuna (ForeignKey): Clave foránea que hace referencia a la clase `Comuna`.
    """
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
    """
    Modelo que representa un tipo de medida. Hereda de `AuditableModel`.

    Atributos:
        - nombre (CharField): Nombre del tipo de medida. No puede ser nulo.
        - descripcion (TextField): Descripción del tipo de medida.
    """
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.descripcion}"
    

class Documento(AuditableModel):
    """
    Modelo que representa un documento asociado a un reporte. Hereda de `AuditableModel`.

    Atributos:
        - nombre (CharField): Nombre del documento.
        - fecha (DateField): Fecha de creación del documento. Se asigna automáticamente al crear.
        - descripcion (TextField): Descripción del documento.
        - estado (BooleanField): Indica si el documento está activo o no.
        - archivo (FileField): Archivo del documento. Se sube a la carpeta 'documentos/'.
        - reporte (ForeignKey): Clave foránea que hace referencia a la clase `Reporte`.
    """
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
    """
    Modelo de usuario personalizado que extiende el modelo de usuario de Django. Hereda de `AbstractUser`.
    
    Atributos:
        - telefono (CharField): Número de teléfono del usuario. Puede estar en blanco.
        - rut (CharField): RUT del usuario. Debe ser único.
        - organismo_sectorial (ForeignKey): Clave foránea que hace referencia a la clase `OrganismoSectorial`. Puede ser nulo o estar en blanco.
    """
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
    """
    Modelo que representa un reporte asociado a una medida. Hereda de `AuditableModel`.

    Atributos:
        - fecha (DateField): Fecha del reporte.
        - resultado (TextField): Resultado del reporte.
        - unidad_fizcalizable (CharField): Unidad de fiscalización asociada al reporte.
        - descripcion (TextField): Descripción del reporte. Puede ser nula.
        - usuario (ForeignKey): Clave foránea que hace referencia a la clase `CustomUser`.
        - medida (ForeignKey): Clave foránea que hace referencia a la clase `Medida`.
    """
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
    """
    Modelo que representa una comuna. Hereda de `models.Model`.
    
    Atributos:
        - nombre (CharField): Nombre de la comuna.
    """
    nombre = models.CharField()

    def __str__(self) -> str:
        return f"{self.nombre}"
    