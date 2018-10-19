from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "locations"


class Temperature(models.Model):
    KELVIN = 'K'
    CELSIUS = '\u2103'
    FAHRENHEIT = '\u2109'

    SCALE_CHOICES = (
        (KELVIN, 'Kelvin'),
        (CELSIUS, 'Celsius'),
        (FAHRENHEIT, 'Fahrenheit'),
    )

    location = models.ForeignKey(Location, verbose_name="location",
                                 on_delete=models.CASCADE, blank=False)
    scale = models.CharField(max_length=2, choices=SCALE_CHOICES, default=KELVIN,
                             blank=False, null=False)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False, null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return "{}{}".format(self.value, self.scale)
