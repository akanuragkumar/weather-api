from rest_framework import serializers

from project_api.models import CityWeatherCollection, MailingTask


class CityWeatherCollectionSerializer(serializers.Serializer):
    """Retrieve Serializer for CityWeatherCollection model."""

    city = serializers.CharField(required=True)
    current_temp = serializers.CharField(required=False)
    feels_like_temp = serializers.CharField(required=False)
    modified_on = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        # creating new movie collection
        collection = CityWeatherCollection.objects.create(city=validated_data['city'])
        return collection


class MailingCollectionSerializer(serializers.Serializer):
    """Retrieve Serializer for MailingCollection model."""

    emails = serializers.JSONField(required=True)

    def create(self, validated_data):
        # getting context of the user
        user = self.context.get('user')
        # creating new movie collection
        collection = MailingTask.objects.create(user=user, emails=validated_data['emails'])
        return collection
