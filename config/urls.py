from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.users.views import login_view, logout_view, register_view, register_api_view, dashboard_view, profile_view, edit_profile_view, user_profile_view, settings_view, change_password_view, delete_account_view
from apps.matching.views import matching_view
from apps.feed.views import my_ads_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentification - Version 1: directe (recommandée)
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('api/register/', register_api_view, name='register_api'),
    
    # OU Version 2: avec namespace (si vous préférez)
    # path('users/', include('apps.users.urls')),  # Décommentez si vous avez apps/users/urls.py
    
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Profil
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/user/<int:user_id>/', user_profile_view, name='user_profile'),
    path('settings/', settings_view, name='settings'),
    path('settings/password/', change_password_view, name='change_password'),
    path('settings/delete/', delete_account_view, name='delete_account'),
    
    # Matching
    path('matching/', matching_view, name='matching'),
    
    # Sessions
    path('sessions/', include('apps.mentorsessions.urls')),
    
    # Chat / Messagerie
    path('chat/', include('apps.messaging.urls')),
    
    # Feed
    path('feed/', include('apps.feed.urls')),
    
    # Mes annonces
    path('my-feed/', my_ads_view, name='my_feed'),
    
    # Pages statiques
    path('', TemplateView.as_view(template_name='pages/index.html'), name='home'),
    path('404/', TemplateView.as_view(template_name='pages/404.html'), name='404'),
    path('start/', TemplateView.as_view(template_name='pages/empty_dashboard.html'), name='start'),
    path('academic-profile/', TemplateView.as_view(template_name='pages/academic-profile.html'), name='academic_profile'),

    path('legal/cgu/', TemplateView.as_view(template_name='pages/legal_cgu.html'), name='legal_cgu'),
    path('legal/confidentialite/', TemplateView.as_view(template_name='pages/legal_confidentialite.html'), name='legal_confidentialite'),
    path('legal/mentions/', TemplateView.as_view(template_name='pages/legal_mentions.html'), name='legal_mentions'),
]