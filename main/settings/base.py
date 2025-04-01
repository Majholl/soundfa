from pathlib import Path
from os import path , getenv
from dotenv import load_dotenv
from loguru import logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)
    


# Application definition
APP_DIR = BASE_DIR / 'core_apps'

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',] 
THIDR_PARTY_APPS = ['rest_framework',]
LOCAL_APP = ['core_apps.musicapp',]
INSTALLED_APPS = DJANGO_APPS + THIDR_PARTY_APPS + LOCAL_APP



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







MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
        'PORT': getenv('DB_PORT')
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_DIR = '/media/'

MEDIA_ROOT = path.join(BASE_DIR , "media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
