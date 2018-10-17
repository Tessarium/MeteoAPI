from rest_framework import serializers
from .models import Location, Temperature


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name")


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"

