import requests
from rest_framework import serializers
from .models import TravelProject, Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "external_id", "notes", "is_visited", "project"]

    def validate_external_id(self, value):
        api_url = f"https://api.artic.edu/api/v1/artworks/{value}"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code != 200:
                raise serializers.ValidationError(
                    "Цього об'єкта не існує в Art Institute API."
                )
        except requests.exceptions.RequestException:
            raise serializers.ValidationError("Сервіс перевірки тимчасово недоступний.")
        return value

    def validate(self, data):
        project = data.get("project")
        if self.instance is None:
            if project and project.places.count() >= 10:
                raise serializers.ValidationError(
                    "У проекті не може бути більше 10 місць."
                )

        external_id = data.get("external_id")
        if project and project.places.filter(external_id=external_id).exists():
            raise serializers.ValidationError("Це місце вже додано до вашого проекту.")

        return data


class TravelProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, read_only=True)

    class Meta:
        model = TravelProject
        fields = ["id", "name", "description", "start_date", "is_completed", "places"]
