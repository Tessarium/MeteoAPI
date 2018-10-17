from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Location, Temperature


# tests for models

class CreationTests(APITestCase):
    def test_create_location(self):
        """
        Ensure we can create a new location object.
        """
        url = reverse("list-locations-create", kwargs={"version": "v1"})
        data = {"name": "Tosno"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.get().name, "Tosno")

    def test_create_temperature(self):
        """
        Ensure we can create a new temperature object.
        """
        Location.objects.create(name="Tosno")
        url = reverse("list-temperatures-create", kwargs={"version": "v1"})
        time_now = timezone.now()

        data = {"location": 1,
                "scale": "\u2103",
                "value": 10,
                "date": time_now}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Temperature.objects.get().location.name, "Tosno")
        self.assertEqual(Temperature.objects.get().scale, "\u2103")
        self.assertEqual(Temperature.objects.get().value, 10)
        self.assertEqual(Temperature.objects.get().date, time_now)
