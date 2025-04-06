import pytest
from django.urls import reverse
from django.test import Client
from plan.models import CustomUser, OrganismoSectorial, Comuna
from plan.forms import CustomUserCreationForm

@pytest.fixture
def client():
    return Client()

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
def user_data(organismo_sectorial):
    return {
        'username': 'testuser',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'rut': '12345678-5',  # RUT válido
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'telefono': '912345678',  # Teléfono válido (comienza con 9 y tiene 9 dígitos)
        'id_organismo_sectorial': organismo_sectorial.id
    }

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'home.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_signup_view_get(client):
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assert 'signup.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], CustomUserCreationForm)

@pytest.mark.django_db
def test_signup_view_post_success(client, user_data):
    response = client.post(reverse('signup'), user_data)
    # Verificamos que el usuario se haya creado
    assert CustomUser.objects.filter(rut=user_data['rut']).exists()
    # Verificamos que se redirija a home
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_signup_view_post_duplicate_rut(client, user_data):
    # Crear un usuario primero
    CustomUser.objects.create_user(
        username='existinguser',
        rut=user_data['rut'],
        password='testpass123'
    )
    
    response = client.post(reverse('signup'), user_data)
    assert response.status_code == 200
    assert 'signup.html' in [t.name for t in response.templates]
    # Verificamos que el formulario tenga errores
    assert response.context['form'].errors

@pytest.mark.django_db
def test_signin_view_get(client):
    response = client.get(reverse('signin'))
    assert response.status_code == 200
    assert 'signin.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_signin_view_post_success(client, user_data):
    # Crear usuario primero
    user = CustomUser.objects.create_user(
        username=user_data['username'],
        rut=user_data['rut'],
        password=user_data['password1']
    )
    
    response = client.post(reverse('signin'), {
        'username': user_data['rut'],  # Usamos el RUT en lugar del username
        'password': user_data['password1']
    })
    # Verificamos que se redirija a home
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_signin_view_post_invalid_credentials(client):
    response = client.post(reverse('signin'), {
        'username': 'nonexistent',
        'password': 'wrongpass'
    })
    assert response.status_code == 200
    assert 'signin.html' in [t.name for t in response.templates]
    assert 'El usuario o password es incorrecto' in str(response.content)

@pytest.mark.django_db
def test_panel_sma_view_requires_login(client):
    response = client.get(reverse('panel_sma'))
    assert response.status_code == 302
    # Verificamos que redirija a la página de login
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
def test_panel_sma_view_with_login(client, user_data):
    # Crear y loguear usuario
    user = CustomUser.objects.create_user(
        username=user_data['username'],
        rut=user_data['rut'],
        password=user_data['password1']
    )
    client.force_login(user)
    
    response = client.get(reverse('panel_sma'))
    assert response.status_code == 200
    assert 'panel_sma.html' in [t.name for t in response.templates] 