from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from .models import Advertisement

class PostForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('name', 'image', 'description', 'phone', 'price', 'category', 'address', 'year', 'area', 'active')
        image = forms.ImageField()

class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]