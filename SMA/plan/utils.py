import re
from django.core.exceptions import ValidationError

def validate_rut(value): 
    value = value.upper().replace(".", "")

    if not re.match(r'^\d{7,8}-[0-9Kk]$', value):
        raise ValidationError("Formato inválido. Usa el formato: 12345678-5 o 12345678-K")

    try:
        rut, dv = value.split("-")
        dv = dv.strip().upper()  
        rut = rut.strip()
    except ValueError:
        raise ValidationError("Formato inválido. Usa el formato: 12345678-5 o 12345678-K")

    reversed_digits = list(map(int, reversed(rut)))
    factors = [2, 3, 4, 5, 6, 7]
    total = 0
    factor_index = 0

    for d in reversed_digits:
        total += d * factors[factor_index]
        factor_index = (factor_index + 1) % len(factors)

    remainder = 11 - (total % 11)

    if remainder == 11:
        dv_esperado = "0"
    elif remainder == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(remainder)

    # Comparar el dígito verificador calculado con el ingresado
    if dv != dv_esperado:
        raise ValidationError("El RUT no es válido.")
    

def validate_phone(value):
    value = value.strip()
    if not re.match(r'^9\d{8}$', value):
        raise ValidationError("El número telefónico no es válido. Debe comenzar con 9 y tener 9 dígitos.")
    return value