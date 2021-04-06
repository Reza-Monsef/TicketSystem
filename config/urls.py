from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

DOCS_TITLE = 'Ticket API'
DOCS_DESCRIPTION = 'documentation created by core api'

schema_view = get_schema_view(
    openapi.Info(
        title="Ticket API",
        default_version='v1',
        description="documentation ticket api by swagger",
    ),
    permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('', include('ticket.urls')),
    path('api/schema/', get_schema_view(DOCS_TITLE)),
    path('api/docs/', include_docs_urls(title=DOCS_TITLE,
         description=DOCS_DESCRIPTION)),
    path('api/swagger(?P<format>\.json|\.yaml)',
         schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger',
                                             cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc',
                                           cache_timeout=0), name='schema-redoc'),
]
