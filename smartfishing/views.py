import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.gis.geos import Point as pnt
from django.views.decorators.http import require_http_methods
from .models import Point, Photo

# Create your views here.

def home_page(request):
    return render(request, 'smartfishing/home.html')

def map_page(request):
    return render(request, 'smartfishing/map.html')

def locations_json(request):
    locations = Point.objects.select_related('user').all()
    locations_list = [{
        'name': location.name,
        'coordinates': [location.coordinates.y, location.coordinates.x],
        'description': location.description,
        'user': location.user.username
    } for location in locations]
    return JsonResponse(locations_list, safe=False)


@require_http_methods(["POST"])
def create_point(request):
    name = request.POST.get('name')
    coordinates_raw = json.loads(request.POST.get('coordinates'))
    coordinates = pnt(coordinates_raw['lng'], coordinates_raw['lat'])
    description = request.POST.get('description')
    type = request.POST.get('type')
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    new_point = Point(user=user, coordinates=coordinates, name=name, description=description, type=type)
    new_point.save()
    print(request.FILES.getlist('images'))
    if request.method == 'POST' and request.FILES.getlist('images'):
        for image_file in request.FILES.getlist('images'):
            photo = Photo(point=new_point, image=image_file)
            photo.save()
    response_data = {
        'name': name,
        'description': description,
        'coordinates': coordinates_raw,
        'type': type,
        'user': request.user.username
    }
    return JsonResponse(response_data, status=201)

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

