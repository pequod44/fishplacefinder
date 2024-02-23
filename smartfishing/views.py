from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
import folium

from .models import Point


# Create your views here.


def home_page(request):
    return render(request, 'smartfishing/home.html')

def map_page(request):
    points = Point.objects.all()

    m = folium.Map(location=[46.347141, 48.026459], zoom_start=12)

    for point in points:
        folium.Marker(point.coordinates, popup=point.name).add_to(m)

    context = {'map': m._repr_html_()}
    return render(request, 'smartfishing/map.html', context)

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

