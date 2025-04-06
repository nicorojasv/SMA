from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento, Reporte, CustomUser
from plan.serializers import (
    PlanSerializer, 
    MedidaSerializer, 
    OrganismoSectorialSerializer,
    TipoMedidaSerializer, 
    DocumentoSerializer, 
    ReporteSerializer, 
    CustomUserSerializer
)
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.models import User
from plan.models import CustomUser
from plan.forms import CustomUserCreationForm
from psycopg2 import errors


def home(request):
    """
    Vista principal de la aplicación.
    
    Returns:
        HttpResponse: Renderiza la plantilla home.html
    """
    return render(request, 'home.html')

def signup(request):
    """
    Vista para el registro de nuevos usuarios.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: 
            - Si GET: Renderiza el formulario de registro
            - Si POST: Procesa el registro y redirige a home si es exitoso
    """
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": CustomUserCreationForm()})
    else:
        form = CustomUserCreationForm(request.POST)
        print("Formulario válido")
        if form.is_valid():
            
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError as e:
                # Verifica si el error es por RUT duplicado
                if 'unique constraint' in str(e) and 'rut' in str(e):
                    form.add_error('rut', 'Este RUT ya está registrado.')
                # Verifica si el error es por usuario duplicado
                elif 'unique constraint' in str(e) and 'username' in str(e):
                    form.add_error('username', 'Este nombre de usuario ya existe.')
                else:
                    form.add_error(None, f"Error de base de datos: {e}")

            except errors.UniqueViolation as e:
                form.add_error(None, f"Violación de unicidad: {e}")

            except Exception as e:
                form.add_error(None, f"Error inesperado: {str(e)}")

        return render(request, 'signup.html', {"form": form})
    

    
def signin(request):
    """
    Vista para el inicio de sesión de usuarios.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: 
            - Si GET: Renderiza el formulario de inicio de sesión
            - Si POST: Procesa el inicio de sesión y redirige a home si es exitoso
    """
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm(), "error": "El usuario o password es incorrecto."})

        login(request, user)
        return redirect('home')

@login_required
def signout(request):
    """
    Vista para cerrar sesión.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponseRedirect: Redirige a la página principal
    """
    logout(request)
    return redirect('home')
@login_required
def panel_sma(request):
    """
    Vista del panel de administración SMA.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Renderiza la plantilla panel_sma.html
    """
    return render(request, 'panel_sma.html')

class PlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar planes.
    
    Permisos:
        - Requiere autenticación
    """
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class MedidaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar medidas.
    
    Permisos:
        - Requiere autenticación
        - Los usuarios solo ven las medidas de su organismo sectorial
        - Los superusuarios ven todas las medidas
    """
    serializer_class = MedidaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        usuario = self.request.user
        
        # Si el usuario es superuser, retorna todas las medidas
        if usuario.is_superuser:
            return Medida.objects.all()
            
        # Si el usuario tiene un organismo sectorial asignado
        if usuario.id_organismo_sectorial:
            return Medida.objects.filter(
                id_organismo_sectorial=usuario.id_organismo_sectorial
            )
        
        # Si el usuario no tiene organismo y no es superuser
        return Medida.objects.none()
class OrganismoSectorialViewSet(viewsets.ModelViewSet): 
    """
    API endpoint que permite ver y editar organismos sectoriales.
    
    Permisos:
        - Requiere ser administrador
    """
    permission_classes = [IsAdminUser]
    queryset = OrganismoSectorial.objects.all()
    serializer_class = OrganismoSectorialSerializer

class TipoMedidaViewSet(viewsets.ModelViewSet): 
    """
    API endpoint que permite ver y editar tipos de medidas.
    
    Permisos:
        - Requiere ser administrador
    """
    permission_classes = [IsAdminUser]
    queryset = TipoMedida.objects.all()
    serializer_class = TipoMedidaSerializer

class DocumentoViewSet(viewsets.ModelViewSet): 
    """
    API endpoint que permite ver y editar documentos.
    
    Permisos:
        - Requiere autenticación
    """
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class ReporteViewSet(viewsets.ModelViewSet): 
    """
    API endpoint que permite ver y editar reportes.
    
    Permisos:
        - Requiere autenticación
    """
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer

class CustomUserViewSet(viewsets.ModelViewSet): 
    """
    API endpoint que permite ver y editar usuarios personalizados.
    
    Permisos:
        - Requiere autenticación
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer