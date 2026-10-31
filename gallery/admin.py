from django.contrib import admin
from .models import Photo, GallerySettings


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    # list_display = ('id', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


@admin.register(GallerySettings)
class GallerySettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
