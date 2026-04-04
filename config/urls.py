from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("", include("apps.dashboards.urls")),
    path("", include("apps.doacoes.urls")),
    path("", include("apps.usuarios.urls")),
]
