# apps/mentorsessions/urls.py
from django.urls import path
from . import views

app_name = 'mentorsessions'

urlpatterns = [
    path('', views.sessions_list, name='list'),
    path('<int:session_id>/', views.session_detail, name='detail'),
    path('<int:session_id>/feedback/', views.submit_feedback, name='feedback'),
    path('<int:session_id>/accept/', views.accept_session, name='accept'),
    path('<int:session_id>/cancel/', views.cancel_session, name='cancel'),
    path('<int:session_id>/complete/', views.complete_session, name='complete'),
]