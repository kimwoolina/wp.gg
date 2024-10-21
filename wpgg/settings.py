"""
Django settings for wpgg project.
Generated by 'django-admin startproject' using Django 4.2.
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
from . import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

RIOT_API_KEY = config.RIOT_API_KEY

OPEN_API_KEY = config.OPEN_API_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["43.201.57.125", "localhost", "127.0.0.1", "wpgg.kr"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #thid_party
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_seed',
    # Allauth 관련 앱
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # 소셜 로그인
    'allauth.socialaccount.providers.google',  # 필요한 소셜 제공자 추가 (구글 로그인)
    'dj_rest_auth',
    'dj_rest_auth.registration',
    #local_apps
    'users',
    'articles',
    'chats',
    'parties',
    'profiles',
    'credits',
    'common',
    'web',
]

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],  # Redis 서버 주소와 포트
#         },
#     },
# }

# Redis를 django의 cache로 사용
CACHES = {  
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379",
        "LOCATION": "redis://43.201.57.125:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

Q_CLUSTER = {
    'name': 'wp.gg',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'django_redis': 'default',  # Redis 사용 시
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'sync': False,  # True로 설정하면 동기화 모드로 실행됨
}

ASGI_APPLICATION = 'wpgg.asgi.application'

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'users.auth.DiscordAuthenticationBackend', #discord 백엔드
    'django.contrib.auth.backends.ModelBackend',  # 기본 백엔드
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth 백엔드
)

ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 이메일로 로그인 
ACCOUNT_EMAIL_REQUIRED = True  # 이메일 필수
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # 이메일 인증 설정 (필요에 따라 설정 / 'mandatory' 이메일 인증 필수 )
ACCOUNT_UNIQUE_EMAIL = True  # 이메일 중복 방지


# 이메일 발송을 위한 기본 설정, 실제 배포시에는 SMTP 서버 설정 해야함
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 테스트용으로 콘솔에 출력

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'wpgg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'wpgg.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT 인증
        # 'rest_framework.authentication.SessionAuthentication',        # 세션 인증 (옵션)
        # 'rest_framework.authentication.BasicAuthentication',         # 기본 인증 (옵션)
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',  # 인증된 사용자만 접근
    ),
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if DEBUG == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':config.POSTGRES_NAME,
            'USER':config.POSTGRES_USER,
            'PASSWORD':config.POSTGRES_PASSWORD,
            'HOST':config.POSTGRES_HOST,
            'PORT':'5432'
        }
    }


AUTH_USER_MODEL = 'users.User'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

#Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST_FRAMEWORK = {
#     # 페이지네이션
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,  # 페이지당 항목 수
# }

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # 허용할 프론트엔드 URL
# ]

CORS_ALLOW_ALL_ORIGINS = True  # 모든 도메인 허용 (개발용)

# All found @https://discord.com/developers/applications/ under your apps "OAuth2" section, make sure to set "scopes" as "identify" only.
DiscordOAuth2 = {
    "CLIENT_ID": config.DISCORD_CLIENT_ID,
    "CLIENT_SECRET": config.DISCORD_SECRET_ID,
    "API_ENDPOINT": "https://discord.com/api/v10",
    "REDIRECT_URI": "http://43.201.57.125/auth/discordlogin/",
    "DISCORD_OAUTH2_URL": config.DISCORD_OAUTH2_URL
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
