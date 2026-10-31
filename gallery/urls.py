from django.urls import path
from . import views

urlpatterns = [
    path('enter/', views.enter_view, name='enter'),
    path('lock/', views.lock_view, name='lock'),
    path('', views.gallery_list_view, name='gallery'),
    path('photo/<int:photo_id>/delete/', views.photo_delete_view, name='photo_delete'),
    path('upload/', views.photo_upload_view, name='photo_upload'),
]
