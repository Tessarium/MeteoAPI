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


# tests for responses
class ResponsesTests(APITestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Tosno")

    def test_response_location(self):
        """
        Ensure we can get necessary location info.
        """
        response = self.client.get(reverse("detail-location", kwargs={"version": "v1", "pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'Tosno'})

    def test_response_temperature(self):
        """
        Ensure we can get necessary temperature info.
        """
        time_now = timezone.now()

        Temperature.objects.create(location=self.location, scale="\u2103", value=10, date=time_now)
        response = self.client.get(reverse("detail-temperature", kwargs={"version": "v1", "pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], 1)
        self.assertEqual(response.data["scale"], "\u2103")
        self.assertEqual(response.data["value"], "10.0")
        self.assertEqual(str(timezone.datetime.strptime(response.data["date"], "%Y-%m-%dT%H:%M:%S.%fZ")),
                         time_now.strftime("%Y-%m-%d %H:%M:%S.%f"))
