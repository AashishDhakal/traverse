"""
Load sample data for Traverse The Himalayas.

Usage: python manage.py load_sample_data
"""
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = "Load sample data for Traverse The Himalayas"

    def handle(self, *args, **options):
        self.stdout.write("Loading sample data...")

        self._copy_sample_images()
        self._create_tags()
        self._create_regions()
        self._create_team_members()
        self._create_trips()
        self._create_blog_posts()
        self._create_glossary_terms()

        self.stdout.write(self.style.SUCCESS("✓ Sample data loaded successfully!"))

    def _copy_sample_images(self):
        """Copy sample images from static/sample to media folders."""
        static_sample = Path(settings.BASE_DIR) / "static" / "sample"
        media_root = Path(settings.MEDIA_ROOT)

        # Copy trip images
        trips_src = static_sample / "trips"
        trips_dest = media_root / "trips" / "featured"
        trips_dest.mkdir(parents=True, exist_ok=True)

        if trips_src.exists():
            for img in trips_src.glob("*.png"):
                shutil.copy2(img, trips_dest / img.name)
            self.stdout.write(f"  Copied {len(list(trips_src.glob('*.png')))} trip images")

        # Copy blog images
        blog_src = static_sample / "blog"
        blog_dest = media_root / "blog" / "featured"
        blog_dest.mkdir(parents=True, exist_ok=True)

        if blog_src.exists():
            for img in blog_src.glob("*.png"):
                shutil.copy2(img, blog_dest / img.name)
            self.stdout.write(f"  Copied {len(list(blog_src.glob('*.png')))} blog images")

    def _create_tags(self):
        from apps.core.models import UniversalTag

        tags_data = [
            {
                "name": "Everest",
                "slug": "everest",
                "icon": "fa-mountain",
                "description": "Expeditions and treks in the Everest region, home to the world's highest peak.",
                "is_featured": True,
            },
            {
                "name": "Annapurna",
                "slug": "annapurna",
                "icon": "fa-mountain-sun",
                "description": "Adventures around the spectacular Annapurna massif.",
                "is_featured": True,
            },
            {
                "name": "Winter Treks",
                "slug": "winter",
                "icon": "fa-snowflake",
                "description": "Cold-weather adventures for experienced trekkers.",
                "is_featured": True,
            },
            {
                "name": "Teahouse Trek",
                "slug": "teahouse",
                "icon": "fa-mug-hot",
                "description": "Comfortable treks staying in local lodges.",
                "is_featured": True,
            },
            {
                "name": "Camping",
                "slug": "camping",
                "icon": "fa-campground",
                "description": "Wilderness camping adventures off the beaten path.",
            },
            {
                "name": "Peak Climbing",
                "slug": "peak-climbing",
                "icon": "fa-flag",
                "description": "Technical climbing expeditions for aspiring mountaineers.",
                "is_featured": True,
            },
            {
                "name": "Beginner Friendly",
                "slug": "beginner",
                "icon": "fa-seedling",
                "description": "Perfect first-time trekking experiences.",
                "is_featured": True,
            },
            {
                "name": "Cultural",
                "slug": "cultural",
                "icon": "fa-om",
                "description": "Immersive cultural experiences in Nepal.",
            },
        ]

        for i, data in enumerate(tags_data):
            UniversalTag.objects.update_or_create(slug=data["slug"], defaults={**data, "display_order": i})

        self.stdout.write(f"  Created {len(tags_data)} tags")

    def _create_regions(self):
        from apps.core.models import Region

        # Parent regions
        nepal = Region.objects.update_or_create(
            slug="nepal", defaults={"name": "Nepal", "description": "The heart of the Himalayas", "is_featured": True}
        )[0]

        regions_data = [
            {
                "name": "Everest Region",
                "slug": "everest-region",
                "parent": nepal,
                "description": "Home to Mount Everest and the Sherpa culture.",
                "is_featured": True,
                "latitude": 27.9881,
                "longitude": 86.9250,
            },
            {
                "name": "Annapurna Region",
                "slug": "annapurna-region",
                "parent": nepal,
                "description": "Diverse landscapes from subtropical to alpine.",
                "is_featured": True,
                "latitude": 28.5960,
                "longitude": 83.8203,
            },
            {
                "name": "Langtang Region",
                "slug": "langtang-region",
                "parent": nepal,
                "description": "The valley of glaciers, close to Kathmandu.",
                "is_featured": True,
                "latitude": 28.2139,
                "longitude": 85.5619,
            },
            {
                "name": "Manaslu Region",
                "slug": "manaslu-region",
                "parent": nepal,
                "description": "Remote and less-traveled mountain region.",
                "latitude": 28.5497,
                "longitude": 84.5592,
            },
        ]

        for i, data in enumerate(regions_data):
            Region.objects.update_or_create(slug=data["slug"], defaults={**data, "display_order": i})

        self.stdout.write(f"  Created {len(regions_data) + 1} regions")

    def _create_team_members(self):
        from apps.team.models import TeamMember

        members_data = [
            {
                "name": "Pemba Sherpa",
                "slug": "pemba-sherpa",
                "role": "guide",
                "title": "Lead Mountain Guide",
                "bio": "Pemba has summited Everest 12 times and has over 20 years of guiding experience in the Himalayas. Born in Namche Bazaar, he knows the mountains like the back of his hand.",
                "short_bio": "12x Everest summiteer with 20+ years experience",
                "certifications": ["IFMGA Certified", "Wilderness First Responder", "Avalanche Safety Level 3"],
                "years_experience": 20,
                "trips_led": 150,
                "summits": 45,
                "is_verified_expert": True,
            },
            {
                "name": "Mingma Tamang",
                "slug": "mingma-tamang",
                "role": "guide",
                "title": "Senior Trek Leader",
                "bio": "Mingma specializes in the Annapurna and Langtang regions. His warm personality and deep knowledge of local culture make every trek memorable.",
                "short_bio": "Annapurna specialist with cultural expertise",
                "certifications": ["Nepal Mountaineering Association Certified", "First Aid Certified"],
                "years_experience": 15,
                "trips_led": 200,
                "is_verified_expert": True,
            },
            {
                "name": "Sarah Mitchell",
                "slug": "sarah-mitchell",
                "role": "author",
                "title": "Adventure Travel Writer",
                "bio": "Sarah is an award-winning travel writer who has trekked across 30 countries. She brings the magic of the Himalayas to life through her vivid storytelling.",
                "short_bio": "Award-winning adventure travel writer",
                "certifications": ["Travel Writers Guild Member"],
                "years_experience": 10,
                "is_verified_expert": True,
            },
        ]

        for i, data in enumerate(members_data):
            TeamMember.objects.update_or_create(slug=data["slug"], defaults={**data, "display_order": i})

        self.stdout.write(f"  Created {len(members_data)} team members")

    def _create_trips(self):
        from apps.core.models import Region, UniversalTag
        from apps.trips.models import Trip

        trips_data = [
            {
                "title": "Everest Base Camp Trek",
                "slug": "everest-base-camp-trek",
                "tagline": "Stand at the foot of the world's highest peak",
                "overview": "The classic trek to Everest Base Camp takes you through stunning Sherpa villages, ancient monasteries, and breathtaking mountain scenery. Witness sunrise over Everest from Kala Patthar.",
                "detailed_itinerary": "<h2>Day 1: Fly to Lukla, Trek to Phakding</h2><p>Scenic flight followed by easy acclimatization walk.</p><h2>Day 2-14: Journey to Base Camp</h2><p>Gradual ascent through Namche, Tengboche, and beyond.</p>",
                "duration_days": 14,
                "max_altitude": 5545,
                "difficulty": "challenging",
                "price": 2499,
                "region_slug": "everest-region",
                "tags": ["everest", "teahouse"],
                "is_published": True,
                "is_featured": True,
            },
            {
                "title": "Annapurna Circuit",
                "slug": "annapurna-circuit",
                "tagline": "The world's greatest trek through diverse landscapes",
                "overview": "Circle the Annapurna massif through subtropical forests, alpine meadows, and cross the legendary Thorong La Pass at 5,416m. Experience incredible cultural diversity.",
                "detailed_itinerary": "<h2>Day 1-3: Subtropical Zone</h2><p>Start from Besisahar through lush vegetation.</p><h2>Day 4-12: High Altitude Crossing</h2><p>Acclimatize and cross Thorong La.</p>",
                "duration_days": 18,
                "max_altitude": 5416,
                "difficulty": "challenging",
                "price": 1899,
                "region_slug": "annapurna-region",
                "tags": ["annapurna", "teahouse", "cultural"],
                "is_published": True,
                "is_featured": True,
            },
            {
                "title": "Poon Hill Trek",
                "slug": "poon-hill-trek",
                "tagline": "Perfect introduction to Himalayan trekking",
                "overview": "A short but rewarding trek offering spectacular sunrise views over Annapurna and Dhaulagiri. Ideal for first-time trekkers and those with limited time.",
                "detailed_itinerary": "<h2>Day 1-2: Trek to Ghorepani</h2><p>Scenic walk through rhododendron forests.</p><h2>Day 3: Sunrise at Poon Hill</h2><p>Early morning hike for panoramic views.</p>",
                "duration_days": 5,
                "max_altitude": 3210,
                "difficulty": "easy",
                "price": 699,
                "discounted_price": 599,
                "region_slug": "annapurna-region",
                "tags": ["annapurna", "teahouse", "beginner"],
                "is_published": True,
                "is_featured": True,
            },
            {
                "title": "Langtang Valley Trek",
                "slug": "langtang-valley-trek",
                "tagline": "The valley of glaciers, close to Kathmandu",
                "overview": "Explore the beautiful Langtang Valley with its stunning glaciers, Tamang culture, and diverse wildlife. One of the most accessible high-altitude treks from Kathmandu.",
                "detailed_itinerary": "<h2>Day 1-2: Drive to Syabrubesi</h2><p>Scenic drive through hills.</p><h2>Day 3-7: Valley Exploration</h2><p>Trek through the glacier valley.</p>",
                "duration_days": 10,
                "max_altitude": 4984,
                "difficulty": "moderate",
                "price": 1299,
                "region_slug": "langtang-region",
                "tags": ["teahouse", "cultural"],
                "is_published": True,
                "is_featured": True,
            },
            {
                "title": "Island Peak Climbing",
                "slug": "island-peak-climbing",
                "tagline": "Summit your first Himalayan peak",
                "overview": "Combine the Everest Base Camp trek with a summit attempt of Island Peak (6,189m). Perfect for trekkers looking to take their first steps into mountaineering.",
                "detailed_itinerary": "<h2>Day 1-12: Trek to Base Camp</h2><p>Standard EBC route with acclimatization.</p><h2>Day 13-16: Island Peak</h2><p>Climbing training and summit attempt.</p>",
                "duration_days": 20,
                "max_altitude": 6189,
                "difficulty": "extreme",
                "price": 3999,
                "region_slug": "everest-region",
                "tags": ["everest", "peak-climbing", "camping"],
                "is_published": True,
                "is_featured": True,
            },
        ]

        for data in trips_data:
            region = Region.objects.filter(slug=data.pop("region_slug")).first()
            tag_slugs = data.pop("tags")

            trip, created = Trip.objects.update_or_create(slug=data["slug"], defaults={**data, "region": region})

            tags = UniversalTag.objects.filter(slug__in=tag_slugs)
            trip.tags.set(tags)

        # Assign featured images (from media folder)
        trip_images = {
            "everest-base-camp-trek": "trips/featured/everest_base_camp.png",
            "annapurna-circuit": "trips/featured/annapurna_circuit.png",
            "poon-hill-trek": "trips/featured/poon_hill.png",
            "langtang-valley-trek": "trips/featured/langtang_valley.png",
            "island-peak-climbing": "trips/featured/island_peak.png",
        }
        for slug, img_path in trip_images.items():
            Trip.objects.filter(slug=slug).update(featured_image=img_path)

        self.stdout.write(f"  Created {len(trips_data)} trips with images")

    def _create_blog_posts(self):
        from apps.content.models import BlogPost
        from apps.core.models import Region, UniversalTag
        from apps.team.models import TeamMember
        from apps.trips.models import Trip

        author = TeamMember.objects.filter(role="author").first() or TeamMember.objects.first()

        posts_data = [
            {
                "title": "Complete Everest Base Camp Packing List 2025",
                "slug": "everest-base-camp-packing-list-2025",
                "excerpt": "Everything you need to pack for the Everest Base Camp trek, from clothing layers to essential gear. Updated for 2025 with expert recommendations.",
                "content": "<h2>Clothing Layers</h2><p>The key to staying comfortable is layering. You'll need base layers, insulation, and waterproof shells.</p><h2>Footwear</h2><p>Quality trekking boots are essential. Break them in before your trip!</p><h2>Gear Checklist</h2><ul><li>Sleeping bag (-15°C rated)</li><li>Trekking poles</li><li>Headlamp</li><li>Water purification</li></ul>",
                "content_type": "guide",
                "tags": ["everest", "teahouse"],
                "region_slug": "everest-region",
                "linked_trip_slugs": ["everest-base-camp-trek"],
                "status": "published",
                "is_featured": True,
            },
            {
                "title": "Best Time to Trek in Nepal: A Complete Guide",
                "slug": "best-time-trek-nepal-complete-guide",
                "excerpt": "Discover the optimal seasons for trekking in Nepal. Learn about monsoon patterns, temperature ranges, and crowd levels for each region.",
                "content": "<h2>Peak Season: October-November</h2><p>The most popular time with stable weather and clear mountain views.</p><h2>Spring: March-May</h2><p>Rhododendrons bloom and temperatures are pleasant.</p><h2>Off-Season Options</h2><p>Winter and monsoon treks for adventurous travelers.</p>",
                "content_type": "guide",
                "tags": ["beginner"],
                "status": "published",
            },
            {
                "title": "Understanding Altitude Sickness: Prevention & Treatment",
                "slug": "altitude-sickness-prevention-treatment",
                "excerpt": "Learn how to recognize, prevent, and treat Acute Mountain Sickness (AMS). Essential reading before any high-altitude trek.",
                "content": "<h2>What is AMS?</h2><p>Acute Mountain Sickness occurs when you ascend too quickly without proper acclimatization.</p><h2>Symptoms</h2><ul><li>Headache</li><li>Nausea</li><li>Fatigue</li><li>Dizziness</li></ul><h2>Prevention</h2><p>The golden rule: climb high, sleep low.</p>",
                "content_type": "safety",
                "tags": ["everest", "annapurna"],
                "status": "published",
                "is_featured": True,
            },
            {
                "title": "Sherpa Culture: More Than Just Guides",
                "slug": "sherpa-culture-more-than-guides",
                "excerpt": "Discover the rich culture, traditions, and spiritual practices of the Sherpa people, the legendary mountain guides of the Himalayas.",
                "content": "<h2>Origins</h2><p>The Sherpa people migrated from Tibet over 500 years ago.</p><h2>Buddhism</h2><p>Tibetan Buddhism is central to Sherpa life, with monasteries in every village.</p><h2>Modern Life</h2><p>Today, many Sherpas balance traditional practices with the trekking industry.</p>",
                "content_type": "culture",
                "tags": ["everest", "cultural"],
                "region_slug": "everest-region",
                "status": "published",
            },
        ]

        for data in posts_data:
            region_slug = data.pop("region_slug", None)
            region = Region.objects.filter(slug=region_slug).first() if region_slug else None
            tag_slugs = data.pop("tags", [])
            linked_trip_slugs = data.pop("linked_trip_slugs", [])

            post, created = BlogPost.objects.update_or_create(
                slug=data["slug"], defaults={**data, "author": author, "region": region, "published_at": timezone.now()}
            )

            tags = UniversalTag.objects.filter(slug__in=tag_slugs)
            post.related_tags.set(tags)

            trips = Trip.objects.filter(slug__in=linked_trip_slugs)
            post.linked_trips.set(trips)

        # Assign featured images to blog posts
        blog_images = {
            "everest-base-camp-packing-list-2025": "blog/featured/packing_list.png",
            "best-time-trek-nepal-complete-guide": "blog/featured/seasons.png",
            "altitude-sickness-prevention-treatment": "blog/featured/packing_list.png",
            "sherpa-culture-more-than-guides": "blog/featured/seasons.png",
        }
        for slug, img_path in blog_images.items():
            BlogPost.objects.filter(slug=slug).update(featured_image=img_path)

        self.stdout.write(f"  Created {len(posts_data)} blog posts with images")

    def _create_glossary_terms(self):
        from apps.glossary.models import Term

        terms_data = [
            {
                "name": "Acute Mountain Sickness",
                "slug": "acute-mountain-sickness",
                "abbreviation": "AMS",
                "definition": "A condition caused by ascending to high altitude too quickly, resulting in headache, nausea, and fatigue.",
                "detailed_explanation": "<p>AMS is the mildest form of altitude illness and typically occurs above 2,500m. Symptoms include headache, nausea, fatigue, and difficulty sleeping.</p><p>Prevention involves gradual ascent, proper hydration, and acclimatization days.</p>",
                "auto_link": True,
                "link_priority": 10,
            },
            {
                "name": "Teahouse",
                "slug": "teahouse",
                "abbreviation": "",
                "definition": "A mountain lodge in Nepal providing basic accommodation and meals for trekkers along popular routes.",
                "detailed_explanation": "<p>Teahouses are family-run lodges found throughout Nepal's trekking regions. They offer simple rooms with beds, blankets, and communal dining areas serving dal bhat and other local cuisine.</p>",
                "auto_link": True,
                "link_priority": 8,
            },
            {
                "name": "Sherpa",
                "slug": "sherpa",
                "abbreviation": "",
                "definition": "An ethnic group from the mountainous regions of Nepal, famous for their mountaineering skills.",
                "detailed_explanation": "<p>The Sherpa people are a Tibetan ethnic group living in the Himalayas. They are renowned worldwide for their mountaineering expertise and have played a crucial role in Himalayan expeditions since the early 20th century.</p>",
                "auto_link": True,
                "link_priority": 9,
            },
            {
                "name": "Dal Bhat",
                "slug": "dal-bhat",
                "abbreviation": "",
                "definition": "The traditional Nepali meal of lentil soup (dal) served with rice (bhat) and accompaniments.",
                "detailed_explanation": "<p>Dal bhat is the staple food of Nepal, typically served twice daily. It consists of rice, lentil soup, vegetable curry (tarkari), pickles (achar), and often includes meat for non-vegetarians.</p>",
                "auto_link": True,
                "link_priority": 5,
            },
            {
                "name": "Namaste",
                "slug": "namaste",
                "abbreviation": "",
                "definition": 'A traditional Nepali greeting meaning "I bow to the divine in you," accompanied by pressing palms together.',
                "detailed_explanation": "<p>Namaste is the most common greeting in Nepal. To perform it, press your palms together at chest level and slightly bow your head. It's a sign of respect used for both greeting and farewell.</p>",
                "auto_link": True,
                "link_priority": 4,
            },
            {
                "name": "Khumbu",
                "slug": "khumbu",
                "abbreviation": "",
                "definition": "The region of Nepal that is home to Mount Everest and the Sherpa people.",
                "detailed_explanation": "<p>Khumbu is a region in northeastern Nepal, part of the Solukhumbu District. It includes the world's highest peak, Mount Everest (8,849m), and is the ancestral homeland of the Sherpa people.</p>",
                "auto_link": True,
                "link_priority": 7,
            },
        ]

        for data in terms_data:
            Term.objects.update_or_create(slug=data["slug"], defaults=data)

        self.stdout.write(f"  Created {len(terms_data)} glossary terms")
