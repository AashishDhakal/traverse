"""
Context processors for the core app.

Provides site configuration to all templates.
"""


def site_config(request):
    """
    Add site configuration to template context.

    Makes site_config available in all templates:
    - {{ site_config.brand_name }}
    - {{ site_config.logo.url }}
    - {{ site_config.primary_color }}
    etc.
    """
    config = getattr(request, "site_config", None)
    site = getattr(request, "site", None)

    # Provide fallback values if no configuration exists
    if config is None:
        return {
            "site_config": None,
            "current_site": site,
            "brand_name": "Traverse The Himalayas",
            "tagline": "Your Gateway to Himalayan Adventures",
        }

    return {
        "site_config": config,
        "current_site": site,
        "brand_name": config.brand_name,
        "tagline": config.tagline,
    }
