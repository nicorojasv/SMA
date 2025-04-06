import pytest
from django.core.exceptions import ValidationError
from plan.utils import validate_rut, validate_phone

def test_validate_rut_valid():
    # RUT válido
    validate_rut('12345678-5')  # RUT válido con DV 5
    validate_rut('12.345.678-5')  # Con puntos

def test_validate_rut_invalid_format():
    # Formatos inválidos
    with pytest.raises(ValidationError, match="Formato inválido"):
        validate_rut('12345678')  # Sin guión
    with pytest.raises(ValidationError, match="Formato inválido"):
        validate_rut('12345678-')  # Sin dígito verificador
    with pytest.raises(ValidationError, match="Formato inválido"):
        validate_rut('12345678-12')  # Dígito verificador muy largo

def test_validate_rut_invalid_dv():
    # Dígitos verificadores inválidos
    with pytest.raises(ValidationError, match="El RUT no es válido"):
        validate_rut('12345678-1')  # DV incorrecto
    with pytest.raises(ValidationError, match="El RUT no es válido"):
        validate_rut('12345678-2')  # DV incorrecto

def test_validate_phone_valid():
    # Teléfonos válidos
    assert validate_phone('912345678') == '912345678'
    assert validate_phone(' 912345678 ') == '912345678'  # Con espacios

def test_validate_phone_invalid():
    # Teléfonos inválidos
    with pytest.raises(ValidationError, match="El número telefónico no es válido"):
        validate_phone('812345678')  # No comienza con 9
    with pytest.raises(ValidationError, match="El número telefónico no es válido"):
        validate_phone('91234567')  # Muy corto
    with pytest.raises(ValidationError, match="El número telefónico no es válido"):
        validate_phone('9123456789')  # Muy largo 