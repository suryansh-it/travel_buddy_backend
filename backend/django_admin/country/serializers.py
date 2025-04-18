from rest_framework import serializers
from .models import Country, TravelApp, AppCategory, Review, AppScreenshot

class TravelAppSerializer(serializers.ModelSerializer):
    platforms = serializers.SerializerMethodField()

    class Meta:
        model = TravelApp
        fields = ['id', 'name', 'description', 'icon_url', 'ios_link', 'android_link', 'platforms'
                  , "screenshots", "reviews"]

    def get_platforms(self, obj):
        return [
            "iOS" if obj.ios_link else None,
            "Android" if obj.android_link else None
        ]

class AppCategorySerializer(serializers.ModelSerializer):
    apps = TravelAppSerializer(many=True)  # Fetch related apps

    class Meta:
        model = AppCategory
        fields = ['name', 'apps']  # Each category will have a name and its apps

class CountrySerializer(serializers.ModelSerializer):
     # categories are added dynamically based on available apps
    curated_app_categories = serializers.SerializerMethodField() 
    flag = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['name', 'flag', 'description', 'curated_app_categories']

    def get_flag(self, obj):
        return obj.flag.url if obj.flag else None  # Ensure flag URL is returned properly


    def get_curated_app_categories(self, obj):
        """
        Get distinct categories from TravelApps related to the country.
        """
        categories = AppCategory.objects.filter(
            apps__country=obj
        ).distinct()
        
        return AppCategorySerializer(categories, many=True).data


class AppScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppScreenshot
        fields = ["image_url"]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["user_id", "rating", "review_text", "created_at"]
