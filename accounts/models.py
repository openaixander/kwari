from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        

        # Normalize the email (lowercases the domain part)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)


        # this hashes the password securely before saving
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        # superusers must have these flags set to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Our Kwari Market custom user model
    """

    # remove the username field

    username = None

    # make email unique and required
    email = models.EmailField(_('email_address'), unique=True)

    # Add our custom display name field
    display_name = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS are for createsuperuser prompt. 
    # Email is automatically required by USERNAME_FIELD, so we leave this empty or add display_name if we want.
    REQUIRED_FIELDS = []


    # connect the custom manager

    objects = CustomUserManager()

    def __str__(self):
        return self.email

