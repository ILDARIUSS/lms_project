from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import CustomTokenObtainPairView


schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version='v1',
        description="Документация LMS проекта",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@lms.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('materials.urls')),
    path('api/users/', include('users.urls')),

    # 🔥 ДОКУМЕНТАЦИЯ
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)