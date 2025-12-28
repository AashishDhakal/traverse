"""
Django settings for SummitX-Django project.

Content-Commerce Ecosystem with Unified Semantic Architecture.
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-change-this-in-production-91p9u0n0kifwb")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# Application definition

INSTALLED_APPS = [
    # Unfold Admin Theme (must be before django.contrib.admin)
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    # Django built-in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",  # For dynamic sitemaps
    # Third-party
    "compressor",
    "meta",
    # SummitX Apps - Unified Semantic Architecture
    "apps.core",  # UniversalTag, Region
    "apps.team",  # TeamMember (E-E-A-T)
    "apps.trips",  # Trip products
    "apps.content",  # BlogPost marketing
    "apps.glossary",  # SEO glossary auto-linker
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files serving
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'apps.glossary.middleware.GlossaryAutoLinkerMiddleware',  # Enable when ready
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Redis Cache (for high-traffic landing pages)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Uncomment for production with Redis:
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"  # Nepal timezone
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise for static files (production only)
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Django Compressor
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
COMPRESS_ENABLED = True


# Media files (uploads)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================
# CKEditor 5 Configuration
# ============================================

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "|",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "|",
            "imageUpload",
            "mediaEmbed",
            "|",
            "undo",
            "redo",
        ],
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
            ]
        },
    },
    "extends": {
        # Extended config for blog posts - supports Trip Card embedding
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "code",
            "|",
            "link",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "codeBlock",
            "insertTable",
            "|",
            "imageUpload",
            "mediaEmbed",
            "|",
            "outdent",
            "indent",
            "|",
            "undo",
            "redo",
            "|",
            "sourceEditing",
        ],
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Heading 4", "class": "ck-heading_heading4"},
            ]
        },
        "image": {"toolbar": ["imageTextAlternative", "imageStyle:full", "imageStyle:side"]},
        "table": {"contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"]},
    },
}

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
CKEDITOR_5_UPLOAD_PATH = "uploads/ckeditor/"


# ============================================
# Django Meta (SEO) Configuration
# ============================================

META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "summitx.com"  # Update for production
META_SITE_NAME = "SummitX - Adventure Travel Nepal"
META_INCLUDE_KEYWORDS = ["nepal", "trekking", "himalaya", "adventure"]
META_DEFAULT_KEYWORDS = ["nepal trekking", "himalayan adventure", "everest trek"]
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_SCHEMAORG_PROPERTIES = True
META_FB_APP_ID = ""  # Add Facebook App ID for analytics
META_TWITTER_SITE = "@traversehimalaya"  # Twitter handle


# ============================================
# Django Unfold Admin Configuration
# ============================================

UNFOLD = {
    "SITE_TITLE": "Traverse The Himalayas",
    "SITE_HEADER": "Traverse The Himalayas",
    "SITE_SUBHEADER": "Content-Commerce Admin",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: "/static/images/logo.png",
        "dark": lambda request: "/static/images/logo.png",
    },
    "SITE_SYMBOL": "hiking",  # Material symbol
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "50": "240 253 250",
            "100": "204 251 241",
            "200": "153 246 228",
            "300": "94 234 212",
            "400": "45 212 191",
            "500": "20 184 166",
            "600": "13 148 136",
            "700": "15 118 110",
            "800": "17 94 89",
            "900": "19 78 74",
            "950": "4 47 46",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Dashboard",
                "separator": True,
                "items": [
                    {
                        "title": "Overview",
                        "icon": "dashboard",
                        "link": "/admin/",
                    },
                ],
            },
            {
                "title": "Content Management",
                "separator": True,
                "items": [
                    {
                        "title": "Trips",
                        "icon": "hiking",
                        "link": "/admin/trips/trip/",
                    },
                    {
                        "title": "Blog Posts",
                        "icon": "article",
                        "link": "/admin/content/blogpost/",
                    },
                    {
                        "title": "Team Members",
                        "icon": "groups",
                        "link": "/admin/team/teammember/",
                    },
                ],
            },
            {
                "title": "Taxonomy",
                "separator": True,
                "items": [
                    {
                        "title": "Tags",
                        "icon": "tag",
                        "link": "/admin/core/universaltag/",
                    },
                    {
                        "title": "Regions",
                        "icon": "map",
                        "link": "/admin/core/region/",
                    },
                    {
                        "title": "Glossary",
                        "icon": "book",
                        "link": "/admin/glossary/term/",
                    },
                ],
            },
        ],
    },
}
