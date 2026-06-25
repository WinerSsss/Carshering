from celery import shared_task
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_rent_statuses():
    """
    Periodic task to update rent statuses based on current date.
    Runs every hour via Celery Beat.
    """
    from .models import Rent
    
    current_date = now().date()
    updated_count = 0
    
    # Update pending rents that should be active
    pending_rents = Rent.objects.filter(
        status=Rent.PENDING,
        rent_start__lte=current_date,
        close_rent=False
    )
    
    for rent in pending_rents:
        rent.status = Rent.ACTIVE
        rent.save(update_fields=['status'])
        updated_count += 1
    
    # Update active rents that are overdue
    overdue_rents = Rent.objects.filter(
        status=Rent.ACTIVE,
        rent_end__lt=current_date,
        close_rent=False
    )
    
    for rent in overdue_rents:
        rent.status = Rent.OVERDUE
        rent.save(update_fields=['status'])
        updated_count += 1
    
    logger.info(f"Updated {updated_count} rent statuses")
    return f"Updated {updated_count} rent statuses"


@shared_task
def cleanup_expired_sessions():
    """
    Clean up expired sessions from the database.
    Runs daily at 3 AM via Celery Beat.
    """
    Session.objects.filter(expire_date__lt=now()).delete()
    logger.info("Cleaned up expired sessions")
    return "Expired sessions cleaned up"


@shared_task
def send_rent_reminder_email(rent_id):
    """
    Send reminder email to user about upcoming rent end date.
    """
    from .models import Rent
    from django.core.mail import send_mail
    from django.conf import settings
    
    try:
        rent = Rent.objects.select_related('user', 'offer__car').get(id=rent_id)
        
        subject = f"Reminder: Your rental ends on {rent.rent_end}"
        message = f"""
        Hello {rent.user.username},
        
        This is a reminder that your rental of {rent.offer.car.car_brand} {rent.offer.car.car_model}
        will end on {rent.rent_end}.
        
        Please make sure to return the vehicle on time.
        
        Best regards,
        TAKE&DRIVE Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [rent.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Sent reminder email for rent {rent_id}")
        return f"Reminder email sent for rent {rent_id}"
    
    except Rent.DoesNotExist:
        logger.error(f"Rent {rent_id} not found")
        return f"Rent {rent_id} not found"
    except Exception as e:
        logger.error(f"Error sending reminder email for rent {rent_id}: {str(e)}")
        raise


@shared_task
def generate_rent_report(rent_id):
    """
    Generate PDF report for a rent asynchronously.
    """
    from .models import Rent
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io
    
    try:
        rent = Rent.objects.select_related('user', 'offer__car').get(id=rent_id)
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Add content to PDF
        p.drawString(100, 750, f"Rent Confirmation - ID: {rent.id}")
        p.drawString(100, 730, f"User: {rent.user.username}")
        p.drawString(100, 710, f"Car: {rent.offer.car.car_brand} {rent.offer.car.car_model}")
        p.drawString(100, 690, f"Start Date: {rent.rent_start}")
        p.drawString(100, 670, f"End Date: {rent.rent_end}")
        p.drawString(100, 650, f"Duration: {rent.duration} days")
        p.drawString(100, 630, f"Price per day: ${rent.offer.price}")
        p.drawString(100, 610, f"Total: ${rent.offer.price * rent.duration}")
        p.drawString(100, 590, f"Status: {rent.status}")
        
        p.showPage()
        p.save()
        
        # Store in cache for retrieval
        cache.set(f'rent_report_{rent_id}', buffer.getvalue(), timeout=3600)
        
        logger.info(f"Generated report for rent {rent_id}")
        return f"Report generated for rent {rent_id}"
    
    except Rent.DoesNotExist:
        logger.error(f"Rent {rent_id} not found")
        return f"Rent {rent_id} not found"
    except Exception as e:
        logger.error(f"Error generating report for rent {rent_id}: {str(e)}")
        raise


@shared_task
def update_status():
    """
    Legacy task for backward compatibility.
    Calls the new update_rent_statuses task.
    """
    return update_rent_statuses()

# Made with Bob
