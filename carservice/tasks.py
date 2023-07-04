from django.utils.timezone import now
from celery import shared_task
from .models import Rent


@shared_task
def update_rent_status():
    pending_rents = Rent.objects.filter(status='pending', rent_start__lte=now().date())
    pending_rents.update(status='active')

    active_rents = Rent.objects.filter(status='active', rent_end__lt=now().date())
    active_rents.update(status='overdue')

    closed_rents = Rent.objects.filter(close_rent=True)
    for rent in closed_rents:
        rent.status = 'finished'
        rent.save()

    return pending_rents, active_rents, closed_rents

# The task is scheduled to run every day at midnight.
