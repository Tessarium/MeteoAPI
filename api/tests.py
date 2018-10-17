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
        time_now = timezone.now()

        Location.objects.create(name="Tosno")

        url = reverse("list-temperatures-create", kwargs={"version": "v1"})
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


# tests for a get, a put and a delete methods
class ResponsesTests(APITestCase):
    def setUp(self):
        self.time_now = timezone.now()
        self.location = Location.objects.create(name="Tosno")
        self.temperature = Temperature.objects.create(location=self.location, scale="\u2103", value=10,
                                                      date=self.time_now)

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
        response = self.client.get(reverse("detail-temperature", kwargs={"version": "v1", "pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], 1)
        self.assertEqual(response.data["scale"], "\u2103")
        self.assertEqual(response.data["value"], "10.0")
        self.assertEqual(str(timezone.datetime.strptime(response.data["date"], "%Y-%m-%dT%H:%M:%S.%fZ")),
                         self.time_now.strftime("%Y-%m-%d %H:%M:%S.%f"))

    def test_response_locations(self):
        """
        Ensure we can get multiply location objects.
        """
        Location.objects.create(name="Tosno-2")
        Location.objects.create(name="Ushaki")

        response = self.client.get(reverse("list-locations-create", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_response_temperatures(self):
        """
        Ensure we can get multiply temperature objects.
        """
        Temperature.objects.create(location=self.location, scale="\u2103", value=-10, date=self.time_now)

        response = self.client.get(reverse("list-temperatures-create", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_response_temperatures_in_location(self):
        """
        Ensure we can get accurate information about temperatures in the location.
        """
        second_location = Location.objects.create(name="Tosno-2")
        Temperature.objects.create(location=self.location, scale="\u2103", value=-10, date=self.time_now)
        Temperature.objects.create(location=second_location, scale="K", value=10, date=self.time_now)

        response = self.client.get(reverse("list-temperatures-location", kwargs={"version": "v1", "pk": 1}))

        filtered_temperatures = [ord_dict for ord_dict in response.data if ord_dict["location"] == 1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(filtered_temperatures.__len__(), 2)

    def test_update_location(self):
        """
        Ensure we can update location object.
        """
        self.client.put(reverse("detail-location", kwargs={"version": "v1", "pk": 1}), data={"name": "Tosno-2"})
        response = self.client.get(reverse("detail-location", kwargs={"version": "v1", "pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'Tosno-2'})

    def test_update_temperature(self):
        """
        Ensure we can update temperature object.
        """
        response_put = self.client.put(reverse("detail-temperature", kwargs={"version": "v1", "pk": 1}),
                                       data={"location": 1, "scale": "K", "value": 5.3})
        response_get = self.client.get(reverse("detail-temperature", kwargs={"version": "v1", "pk": 1}))

        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data["id"], 1)
        self.assertEqual(response_get.data["scale"], "K")

    def test_delete_location(self):
        """
        Ensure we can delete location object.
        """
        response = self.client.delete(reverse("detail-location", kwargs={"version": "v1", "pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_temperature(self):
        """
        Ensure we can delete temperature object.
        """
        response = self.client.delete(reverse("detail-temperature", kwargs={"version": "v1", "pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
