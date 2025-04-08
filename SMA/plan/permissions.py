from rest_framework.permissions import BasePermission

class EsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Administrador').exists()

class EsFiscalizador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Fiscalizador').exists()

class EsOrganismoSectorial(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Organismo sectorial').exists()
