from .models import Rent
from django.utils.timezone import now


def update_rent_status():
    rents = Rent.objects.exclude(status=Rent.FINISHED)
    for rent in rents:
        if rent.rent_start == now().date():
            rent.status = Rent.ACTIVE
        elif rent.rent_end > now().date():
            rent.status = Rent.OVERDUE

        rent.save()
