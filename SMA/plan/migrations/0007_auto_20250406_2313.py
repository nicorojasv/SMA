# Generated by Django 5.1.5 on 2025-04-07 03:13

from django.db import migrations

def crear_roles_y_permisos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Crear roles
    admin_sma, creado = Group.objects.get_or_create(name='Administrador')
    fiscalizador_sma, creado = Group.objects.get_or_create(name='Fiscalizador')
    organismo_sectorial, creado = Group.objects.get_or_create(name='Organismo sectorial')

    # Buscar permisos por codename o nombre
    # Permisos del administrador
    permisos_admin = Permission.objects.filter(codename__in=[
        'add_customuser', 'change_customuser', 'delete_customuser', 'view_customuser'
    ])
    # Permisos del fiscalizador
    permisos_fiscalizador = Permission.objects.filter(codename__in=[
        'add_documento', 'change_documento', 'delete_documento', 'view_documento',
        'add_medida', 'change_medida', 'delete_medida', 'view_medida',
        'add_tipomedida', 'change_medida', 'delete_tipomedida', 'view_tipomedida',
        'add_organismosectorial', 'change_organismosectorial', 'delete_organismosectorial', 'view_organismosectorial',
        'add_plan', 'change_plan', 'delete_plan', 'view_plan',
        'add_reporte', 'change_reporte', 'delete_reporte', 'view_reporte',

    ])
    # Permisos del Organismo sectorial
    permisos_organismo_sectorial = Permission.objects.filter(codename__in=[
        'view_medida',
        'view_tipomedida',
        'view_organismosectorial'

    ])

    # Asignar permisos al grupo
    admin_sma.permissions.set(permisos_admin)
    fiscalizador_sma.permissions.set(permisos_fiscalizador)
    organismo_sectorial.permissions.set(permisos_organismo_sectorial)

def borrar_roles(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Administrador').delete()
    Group.objects.filter(name='Fiscalizador').delete()
    Group.objects.filter(name='Organismo sectorial').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0006_alter_customuser_telefono_alter_plan_comuna'),
    ]

    operations = [
        migrations.RunPython(crear_roles_y_permisos, reverse_code=borrar_roles),
    ]
