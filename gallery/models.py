from django.db import models
from cloudinary.models import CloudinaryField


class GallerySettings(models.Model):
    password_hash = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return "Gallery Settings"

    class Meta:
        verbose_name_plural = "Gallery Settings"


class Photo(models.Model):
    image = CloudinaryField('image', folder='private_gallery')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Photo {self.id}"

    def thumbnail_url(self):
        """Returns a Cloudinary-optimised thumbnail URL (800px wide, auto format)."""
        try:
            return self.image.url
        except:
            return ''

    def full_url(self):
        """Returns the full-quality Cloudinary URL."""
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f'{self.image.url}'

