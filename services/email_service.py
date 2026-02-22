from accounts.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
import logging

# This connects to the logger we are about to add in settings.py
logger = logging.getLogger(__name__)

class EmailService:
    @classmethod
    def send_activation_email(cls, user, domain, protocol):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        activation_link = f"{protocol}://{domain}/accounts/activate/{uid}/{token}/"
        
        subject = "Activate your Kwari Market Account"
        message = f"Hello {user.display_name},\n\nPlease click the link below to activate your account:\n{activation_link}"

        # We use logger.error so it forcefully prints to the Render console immediately!
        logger.error(f"⏳ Attempting to send sync email to {user.email}...")

        # We removed the EmailThread completely. This executes directly!
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False, 
        )
        
        logger.error(f"✅ SUCCESS: Email actually sent to {user.email}!")