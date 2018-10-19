from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from .models import Location, Temperature
from .serializers import LocationSerializer, TemperatureSerializer

import datetime
from datetime import datetime as dt


class ListLocationsView(generics.ListCreateAPIView):
    """
    Provides a get and a post methods handlers of locations.

    get:
    Returns all locations.

    post:
    Creates a new location object.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class DetailLocationsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Request with the primary key of the location object.

    get:
    Returns the location.

    put:
    Updates the location.

    patch:
    Partial updates the location.

    delete:
    Deletes the location.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ListTemperaturesView(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    """
    Provides a get and a post methods handlers of temperatures.

    get:
    Returns all temperatures.
    It returns all temperatures in a range of 3 days by adding parameter
    'date' (ex. 2018-10-23). It returns all temperatures in the
     specified range by adding a 'date_start' and a 'date_end' parameters.

    post:
    Creates a new temperature.
    """
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned temperatures,
        by filtering against a 'date', a 'date_start' and a 'date_end'
        query parameter in the URL.
        """
        queryset = Temperature.objects.all()

        date = self.request.query_params.get("date", None)
        date_start = self.request.query_params.get("date_start", None)
        date_end = self.request.query_params.get("date_end", None)

        if date is not None:
            queryset = queryset.filter(date__startswith=date)
        elif date_start is not None:
            if date_end is not None:
                queryset = queryset.filter(date__range=(date_start, date_end))
            else:
                queryset = queryset.filter(date__range=(date_start,
                                                        dt.strptime(date_start, "%Y-%m-%d") +
                                                        datetime.timedelta(days=3)))

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListTemperaturesInLocationView(generics.ListAPIView):
    """
    Provides a get method handler of the temperatures
    in the specified location.

    get:
    Returns all temperatures in the location.
    """
    serializer_class = TemperatureSerializer

    def get_queryset(self):
        """
        Returns a list of all temperatures in the specified location.
        """
        pk = self.kwargs["pk"]
        return Temperature.objects.filter(location__pk=pk)


class DetailTemperaturesView(generics.RetrieveUpdateDestroyAPIView):
    """
    Request with the primary key of the temperature object.

    get:
    Returns the temperature.
    It returns converted value with specified scale,
    by adding parameter of the scale (allowed - 'K', '\u2103', '\u2109').

    put:
    Updates the temperature.

    patch:
    Partial updates the temperature.

    delete:
    Deletes the temperature
    """
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    def get_object(self):
        """
        Optionally converts the returned temperatures
        by adding against a `scale` query parameter.
        """
        queryset = self.get_queryset()
        filter_by_pk = {"pk": self.kwargs["pk"]}
        temperature = get_object_or_404(queryset, **filter_by_pk)

        scale = self.request.query_params.get("scale", None)

        if scale is not None:
            if not temperature.scale == scale:
                temperature.value = float(temperature.value)
                if scale == "K":
                    if temperature.scale == "\u2103":
                        temperature.value += 273.15
                    else:
                        temperature.value = (temperature.value + 459.67) / 1.8
                    temperature.scale = "K"
                elif scale == "\u2103":
                    if temperature.scale == "K":
                        temperature.value -= 273.15
                    else:
                        temperature.value = (temperature.value - 32) / 1.8
                    temperature.scale = "\u2103"
                elif scale == "\u2109":
                    if temperature.scale == "K":
                        temperature.value = temperature.value * 1.8 - 459.67
                    else:
                        temperature.value = temperature.value * 1.8 + 32
                    temperature.scale = "\u2109"
                else:
                    temperature.scale = "Invalid scale: " + scale + \
                                        " (possible variants are 'K', '\u2103', '\u2109'.)"
                    temperature.value = None

        return temperature
