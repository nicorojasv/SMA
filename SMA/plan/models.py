from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Plan(models.Model):
    id_plan = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    fecha_registro = models.DateField()
    comuna = models.CharField(max_length=50)
    estado = models.BooleanField()

    def __str__(self):
        return f"{self.nombre} {self.codigo} {self.estado}"

class Medida(models.Model):
    id_medida = models.AutoField(primary_key=True)
    indicador = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    formula_calculo = models.TextField()
    descripcion = models.TextField()
    id_tipo_medida = models.ForeignKey(
        'TipoMedida',
        on_delete=models.CASCADE
    )
    id_organismo_sectorial = models.ForeignKey(
        'OrganismoSectorial',
        on_delete=models.CASCADE
        )
    id_plan = models.ForeignKey(
        'Plan',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f"{self.nombre} {self.descripcion}  {self.id_plan.nombre} "


class OrganismoSectorial(models.Model):
    id_organismo_sectorial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    sigla = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.sigla}"
    
class TipoMedida(models.Model):
    id_tipo_medida = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.descripcion}"
    

class Documento(models.Model):
    id_documento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    archivo = models.FileField(upload_to='documentos/')
    id_informe = models.ForeignKey(
        'Informe',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.nombre} {self.descripcion} {self.id_medida.nombre}"
class CustomUser(AbstractUser):
    USERNAME_FIELD = 'rut' #para que los usuarios se logeen con el rut
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] #datos basicos requeridos al crear user por shell


    rut = models.CharField( 
        max_length=12,
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este RUT registrado.'
        }
    )
    id_organismo_sectorial = models.ForeignKey(
        'OrganismoSectorial',
        on_delete=models.SET_NULL,
        null=True,  # permite que usuarios no tengan organismo
        blank=True  # permite que  sea opcional
    )

class Informe(models.Model):
    id_informe = models.AutoField(primary_key=True)
    fecha = models.DateField()
    resultado = models.TextField()
    id_usuario = models.ForeignKey(
    'plan.CustomUser',  #hacemos referencia a users, pero desde nuestro custom
    on_delete=models.CASCADE
)
    id_medida = models.ForeignKey('Medida', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} {self.descripcion} {self.id_medida.nombre}"