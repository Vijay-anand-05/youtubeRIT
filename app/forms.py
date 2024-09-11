# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Staff ID',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your staff ID'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )


# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StaffRegistrationForm(UserCreationForm):
    staff_id = forms.CharField(
        label='Staff ID',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your staff ID'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['staff_id', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }
    
    def clean_staff_id(self):
        staff_id = self.cleaned_data.get('staff_id')
        # Ensure the staff ID is unique (assuming it is used as a unique identifier)
        if User.objects.filter(username=staff_id).exists():
            raise forms.ValidationError("A user with this Staff ID already exists.")
        return staff_id
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['staff_id']  # Set the username to staff_id
        if commit:
            user.save()
        return user
