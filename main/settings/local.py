from os import path , getenv 
from dotenv import load_dotenv
from .base import * #noqa




# Local variables 
SITE_NAME = getenv("SITE_NAME")

ADMIN_URL = getenv("ADMIN_URL")

SECRET_KEY = getenv('SECRET_KEY')

DEBUG = getenv('DEBUG')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


    
CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

CELERY_ACCEPT_CONTENT = ["application/json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = getenv('EMAIL_HOST')

EMAIL_PORT = getenv('EMAIL_PORT')

ADMIN_EMAIL=getenv('ADMIN_EMAIL')

DEFAULT_FROM_EMAIL=getenv('DEFAULT_FROM_EMAIL')

MAX_UPLOAD_SIZE = 10 * 1024 * 1024 # 10 Mg

OTP_REQUIRED = getenv('OTP_REQUIRED')

OTP_EXPIRE_TIME = timedelta(minutes=5)

RESET_PASSWORD_EXPIRE_TIME = timedelta(minutes=5)
