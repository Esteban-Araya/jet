"""jet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from apps.Users.urls import router as routerUsers
from apps.Devices.urls import router as routerDevices
from apps.Record.urls import router as routerRecord
from rest_framework.routers import DefaultRouter

# Crea un nuevo router
router = DefaultRouter()


router.registry.extend(routerUsers.registry)
router.registry.extend(routerRecord.registry)
router.registry.extend(routerDevices.registry)


schema_view = get_schema_view(
   openapi.Info(
      title="Jet API",
      default_version='v1',
      description="api",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jetiot@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path("",include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


