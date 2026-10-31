from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Photo, GallerySettings
from .auth import gallery_authenticated
from django.core.cache import cache


def enter_view(request):
    if request.session.get('gallery_authenticated'):
        return redirect('gallery')

    error = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        settings_obj = GallerySettings.objects.first()

        if settings_obj:
            is_valid = False
            # Check hashed password (set via management command)
            if check_password(password, settings_obj.password_hash):
                is_valid = True
            # Fallback: plain-text match (set via admin panel)
            elif password == settings_obj.password_hash:
                is_valid = True

            if is_valid:
                request.session['gallery_authenticated'] = True
                return redirect('gallery')
            else:
                error = "Incorrect password."

    return render(request, 'gallery/enter.html', {'error': error})


@require_POST
def lock_view(request):
    if 'gallery_authenticated' in request.session:
        del request.session['gallery_authenticated']
    return redirect('enter')


@gallery_authenticated
def gallery_list_view(request):
    context = {}

    photos = cache.get("photos")

    if photos is None:
        photos = list(
            Photo.objects.all().order_by("?")
        )
        cache.set("photos", photos, timeout=300)
        
    return render(request, 'gallery/gallery.html',  {'photos': photos} )


@gallery_authenticated
@require_POST
def photo_delete_view(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    # Cloudinary deletion is handled by django-cloudinary-storage automatically
    photo.delete()
    cache.delete("photos")  # Clear the cache after deletion
    return redirect('gallery')


@gallery_authenticated
def photo_upload_view(request):

    uploaded = 0
    errors = []

    if request.method == 'POST':
        files = request.FILES.getlist('images')

        if not files:
            errors.append("No images were selected.")
        else:
            for f in files:
                try:
                    Photo.objects.create(image=f)
                    uploaded += 1
                except Exception as e:
                    errors.append(f"{f.name}: {e}")

        if uploaded and not errors:
            cache.delete("photos")  # Clear the cache after upload
            return redirect('gallery')

    return render(request, 'gallery/upload.html', {
        'uploaded': uploaded,
        'errors': errors,
    })
