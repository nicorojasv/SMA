import pytest
from plan.serializers import (
    PlanSerializer, MedidaSerializer, OrganismoSectorialSerializer,
    TipoMedidaSerializer, CustomUserSerializer
)
from plan.models import (
    Plan, Medida, OrganismoSectorial, TipoMedida,
    CustomUser, Comuna
)

@pytest.fixture
def comuna():
    return Comuna.objects.create(nombre="Santiago")

@pytest.fixture
def organismo_sectorial(comuna):
    return OrganismoSectorial.objects.create(
        nombre="Ministerio de Salud",
        sigla="MINSAL",
        descripcion="Ministerio de Salud de Chile",
        comuna=comuna
    )

@pytest.fixture
def tipo_medida():
    return TipoMedida.objects.create(
        nombre="Tipo de Medida Test",
        descripcion="Descripción del tipo de medida"
    )

@pytest.fixture
def plan(organismo_sectorial):
    return Plan.objects.create(
        codigo="PLAN-001",
        nombre="Plan Test",
        fecha_registro="2024-01-01",
        comuna=comuna,
        estado=True
    )

@pytest.fixture
def medida(plan, tipo_medida, organismo_sectorial):
    return Medida.objects.create(
        indicador="IND-001",
        nombre="Medida Test",
        formula_calculo="x + y",
        descripcion="Descripción de la medida",
        tipo_medida=tipo_medida,
        organismo_sectorial=organismo_sectorial,
        plan=plan
    )

@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        username="testuser",
        rut="12345678-5",
        telefono="912345678",
        password="testpass123"
    )

@pytest.mark.django_db
def test_plan_serializer(plan):
    serializer = PlanSerializer(plan)
    data = serializer.data
    assert data['codigo'] == "PLAN-001"
    assert data['nombre'] == "Plan Test"
    assert data['estado'] is True

@pytest.mark.django_db
def test_medida_serializer(medida):
    serializer = MedidaSerializer(medida)
    data = serializer.data
    assert data['indicador'] == "IND-001"
    assert data['nombre'] == "Medida Test"
    assert data['formula_calculo'] == "x + y"

@pytest.mark.django_db
def test_organismo_sectorial_serializer(organismo_sectorial):
    serializer = OrganismoSectorialSerializer(organismo_sectorial)
    data = serializer.data
    assert data['nombre'] == "Ministerio de Salud"
    assert data['sigla'] == "MINSAL"

@pytest.mark.django_db
def test_tipo_medida_serializer(tipo_medida):
    serializer = TipoMedidaSerializer(tipo_medida)
    data = serializer.data
    assert data['nombre'] == "Tipo de Medida Test"
    assert data['descripcion'] == "Descripción del tipo de medida"

@pytest.mark.django_db
def test_custom_user_serializer(user):
    serializer = CustomUserSerializer(user)
    data = serializer.data
    assert data['username'] == "testuser"
    assert data['rut'] == "12345678-5"
    assert data['telefono'] == "912345678"

@pytest.mark.django_db
def test_plan_serializer_create(organismo_sectorial):
    data = {
        'codigo': 'PLAN-002',
        'nombre': 'Nuevo Plan',
        'fecha_registro': '2024-01-01',
        'estado': True
    }
    serializer = PlanSerializer(data=data)
    assert serializer.is_valid()
    plan = serializer.save()
    assert plan.codigo == 'PLAN-002'
    assert plan.nombre == 'Nuevo Plan'

@pytest.mark.django_db
def test_medida_serializer_create(plan, tipo_medida, organismo_sectorial):
    data = {
        'indicador': 'IND-002',
        'nombre': 'Nueva Medida',
        'formula_calculo': 'x * y',
        'descripcion': 'Nueva descripción',
        'tipo_medida': tipo_medida.id,
        'organismo_sectorial': organismo_sectorial.id,
        'plan': plan.id
    }
    serializer = MedidaSerializer(data=data)
    assert serializer.is_valid()
    medida = serializer.save()
    assert medida.indicador == 'IND-002'
    assert medida.nombre == 'Nueva Medida' 