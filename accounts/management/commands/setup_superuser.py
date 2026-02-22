import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser automatically from Environment Variables if none exists.'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Pull credentials from the vault (.env or Render environment)
        email = os.environ.get('SUPERUSER_EMAIL')
        password = os.environ.get('SUPERUSER_PASSWORD')

        if not email or not password:
            self.stdout.write(self.style.WARNING("⚠️ SUPERUSER_EMAIL or SUPERUSER_PASSWORD not found in environment. Skipping..."))
            return

        # Check if ANY superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("✅ A Superuser already exists in the database. Skipping creation."))
        else:
            # Create the superuser using your custom model fields
            display_name = email.split('@')[0]
            
            User.objects.create_superuser(
                email=email,
                password=password,
                display_name=display_name
            )
            self.stdout.write(self.style.SUCCESS(f"🚀 Superuser {email} created successfully!"))