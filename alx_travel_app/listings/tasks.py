from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(subject, message, recipient_list):
    """
    Sends a booking confirmation email to the user.
    """
    send_mail(
        subject,
        message,
        'noreply@alx_travel_app.com',  # The sender's email address
        recipient_list,
        fail_silently=False,
    )