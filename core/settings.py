from pathlib import Path
import os
import environ # type: ignore


env = environ.Env()
environ.Env.read_env()

ENVIRONMENT = env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = [
    '*'
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
# Application definition

INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # Auth / terceros
    'allauth',
    'allauth.account',
    'allauth.socialaccount',



    # Core apps
    'core',
    'accounts',
    'social',

    # 🟢 Apps con signals (USAR AppConfig)
    'friends.apps.FriendsConfig',          # si tenés signals ahí
    'notifications.apps.NotificationsConfig',
    'lost_found.apps.LostFoundConfig',
    'parroquiales.apps.ParroquialesConfig',
    'store.apps.StoreConfig',
    'groups.apps.GroupsConfig',
    'foster.apps.FosterConfig',

    # Otras apps
    'reels',
    'pets',
    'search',
    'interactions',
    'messaging.apps.MessagingConfig',

]


SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ================ ALLAUTH ==================== #
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_UNIQUE = True
AUTH_USER_MODEL="accounts.User"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGIN_URL = "account_login"
ACCOUNT_RATE_LIMITS = {
    'login': '5/m',  # Máximo 5 intentos por minuto.
    'login_failed': '3/5m',  # Máximo 3 intentos fallidos en 5 minutos.
    'signup': '3/h'  # Máximo 3 registros por hora.
}
# ELIMINA USERNAME DEL FORM
ACCOUNT_SIGNUP_FORM_CLASS = None
ACCOUNT_FORMS = {
    "login": "accounts.forms.CustomLoginForm",
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notifications_nav',
                'pets.context_processors.user_pets',
                'messaging.context_processors.messages_preview',    
                "messaging.context_processors.contacts_list",
                "groups.context_processors.groups_sidebar",

            ],
        },
    },
]




WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql', 'NAME': 'mascotas25$default', 'USER': 'mascotas25', 'PASSWORD': '_$SgS$X6w2uPkPz', 'HOST': 'mascotas25.mysql.pythonanywhere-services.com', 'PORT': '3306', 'OPTIONS': { 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", }, } }

# DATABASES = {
#     "default": env.db("DATABASE_URL", default="//postgres:1@127.0.0.1:5432/social"),
#}

DATABASES["default"]["ATOMIC_REQUESTS"] = True


PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

if not DEBUG:
    # EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = env('EMAIL_HOST')
    # EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    # EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    # EMAIL_PORT = env('EMAIL_PORT')
    # EMAIL_USE_TLS = env('EMAIL_USE_TLS')

    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


    DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB total
    FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024  # 2MB por archivo


    # s3 static settings
