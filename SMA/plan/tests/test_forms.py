import pytest
from plan.forms import CustomUserCreationForm
from plan.models import OrganismoSectorial, Comuna

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
def form_data(organismo_sectorial):
    return {
        'username': 'testuser',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'rut': '12345678-5',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'telefono': '912345678',
        'id_organismo_sectorial': organismo_sectorial.id
    }

@pytest.mark.django_db
def test_custom_user_creation_form_valid(form_data):
    form = CustomUserCreationForm(data=form_data)
    assert form.is_valid()
    assert not form.errors

@pytest.mark.django_db
def test_custom_user_creation_form_missing_required_fields(form_data):
    # Eliminar campos requeridos uno por uno
    for field in ['username', 'rut', 'telefono', 'password1', 'password2']:
        data = form_data.copy()
        del data[field]
        form = CustomUserCreationForm(data=data)
        assert not form.is_valid()
        assert field in form.errors

@pytest.mark.django_db
def test_custom_user_creation_form_password_mismatch(form_data):
    data = form_data.copy()
    data['password2'] = 'differentpass'
    form = CustomUserCreationForm(data=data)
    assert not form.is_valid()
    assert 'password2' in form.errors

@pytest.mark.django_db
def test_custom_user_creation_form_invalid_rut(form_data):
    data = form_data.copy()
    data['rut'] = '12345678-0'  # RUT inválido
    form = CustomUserCreationForm(data=data)
    assert not form.is_valid()
    assert 'rut' in form.errors

@pytest.mark.django_db
def test_custom_user_creation_form_invalid_phone(form_data):
    data = form_data.copy()
    data['telefono'] = '812345678'  # Teléfono inválido
    form = CustomUserCreationForm(data=data)
    assert not form.is_valid()
    assert 'telefono' in form.errors

@pytest.mark.django_db
def test_custom_user_creation_form_optional_organismo(form_data):
    data = form_data.copy()
    data['id_organismo_sectorial'] = None
    form = CustomUserCreationForm(data=data)
    assert form.is_valid()  # El organismo es opcional 