import json
from django.contrib.gis.db import models as m
from smartfishing.models import Point
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from .forms import PointForm
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point as pnt
from django.views.decorators.http import require_http_methods

import folium
from folium import plugins

from .models import Point


# Create your views here.


def home_page(request):
    return render(request, 'smartfishing/home.html')

def map_page(request):
    # points = Point.objects.all()
    #
    # m = folium.Map(location=[46.347141, 48.026459], zoom_start=12)
    #
    # for point in points:
    #     spec = f"""
    #             <h1> {point.name}</h1>
    #             <p>Координаты: {point.coordinates[0]} {point.coordinates[1]}</p>
    #             <p>Доп. информация: {point.description}</p>
    #             """
    #     frame = folium.IFrame(html=spec, width=250, height=160)
    #     bloop = folium.Popup(frame,
    #                          max_width=2650)
    #
    #     folium.Marker(point.coordinates, popup=bloop).add_to(m)
    #
    # m.get_root().html.add_child(folium.Element("""
    #         <script>
    #         function onMapClick(e) {
    #             var userResponse = confirm('Установить маркер?');
    #             if (userResponse) {
    #                 var newMarker = L.marker(e.latlng).addTo(mymap);
    #                 newMarker.bindPopup("<b>Маркер установлен!</b>").openPopup();
    #             }
    #         }
    #
    #         mymap.on('click', onMapClick);
    #         </script>
    #     """))
    #
    # context = {'map': m._repr_html_()}
    # return render(request, 'smartfishing/map.html', context)


    # points = Point.objects.values('coordinates')
    # p=[]
    # for point in points:
    #     p.append({'latitude': point['coordinates'][0], 'longitude': point['coordinates'][1]})
    # context = {'points': p}
    # return render(request, 'smartfishing/map.html', context)


    return render(request, 'smartfishing/map.html')

def locations_json(request):
    locations = Point.objects.select_related('user').all()
    locations_list = [{
        'name': location.name,
        'coordinates': [location.coordinates.y, location.coordinates.x],
        'description': location.description,
        'user': location.user.username  # Добавляем никнейм пользователя
    } for location in locations]
    return JsonResponse(locations_list, safe=False)

# locations = Point.objects.select_related('user').all()

# 'user': location.user.username  # Добавляем никнейм пользователя

# @csrf_exempt
# def add_point(request):
#     if request.method == 'POST':
#         form = PointForm(request.POST)
#         if form.is_valid():
#             point = form.save(commit=False)
#             coordinates = form.cleaned_data['coordinates']
#             point.coordinates = fromstr(coordinates, srid=4326)
#             point.user = request.user  # Присваиваем текущего пользователя
#             point.save()
#             return JsonResponse({'success': 'Точка успешно добавлена.'})
#         else:
#             return JsonResponse({'error': 'Ошибка в данных формы.'}, status=400)
#     return JsonResponse({'error': 'Неверный запрос.'}, status=400)

@require_http_methods(["POST"])
def create_point(request):
    name = request.POST.get('name')
    coordinates_raw = json.loads(request.POST.get('coordinates'))
    coordinates = pnt(coordinates_raw['lng'], coordinates_raw['lat'])
    description = request.POST.get('description')
    type = request.POST.get('type')
    user = request.user  # Используйте request.user для получения текущего пользователя

    if not user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

    new_point = Point(user=user, coordinates=coordinates, name=name, description=description, type=type)
    new_point.save()
    response_data = {
        'name': name,
        'description': description,
        'coordinates': coordinates_raw,  # Возвращаем в формате, который был передан
        'type': type,
        'user': request.user.username
    }
    return JsonResponse(response_data, status=201)  # Возвращает JSON с данными точки и статусом 201 Created




    #     form = PointForm(request.POST)
    #     if form.is_valid():
    #         point = form.save(commit=False)
    #         point.user = request.user  # предполагаем, что пользователь уже аутентифицирован
    #         # здесь вы можете установить coordinates или другие поля, если это необходимо
    #         point.save()
    #         return redirect('smartfishing/map.html')  # перенаправление после успешного сохранения
    # else:
    #     form = PointForm()
    # return render(request, 'smartfishing/map.html', {'form': form})


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

