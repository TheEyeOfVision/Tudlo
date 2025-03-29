# summarization_project/settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'  # Replace with your actual secret key

DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['*']  # Allow all hosts for development

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',          # For REST API endpoints, if needed
    'corsheaders',             # For CORS support
    # Add your apps here (e.g., 'api' or similar)
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be placed as high as possible
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS configuration: You can either allow all origins or specify a whitelist.
# To allow all origins (not recommended for production):
CORS_ALLOW_ALL_ORIGINS = True

# Alternatively, to allow specific origins:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8501",  # Your frontend URL (update as needed)
#     "http://localhost:3000",  # Another example origin
# ]

ROOT_URLCONF = 'summarization_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add template directories if needed
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

WSGI_APPLICATION = 'summarization_project.wsgi.application'

# Database: Using SQLite for development; change as needed for production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Groq API Key (if used within your backend)
GROQ_API_KEY = "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"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Optional: Set APPEND_SLASH behavior
# If you prefer no automatic trailing slash redirects, disable it:
# APPEND_SLASH = False
