from celery import shared_task
from django.core.mail import send_mail

from root import settings


@shared_task
def send_verify_code(receiver, code):
    subject = "Verification code"
    msg = f"Code: {code}. This code is valid only 5 minutes."
    send_mail(subject=subject,
              message=msg,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[receiver])
    return {'status': f"Success : {receiver}"}
