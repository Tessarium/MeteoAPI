from rest_framework import generics, mixins
from .models import Location, Temperature
from .serializers import LocationSerializer, TemperatureSerializer

import datetime
from datetime import datetime as dt


class ListLocationsView(generics.ListCreateAPIView):
    """
    Provides a get and a post methods handlers of locations.
    GET locations/
    POST locations/
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class DetailLocationsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides a get, a put and a delete methods handlers of a location.
    GET locations/:id/
    PUT locations/:id/
    PATCH locations/:id/
    DELETE locations/:id/
    HEAD locations/:id/
    OPTIONS locations/:id/
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ListTemperaturesView(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    """
    Provides a get and a post methods handlers of temperatures.
    GET temperatures/
    POST temperatures/
    """
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned temperatures to dates,
        by filtering against a `date` query parameter in the URL.
        """
        queryset = Temperature.objects.all()
        date = self.request.query_params.get('date', None)
        date_start = self.request.query_params.get('date_start', None)
        date_end = self.request.query_params.get('date_end', None)

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


# slightly different realization
class ListTemperaturesInLocationView(generics.ListAPIView):
    """
    Provides a get and a post methods handlers of temperatures in a location.
    GET temperatures/location/:id_location/
    """
    serializer_class = TemperatureSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        pk = self.kwargs['pk']
        return Temperature.objects.filter(location__pk=pk)


class DetailTemperaturesView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides a get, a put and a delete method handlers of a temperature.
    GET temperatures/:id/
    PUT temperatures/:id/
    PATCH temperature/:id/
    DELETE temperatures/:id/
    HEAD temperature/:id/
    OPTIONS temperatures/:id/
    """
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


