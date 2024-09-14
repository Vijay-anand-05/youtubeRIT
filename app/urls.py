# urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.staff_register, name='staff_register'),
    path('login/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('upload/', views.upload_video, name='upload_video'),
    path('category/<str:category_name>/', views.category_videos, name='category_videos'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
] 