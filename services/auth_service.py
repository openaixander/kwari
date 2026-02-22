from django.db import transaction
from accounts.models import CustomUser
from accounts.tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode


class AuthService:

    @classmethod
    @transaction.atomic
    def register_user(cls, email, password): # Added cls
        display_name = email.split('@')[0]

        # We pass is_active=False directly to save a DB hit!
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            display_name=display_name,
            is_active=False 
        )
        return user
    
    @classmethod
    @transaction.atomic
    def activate_user(cls, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is None:
            return False, "Invalid activation link."
        
        if user.is_active:
            return True, "Account is already active."
        
        # USE CUSTOM GENERATOR HERE
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return True, "Account successfully activated."
        else:
            return False, "Activation link expired."