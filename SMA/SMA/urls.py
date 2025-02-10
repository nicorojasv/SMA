"""
URL configuration for SMA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from plan.views import PlanViewSet, MedidaViewSet, OrganismoSectorialViewSet, TipoMedidaViewSet, DocumentoViewSet, InformeViewSet, CustomUserViewSet


router = DefaultRouter()

router.register(r'planes', PlanViewSet)
router.register(r'medidas', MedidaViewSet, basename='medida')
router.register(r'organismos_sectoriales', OrganismoSectorialViewSet)
router.register(r'tipo_medidas', TipoMedidaViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'informes', InformeViewSet)
router.register(r'usuarios', CustomUserViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
]
