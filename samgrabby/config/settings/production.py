from .common import *  # noqa

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
POD_IP = env.str("POD_IP", default=None)
if POD_IP:
    ALLOWED_HOSTS.append(POD_IP)

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

INSTALLED_APPS += ["gunicorn"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy
USE_X_FORWARDED_HOST = env.bool("DJANGO_USE_X_FORWARDED_HOST", default=False)
SECURE_PROXY_SSL_HEADER = env.tuple(
    "DJNAGO_SECURE_PROXY_SSL_HEADER", default=("HTTP_X_FORWARDED_PROTO", "https")
)
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
SECURE_BROWSER_XSS_FILTER = env.bool("DJANGO_SECURE_BROWSER_XSS_FILTER", default=True)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
SESSION_COOKIE_HTTPONLY = env.bool("DJANGO_SESSION_COOKIE_HTTPONLY", default=True)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
CSRF_COOKIE_HTTPONLY = env.bool("DJANGO_CSRF_COOKIE_HTTPONLY", default=True)
X_FRAME_OPTIONS = env.str("DJNAGO_X_FRAME_OPTIONS", default="DENY")

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_USE_TLS = env.bool("DJANGO_EMAIL_USE_TLS", default=True)
EMAIL_PORT = env.int("DJANGO_EMAIL_PORT", default=587)
DEFAULT_FROM_EMAIL = env.str("DJANGO_DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)
SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default=EMAIL_HOST_USER)

# CACHING
# ------------------------------------------------------------------------------
CACHE_MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
]
MIDDLEWARE = MIDDLEWARE[:1] + CACHE_MIDDLEWARE + MIDDLEWARE[1:]
MIDDLEWARE.append("django.middleware.cache.FetchFromCacheMiddleware")

CACHE_MIDDLEWARE_SECONDS = 3600
USE_ETAGS = True
