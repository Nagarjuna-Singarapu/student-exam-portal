from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from exam.views import health_view, RegisterView, TemplateIndexRedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

    # health check
    path("api/health/", health_view, name="health"),

    # auth: register (view) + JWT token obtain/refresh
    path("api/auth/register/", RegisterView.as_view(), name="api_register"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # exam app API & template urls
    path("api/exam/", include("exam.urls_api")),      # API endpoints
    path("", include("exam.urls_templates")),         # template pages for validation
]
