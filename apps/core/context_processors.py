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

    # Default values for whitelabeling
    defaults = {
        "site_config": config,
        "current_site": site,
        "brand_name": "Nepal Travel Portal",
        "tagline": "Your Gateway to Himalayan Adventures",
        "title_suffix": "",
        "hero_title": "Discover Nepal",
        "hero_subtitle": "Experience the majesty of the Himalayas with expert-led adventures.",
        "hero_cta_text": "Explore Trips",
        "footer_description": "Expert-led adventures through the world's most majestic mountain ranges.",
        "primary_color": "#0d9488",
        "secondary_color": "#0f766e",
        "accent_color": "#f59e0b",
    }

    # If no config, return defaults
    if config is None:
        return defaults

    # Override with config values
    return {
        "site_config": config,
        "current_site": site,
        "brand_name": config.brand_name,
        "tagline": config.tagline or defaults["tagline"],
        "title_suffix": config.title_suffix or f" | {config.brand_name}",
        "hero_title": config.hero_title or defaults["hero_title"],
        "hero_subtitle": config.hero_subtitle or defaults["hero_subtitle"],
        "hero_cta_text": config.hero_cta_text or defaults["hero_cta_text"],
        "footer_description": config.footer_description or config.tagline or defaults["footer_description"],
        "primary_color": config.primary_color or defaults["primary_color"],
        "secondary_color": config.secondary_color or defaults["secondary_color"],
        "accent_color": config.accent_color or defaults["accent_color"],
    }
