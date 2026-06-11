# apps/messaging/urls.py
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversations_list, name='conversations_list'),
    path('new/', views.new_conversation, name='new_conversation'),
    
    # Redirection pour l'ancienne URL
    path('new/<int:user_id>/', views.conversation_with, name='new_redirect'),
    
    # URL principale
    path('with/<int:user_id>/', views.conversation_with, name='conversation_with'),
    
    # API
    path('api/send/<int:user_id>/', views.send_message, name='send_message'),
    path('api/poll/<int:user_id>/', views.get_new_messages, name='get_new_messages'),
    path('api/typing/<int:user_id>/', views.typing_indicator, name='typing_indicator'),
    path('api/stop-typing/<int:user_id>/', views.stop_typing, name='stop_typing'),
    path('api/users/', views.get_users_list, name='get_users_list'),
]