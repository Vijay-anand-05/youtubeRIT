# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.staff_register, name='staff_register'),
    path('login/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('upload_video/', views.upload_video, name="upload_video"),
    path('video/<int:video_id>/', views.play_video, name='play_video'),
]
