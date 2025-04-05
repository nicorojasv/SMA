from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Plan(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    fecha_registro = models.DateField()
    comuna = models.CharField(max_length=50)
    estado = models.BooleanField()

    def __str__(self):
        return f"{self.nombre} {self.codigo} {self.estado}"

class Medida(models.Model):
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


class OrganismoSectorial(models.Model):
    nombre = models.CharField(max_length=50)
    sigla = models.CharField(max_length=50, unique=True, blank=False)
    descripcion = models.TextField()
    

    def __str__(self):
        return f"{self.nombre} {self.sigla}"
    
class TipoMedida(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.descripcion}"
    

class Documento(models.Model):
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
    telefono = models.CharField()
    rut = models.CharField( 
        max_length=12,
        unique=True,
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

class Reporte(models.Model):
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