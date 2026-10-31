from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from gallery.models import GallerySettings
import getpass

class Command(BaseCommand):
    help = 'Sets the gallery password securely.'

    def handle(self, *args, **options):
        password = getpass.getpass('Enter new gallery password: ')
        confirm_password = getpass.getpass('Confirm new gallery password: ')

        if password != confirm_password:
            self.stdout.write(self.style.ERROR('Passwords do not match. Aborting.'))
            return

        if not password:
            self.stdout.write(self.style.ERROR('Password cannot be empty.'))
            return

        settings, created = GallerySettings.objects.get_or_create(id=1)
        settings.password_hash = make_password(password)
        settings.save()

        self.stdout.write(self.style.SUCCESS('Gallery password successfully updated.'))
