# apps/feed/urls.py
from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('create/', views.create_annonce, name='create_annonce'),
    path('<int:annonce_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:annonce_id>/apply/', views.apply_to_annonce, name='apply_to_annonce'),
    path('<int:annonce_id>/candidature/', views.get_candidature_form, name='get_candidature_form'),
    path('<int:annonce_id>/get/', views.get_annonce_json, name='get_annonce'),
    path('<int:annonce_id>/edit/', views.edit_annonce, name='edit_annonce'),
    path('<int:annonce_id>/archive/', views.archive_annonce, name='archive_annonce'),
    path('<int:annonce_id>/delete/', views.delete_annonce, name='delete_annonce'),
]