from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from smartfishing.models import Point


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['name', 'description', 'type']  # 'coordinates' будут заполняться отдельно
