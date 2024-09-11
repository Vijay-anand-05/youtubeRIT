from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StaffLoginForm, StaffRegistrationForm

def home(request):
    """Render the home page."""
    return render(request, "index.html")

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
