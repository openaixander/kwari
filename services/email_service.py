import threading
from accounts.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

# 1. CREATE THE BACKGROUND THREAD CLASS
class EmailThread(threading.Thread):
    def __init__(self, subject, message, from_email, recipient_list):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        try:
            print(f"⏳ Attempting to send email to {self.recipient_list}...")
            send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
                fail_silently=False, # We want it to crash loudly if it fails!
            )
            print(f"✅ SUCCESS: Email sent to {self.recipient_list}!")
        except Exception as e:
            print(f"❌ CRITICAL EMAIL ERROR: {str(e)}")

class EmailService:
    @classmethod
    def send_activation_email(cls, user, domain, protocol):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        activation_link = f"{protocol}://{domain}/accounts/activate/{uid}/{token}/"
        
        subject = "Activate your Kwari Market Account"
        message = f"Hello {user.display_name},\n\nPlease click the link below to activate your account:\n{activation_link}"

        logger.error(f"⏳ Attempting to send sync email to {user.email}...")

        # We removed the thread! This happens instantly on the main process.
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False, 
        )
        
        logger.error(f"✅ SUCCESS: Email actually sent to {user.email}!")