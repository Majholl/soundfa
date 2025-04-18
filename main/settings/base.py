from pathlib import Path
from os import path , getenv
from dotenv import load_dotenv
from loguru import logger
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)
    


# Application definition
APP_DIR = BASE_DIR / 'core_apps'

STATIC_URL = 'static/'
STATIC_DIR = 'static/'


MEDIA_DIR = '/media/'
MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR , "media")


# Apps that working with togheter to make the project working
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',] 

THIDR_PARTY_APPS = ['rest_framework',  'corsheaders', 'rest_framework_simplejwt']

LOCAL_APP = ['core_apps.musicapp', 'core_apps.user']

INSTALLED_APPS = DJANGO_APPS + THIDR_PARTY_APPS + LOCAL_APP




# Middlewares which their job is to act as gate to change and customize Requests/Response
DJANGO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THIRD_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',]
LOCAL_MIDDLEWARE = []

MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_MIDDLEWARE + LOCAL_MIDDLEWARE 



# CORS configuration
# CORS_ALLOWED_ORIGINS = ["https://*", 'http://localhost', 'http://127.0.0.1']
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True # production mode



REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES' : ('core_apps.musicapp.cookie_auth.CookieAuthentication',),
    
}

SIMPLE_JWT = {
    'SIGNING_KEY': getenv('SIGNING_KEY'),
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'USER_ID_FIELD' : 'id',
    'USER_ID_CLAIM': 'user_id'
}


COOKIE_NAME = 'access'
COOKIE_SAMESITE = 'Lax'
COOKIE_PATH ='/'
COOKIE_HTTPONLY = True
COOKIE_SECURE = getenv("COOKIE_SECURE", "True") 



# logs configurations
LOGGIN_CONFIG=None

LOGURU_LOGGING = {
    'handlers':[
        {
            'sink': BASE_DIR / 'logs/debug.log',
            'level': 'DEBUG',
            'filter': lambda record : record['level'].no == logger.level('WARNING' , None).no ,
            'format': '{time:YYYY-MM-DD HH:mm:ss.SSS}|{level:<8}|{name}:{function}:{line} - ""{message}""',
            'rotation': '10MB',
            'retention':'30 days',
            'compression':'zip',
        },
        {
            'sink': BASE_DIR / 'logs/info.log',
            'level': 'INFO',
            'filter': lambda record : record['level'].no == logger.level('INFO').no,
            'format': '{time:YYYY-MM-DD HH:mm:ss.SSS}|{level:<8}|{name}:{function}:{line} - "{message}"',
            'rotation': '10MB',
            'retention':'30 days',
            'compression':'zip', 
        },
    ]}

logger.configure(**LOGURU_LOGGING)

LOGGING = {
    'version':1,
    'disable_existing_loggers': False,
    'handlers':{'loguru':{'class':'intercepter.InterceptHandler'}},
    'root':{'handlers':['loguru'] , 'level':'DEBUG'}
}







ROOT_URLCONF = 'main.urls'





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APP_DIR / 'templates')],
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

WSGI_APPLICATION = 'main.wsgi.application'









# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('DB_NAME'),
        'HOST': getenv('DB_HOST'),
        'USER': getenv('DB_USER'),
        'PORT': getenv('DB_PORT'), 
    }
}





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]






# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'user.Users'