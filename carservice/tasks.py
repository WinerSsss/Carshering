from django.utils.timezone import now
from celery import shared_task
from .models import Rent


@shared_task
def update_rent_status():
    pending_rents = Rent.objects.filter(status='PENDING', rent_start__lte=now().date())
    pending_rents.update(status='ACTIVE')

    active_rents = Rent.objects.filter(status='ACTIVE', rent_end__gt=now().date())
    active_rents.update(status='OVERDUE')

    return pending_rents, active_rents

# The task is scheduled to run every day at midnight.
