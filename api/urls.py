from django.urls import path
from .views import *


urlpatterns = [
    path('locations/', ListLocationsView.as_view(), name="list-locations-create"),
    path('locations/<int:pk>', DetailLocationsView.as_view(), name="detail-location"),
    path('temperatures/', ListTemperaturesView.as_view(), name="list-temperatures-create"),
    path('temperatures/<int:pk>', DetailTemperaturesView.as_view(), name="detail-temperature"),
    path('temperatures/location/<int:pk>/', ListTemperaturesInLocationView.as_view(), name="list-location-temperatures"),
]
