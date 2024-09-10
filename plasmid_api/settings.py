"""
Django settings for plasmid_api project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@$^oy$2_m!)brfp&_@&q4inn*t_=)cm&)r(2l2jdhk(&n4!#!='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'database',
    'drf_yasg',
    'analysis',
    'django_crontab',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.gzip.GZipMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = 'plasmid_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'plasmid_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'plasmid_db',
        'USER': 'plasmid_admin',
        'PASSWORD': 'Io81iwv!J@3u',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRONJOBS = [
    ('*/1 * * * *', 'analysis.cron.task_status_update')
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static/'),
    # os.path.join(BASE_DIR, 'web-build/static/')
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"


# analysis module path 
USERTASKPATH = 'workspace/user_task'
ABSUSERTASKPATH = '/home/platform/project/plasmid_platform/plasmid_api/workspace/user_task'
# PLASMIDDATA = '/home/platform/project/plasmid_platform/plasmid_api/media/data/'
PROTEINSEQUENCE = '/home/platform/phage_db/phage_data/data/phage_sequence/proteins/'
TEMPPATH = '/home/platform/project/plasmid_platform/plasmid_api/media/data/tmp/'


CLUSTERTREEPATH = '/home/platform/phage_db/phage_data/data/phage_sequence/cluster_tree_v2/'
CLUSTERALIGNMENTPATH='/home/platform/phage_db/phage_data/data/analysis_data/alignment/result'
CLUSTERSEQUENCEPATH = '/home/platform/phage_db/phage_data/data/phage_sequence/group/'
METADATA = '/home/platform/project/plasmid_platform/plasmid_api/media/data/'
FASTAPATH = '/home/platform/phage_db/phage_data/data/'
# Analysis script path


ANALYSIS = '/home/platform/phage_db/phage_api/workspace/analysis_script/'
# TASKLOG = '/home/platform/project/plasmid_platform/plasmid_api/workspace/task_log/'
TASKLOG = '/home/platform/phage_db/phage_api/workspace/task_log/'

DEMOFILE = '/home/platform/project/plasmid_platform/plasmid_api/demo_file/'
