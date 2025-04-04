from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Plan, Medida, OrganismoSectorial, TipoMedida, Documento, Informe, CustomUser
from plan.serializers import (
    PlanSerializer, 
    MedidaSerializer, 
    OrganismoSectorialSerializer,
    TipoMedidaSerializer, 
    DocumentoSerializer, 
    InformeSerializer, 
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
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": CustomUserCreationForm()})
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.telefono = form.cleaned_data['telefono']
                user.rut = form.cleaned_data['rut']
                #user.id_organismo_sectorial = form.cleaned_data['id_organismo_sectorial']
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
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm(), "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')
@login_required
def panel_sma(request):
    return render(request, 'panel_sma.html')

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class MedidaViewSet(viewsets.ModelViewSet):
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
    permission_classes = [IsAdminUser]
    queryset = OrganismoSectorial.objects.all()
    serializer_class = OrganismoSectorialSerializer

class TipoMedidaViewSet(viewsets.ModelViewSet): 

    permission_classes = [IsAdminUser]
    queryset = TipoMedida.objects.all()
    serializer_class = TipoMedidaSerializer

class DocumentoViewSet(viewsets.ModelViewSet): 
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class InformeViewSet(viewsets.ModelViewSet): 
    queryset = Informe.objects.all()
    serializer_class = InformeSerializer

class CustomUserViewSet(viewsets.ModelViewSet): 
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer