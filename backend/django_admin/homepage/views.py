from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Destination  # To be created later


@api_view(['GET'])
def homepage_view(request):
    destinations = get_list_or_404(Destination.objects.all())  # Fetch from DB

    data = {
        "hero_section": {
            "search_placeholder": "Search for a country...",
            "cta_text": "Get Started"
        },
        "how_it_works": [
            "Choose a country",
            "Select the best travel apps",
            "Generate your QR code"
        ],
        "popular_destinations": [
            {"name": d.name, "image": d.image_url} for d in destinations
        ],
        "footer": {
            "about": "About Travel App Curator",
            "contact": "Contact Us",
            "privacy": "Privacy Policy",
            "social_links": [
                {"platform": "Twitter", "url": "https://twitter.com"},
                {"platform": "Facebook", "url": "https://facebook.com"}
            ]
        }
    }
    return Response(data)