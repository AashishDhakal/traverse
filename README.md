# SummitX Django - Multi-Site Travel Platform

A Django-based travel platform supporting multiple whitelabeled portals from a single codebase.

## 🌄 Features

- **Multi-Site Architecture** - Run multiple travel portals (Traverse, VisitNepalDirect, NepalLuxe, BudgetHimalaya) from one codebase
- **Dynamic Branding** - Per-site logos, colors, hero sections, and footer content
- **Content Management** - Trips, blog posts, team members, regions, and glossary
- **SEO Optimized** - Meta tags, structured data, sitemap support
- **Modern Admin** - Django Unfold admin theme
- **Production Ready** - PostgreSQL, Redis caching, WhiteNoise static files

## 🚀 Quick Start

### Local Development

```bash
# Clone and setup
git clone https://github.com/AashishDhakal/traverse.git
cd traverse
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run migrations and load sample data
python manage.py migrate
python manage.py load_sample_data

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Production Setup

Set these environment variables:

```bash
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
STATIC_ROOT=/var/www/static
MEDIA_ROOT=/var/www/media
```

## 🏗️ Architecture

### Multi-Site Configuration

Each portal is configured via `SiteConfiguration` model:

- **Branding**: Logo, brand name, tagline, favicon
- **Theme Colors**: Primary, secondary, accent colors (CSS custom properties)
- **Hero Section**: Title, subtitle, CTA button text, background image
- **Contact**: Email, phone, WhatsApp, address
- **Social Media**: Facebook, Instagram, Twitter, YouTube, TikTok
- **SEO**: Meta description, keywords
- **Analytics**: Google Analytics, Facebook Pixel

### Key Apps

| App | Description |
|-----|-------------|
| `core` | Regions, tags, site configuration, middleware |
| `trips` | Trek/expedition listings with itineraries |
| `content` | Blog posts and travel guides |
| `team` | Team member profiles |
| `glossary` | Trekking terminology |

## 📦 Management Commands

```bash
# Load sample data (regions, trips, blog posts, site configs)
python manage.py load_sample_data

# Clear and reload all sample data
python manage.py load_sample_data --clear

# Collect static files (production)
python manage.py collectstatic
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | Required in production |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection URL | SQLite fallback |
| `SITE_ID` | Default Django site ID | `1` |
| `STATIC_ROOT` | Static files directory | `staticfiles/` |
| `MEDIA_ROOT` | Media files directory | `media/` |
| `ADMIN_SITE_TITLE` | Admin panel title | `Nepal Travel Admin` |

### Multi-Domain Setup

1. Add sites in Django admin: `/admin/sites/site/`
2. Create SiteConfiguration for each site: `/admin/core/siteconfiguration/`
3. Point all domains to the same server
4. Configure nginx to proxy all domains to Django

## 🎨 Theming

Colors are set per-site via CSS custom properties:

```css
:root {
    --color-primary: #0d9488;    /* From site_config.primary_color */
    --color-secondary: #0f766e;  /* From site_config.secondary_color */
    --color-accent: #f59e0b;     /* From site_config.accent_color */
}
```

Theme classes available:
- `.btn-primary` - Gradient button using brand colors
- `.text-brand` - Text in primary color
- `.bg-brand` - Background in primary color
- `.gradient-text` - Gradient text effect

## 📁 Project Structure

```
├── apps/
│   ├── core/          # Site config, regions, tags, middleware
│   ├── trips/         # Trek listings
│   ├── content/       # Blog posts
│   ├── team/          # Team members
│   └── glossary/      # Terminology
├── config/
│   ├── settings.py    # Django settings
│   └── urls.py        # URL routing
├── templates/         # HTML templates
├── static/            # CSS, JS, images
└── media/             # User uploads
```

## 🔒 Security

- CSRF protection enabled
- XSS prevention via template escaping
- Secure password validation
- Environment-based secret key
- HTTPS recommended in production

## 📄 License

Private/Proprietary - All rights reserved.

## 🤝 Contributing

Internal development only. Contact project maintainers for access.
