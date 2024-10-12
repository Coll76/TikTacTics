"""Tiktaktiks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
#from rest_framework.schemas import get_schema_view #new
#from rest_framework_swagger.views import get_swagger_view # new
from rest_framework import permissions #new
from drf_yasg.views import get_schema_view #new
from drf_yasg import openapi #new
from django.urls import path, include #new
from django.conf import settings
#API_TITLE = 'Tiktaktiks API'
#schema_view = get_swagger_view(title=API_TITLE) # new

schema_view = get_schema_view(
    openapi.Info(
        title="Tiktaktiks API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="collins.kubu@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('PhishingSolution.urls')),
    #path('__debug__/', include('debug_toolbar.urls')),
    #path('schema/', schema_view), # new
    #path('swagger-docs/', schema_view), # new

    #new
    #path('api/v1/auth/', include('dj_rest_auth.urls')),  # Login, Logout, Password Reset
    #path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
