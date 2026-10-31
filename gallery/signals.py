import cloudinary.uploader
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Photo


@receiver(post_delete, sender=Photo)
def delete_cloudinary_image(sender, instance, **kwargs):
    if instance.image:
        public_id = instance.image.public_id

        if public_id:
            cloudinary.uploader.destroy(public_id)