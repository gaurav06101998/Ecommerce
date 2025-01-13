# forms.py

from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'address', 'phone']  # Exclude email, as it's handled by User model

    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the email field with the user's email
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        """ Override the save method to update the user's email """
        user = self.instance.user
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        profile = super().save(commit)
        return profile


