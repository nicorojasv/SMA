from rest_framework.permissions import BasePermission

class EsAdministrador(BasePermission):
    """
    Permiso para verificar si el usuario pertenece al grupo 'Administrador'.

    """
    def has_permission(self, request, view):
        """
        Determina si el usuario tiene permiso para acceder a la vista especificada.

        Args:
            - request (HttpRequest): La solicitud HTTP actual.
            - view (APIView): La vista a la que se está intentando acceder.
        
        Returns:
            - bool: True si el usuario está autenticado y pertenece al grupo 'Administrador',
                  False en caso contrario.
        """
        return request.user and request.user.groups.filter(name='Administrador').exists()

class EsFiscalizador(BasePermission):
    """
    Permiso para verificar si el usuario pertenece al grupo 'Fiscalizador'.

    """
    def has_permission(self, request, view):
        """
        Determina si el usuario tiene permiso para acceder a la vista especificada.

        Args:
            - request (HttpRequest): La solicitud HTTP actual.
            - view (APIView): La vista a la que se está intentando acceder.    
        Returns:
            - bool: True si el usuario está autenticado y pertenece al grupo 'Fiscalizador',
                  False en caso contrario. 
        """
        return request.user and request.user.groups.filter(name='Fiscalizador').exists()

class EsOrganismoSectorial(BasePermission):
    """
    Permiso para verificar si el usuario pertenece al grupo 'Organismo sectorial'.
    
    """
    def has_permission(self, request, view):
        """
        Determina si el usuario tiene permiso para acceder a la vista especificada.

        Args:
            - request (HttpRequest): La solicitud HTTP actual.
            - view (APIView): La vista a la que se está intentando acceder.
        
        Returns:
            - bool: True si el usuario está autenticado y pertenece al grupo 'Organismo sectorial',
                  False en caso contrario.
        """
        return request.user and request.user.groups.filter(name='Organismo sectorial').exists()
