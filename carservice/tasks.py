from django.utils.timezone import now

from carservice.models import Rent


def update_status(self):
    rents = Rent.objects.exclude(status=Rent.FINISHED)
    for rent in rents:
        if rent.rent_start <= now().date() <= rent.rent_end:
            rent.status = Rent.ACTIVE
        elif now().date() > rent.rent_end:
            rent.status = Rent.OVERDUE
        rent.save()
