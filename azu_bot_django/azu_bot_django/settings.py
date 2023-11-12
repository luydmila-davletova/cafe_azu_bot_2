import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-$9h!ujjvgrgilsbc&%idh%)tb86u+^qkr#2#p!o^ej48n6)=m7'

DEBUG = True

ALLOWED_HOSTS = []

MAX_CHAR_LENGHT = 256
MAX_DIGIT_LENGHT = 10
MAX_DECIMAL_LENGHT = 2

# AUTH_USER_MODEL = 'users.CustomUser'

INSTALLED_APPS = [
    'cafe.apps.CafeConfig',
    'menu.apps.MenuConfig',
    'reservation.apps.ReservationConfig',
    'tables.apps.TablesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ckeditor',
    'admin_users',

]

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_JQUERY_URL = 'https://cdn.jsdelivr.net/jquery/3.5.1/jquery.min.js'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'azu_bot_django.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'azu_bot_django.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DATABASE_NAME', default='postgres'),
#         'USER': os.getenv('DATABASE_USERNAME', default='postgres'),
#         'PASSWORD': os.getenv('DATABASE_PASSWORD', default='postgres'),
#         'HOST': os.getenv('DATABASE_HOST', default='localhost'),
#         'PORT': os.getenv('DATABASE_PORT', default='5432'),
#     }
# }


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


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PERMISSIONS_LIST = [
    "view_cafe",
    "view_customuser",
    "view_dish",
    "view_set",
    "view_setdish",
    "view_ordersets",
    "view_reservation",
    "view_table",
    "view_reservationtable",

    "add_dish",
    "add_set",
    "add_setdish",
    "add_ordersets",
    "add_reservation",
    "add_table",
    "add_reservationtable",

    "change_dish",
    "change_set",
    "change_setdish",
    "change_ordersets",
    "change_reservation",
    "change_table",
    "change_reservationtable",

    "delete_dish",
    "delete_set",
    "delete_setdish",
    "delete_ordersets",
    "delete_reservation",
    "delete_table",
    "delete_reservationtable"
]
