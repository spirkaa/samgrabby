from .common import *  # noqa

SECRET_KEY = env('DJANGO_SECRET_KEY', default='djangolocalsettingssecretkey!123)')

if DEBUG:  # pragma: no cover
    INTERNAL_IPS = type(str("c"), (), {"__contains__": lambda *a: True})()

if DEBUG and DEBUG_TOOLBAR:  # pragma: no cover
    # django-debug-toolbar
    # ------------------------------------------------------------------------------
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": [
            "debug_toolbar.panels.redirects.RedirectsPanel",
        ],
        "SHOW_TEMPLATE_CONTEXT": True,
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
