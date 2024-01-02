from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include(("apps.soft.urls", "apps.soft"), namespace="soft")),
    path(settings.ADMIN_URL, admin.site.urls),
]

if settings.DEBUG:  # pragma: no cover
    from django.views import defaults

    urlpatterns += [
        path(
            "400/",
            defaults.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            defaults.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            defaults.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", defaults.server_error),
    ]

    if settings.DEBUG_TOOLBAR:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            path("__reload__/", include("django_browser_reload.urls")),
        ] + urlpatterns
