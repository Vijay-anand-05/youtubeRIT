from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StaffLoginForm, StaffRegistrationForm

# def home(request):
    
#     return render(request, "index.html")

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('dashboard')  # Redirect to the dashboard or another page after registration
    else:
        form = StaffRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def staff_login(request):
    if request.method == 'POST':
        form = StaffLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard or another page after login
            else:
                messages.error(request, "Invalid staff ID or password.")
    else:
        form = StaffLoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required  # Ensure only logged-in users can access the dashboard
def dashboard(request):
    """Render the dashboard page."""
    
    return render(request, 'dashboard.html')

def staff_logout(request):
    """Handle user logout."""
    logout(request)
    return redirect('staff_login')  # Redirect to login page after logout



#---------------------------


from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoUploadForm
from django.contrib.auth.decorators import login_required
from urllib.request import urlretrieve
from django.core.files import File
import os
from django.conf import settings

# Home Page - Show all videos
def home(request):
    videos = Video.objects.all()
    return render(request, 'index.html', {'videos': videos})

# Dashboard Page - Show user-specific videos
@login_required
def dashboard(request):
    user_videos = Video.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user_videos': user_videos})

# Upload Page - Separate page for uploading videos
import os
import requests
from django.core.files import File
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()

            # Generate and save thumbnail
            thumbnail_url = video.get_youtube_thumbnail_url()
            thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f"{video.id}.jpg")

            try:
                response = requests.get(thumbnail_url)
                response.raise_for_status()  # Check if the request was successful
                with open(thumbnail_path, 'wb') as f:
                    f.write(response.content)

                # Save the thumbnail file to the Video model
                with open(thumbnail_path, 'rb') as f:
                    video.thumbnail.save(f"{video.id}.jpg", File(f), save=True)

            except requests.RequestException as e:
                # Handle the error (e.g., log it or use a default thumbnail)
                print(f"Error fetching thumbnail: {e}")
                video.thumbnail = None  # Or set to a default image

            video.save()  # Ensure changes are saved to the database

            return redirect('dashboard')
    else:
        form = VideoUploadForm()

    return render(request, 'upload_video.html', {'form': form})




# Category Page - Show videos by category
def category_videos(request, category_name):
    videos = Video.objects.filter(category=category_name)
    return render(request, 'category_videos.html', {'category_name': category_name, 'videos': videos})

# Video Detail - Show video details and embed YouTube video
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    youtube_video_id = video.youtube_url.split('v=')[-1]
    context = {
        'video': video,
        'youtube_video_id': youtube_video_id
    }
    return render(request, 'video_detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Video

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Extract YouTube video ID for embedding
    if video.youtube_url:
        video_id = video.youtube_url.split('v=')[-1]
        # Handle possible additional parameters in URL
        video_id = video_id.split('&')[0]
    else:
        video_id = None

    return render(request, 'video_detail.html', {
        'video': video,
        'video_id': video_id
    })

