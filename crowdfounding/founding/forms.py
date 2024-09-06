from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'pictures', 'total_target', 'tags', 'start_time', 'end_time']

class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPicture
        fields = ['image']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating',)
        
        
        
        
        
        
        
        
# --------------------------------------------------------------------------------register











from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    mobile_phone = forms.CharField(max_length=11, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'mobile_phone', 'profile_picture']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 3:
            raise ValidationError("First name must be at least 3 characters long.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 3:
            raise ValidationError("Last name must be at least 3 characters long.")
        return last_name

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not re.match(r'^01[0-9]{9}$', mobile_phone):
            raise ValidationError("Please, use a valid Egyptian phone number.")
        return mobile_phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Please, enter a valid email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")







# ////////////////////////////////////////////////////////////////////////////////////////////////////

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required',widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "form-control"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))
