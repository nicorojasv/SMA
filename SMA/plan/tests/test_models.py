import pytest
from django.core.exceptions import ValidationError
from plan.models import (
    CustomUser, Comuna, OrganismoSectorial, Plan,
    TipoMedida, Medida, Reporte, Documento
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

@pytest.fixture
def reporte(medida, user):
    return Reporte.objects.create(
        fecha="2024-01-01",
        resultado="Resultado test",
        unidad_fizcalizable="Unidad test",
        descripcion="Descripción test",
        usuario=user,
        medida=medida
    )

@pytest.mark.django_db
def test_custom_user_creation():
    user = CustomUser.objects.create_user(
        username="testuser",
        rut="12345678-5",
        telefono="912345678",
        password="testpass123"
    )
    assert user.username == "testuser"
    assert user.rut == "12345678-5"
    assert user.telefono == "912345678"
    assert user.check_password("testpass123")

@pytest.mark.django_db
def test_custom_user_invalid_rut():
    user = CustomUser(
        username="testuser",
        rut="12345678-1",  # RUT inválido
        telefono="912345678",
        password="testpass123"
    )
    with pytest.raises(ValidationError):
        user.full_clean()  # Esto ejecuta las validaciones

@pytest.mark.django_db
def test_custom_user_invalid_phone():
    user = CustomUser(
        username="testuser",
        rut="12345678-5",
        telefono="812345678",  # Teléfono inválido
        password="testpass123"
    )
    with pytest.raises(ValidationError):
        user.full_clean()  # Esto ejecuta las validaciones

@pytest.mark.django_db
def test_plan_creation(plan):
    assert plan.codigo == "PLAN-001"
    assert plan.nombre == "Plan Test"
    assert plan.estado is True

@pytest.mark.django_db
def test_medida_creation(medida):
    assert medida.indicador == "IND-001"
    assert medida.nombre == "Medida Test"
    assert medida.formula_calculo == "x + y"

@pytest.mark.django_db
def test_reporte_creation(reporte):
    assert reporte.resultado == "Resultado test"
    assert reporte.unidad_fizcalizable == "Unidad test"
    assert reporte.medida is not None
    assert reporte.usuario is not None

@pytest.mark.django_db
def test_auditable_model_timestamps(plan):
    assert plan.created_at is not None
    assert plan.updated_at is not None 