import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'pee^34#xy=w=i2+$f5d9nl$*0@xe*up)$ov6^#(d1u^-h8z=)x'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'server',
        'USER': 'admin',
        'PASSWORD': '123456',
    }
}

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'public.permissions.TokenExpirationCheck',
    )
}

LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


LOG_FILE_COUNT = 3  # 备份份数
LOG_FILE_SIZE_MAX = 10485706  # 日志大小10MB
LOG_DIR = os.path.join(BASE_DIR, 'log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detail': {
            'format': '%(asctime)s [%(process)d] [%(threadName)s:%(thread)d] '
                      '[%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'
        },
        'brief': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detail'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        },
        'public': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'public.log'),
            'formatter': 'detail',
            'backupCount': LOG_FILE_COUNT,
            'maxBytes': LOG_FILE_SIZE_MAX

        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['public'],
            'level': 'WARNING',
            'propagate': False,
        },
        'public': {
            'handlers': ['public'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '3164202528@qq.com'
EMAIL_HOST_PASSWORD = 'zs@200483'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
