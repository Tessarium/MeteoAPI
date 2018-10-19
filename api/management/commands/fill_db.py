from django.core.management.base import BaseCommand
from api.models import Location, Temperature

import datetime
from datetime import datetime as dt
import random


class Command(BaseCommand):
    help = 'Filling the db with temperatures'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str,
                            help='Temperatures will be created since this date every 6 hours,'
                                 'format - YYYY-MM-DD'
                            )

    def handle(self, *args, **options):
        date = dt.strptime(options['date'], "%Y-%m-%d")
        locations = Location.objects.all()
        locations_count = locations.__len__()
        scales = ("K", "\u2103", "\u2109")
        plural = False

        if locations_count:
            if locations_count > 1:
                plural = True

            while date < dt.now():
                date += datetime.timedelta(hours=6)
                rand_dig = random.uniform(-1000, 1000)

                if plural:
                    Temperature.objects.create(location=locations[int(abs(rand_dig) % locations_count)],
                                               value=rand_dig, scale=scales[int(abs(rand_dig) % 3)],
                                               date=date)
                else:
                    Temperature.objects.create(location=locations[0], value=rand_dig,
                                               scale=scales[int(abs(rand_dig) % 3)],
                                               date=date)
        else:
            print("Location doesnt exist\n"
                  "Create locations")
