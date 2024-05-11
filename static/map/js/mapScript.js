document.addEventListener('DOMContentLoaded', function() {
    let map = L.map('map').setView([46.347141, 48.026459], 14);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);
    // Отображенеи маркеров на карте
    fetch('/api/locations/')
      .then(response => response.json())
      .then(data => {
        data.forEach(function(location) {
          const marker = L.marker([location.coordinates[0], location.coordinates[1]])
            .addTo(map);

          marker.on('click', function() {
            // Обновляем содержимое кастомного окна
            document.getElementById('point-infoLabel').textContent = location.name; // Заголовок кастомного окна
            document.querySelector('#point-info .offcanvas-body').innerHTML = `
              <p>${location.user}</p>
              <p>${location.description}</p>
              <!-- Вставьте сюда любой дополнительный контент -->
            `;
            // Открываем кастомное окно
            const offcanvas = new bootstrap.Offcanvas(document.getElementById('point-info'));
            offcanvas.show();
          });
        });
      });

    let tempMarker;
    // добавление маркера на карту
    function onMapClick(e) {
      if (tempMarker) {
      map.removeLayer(tempMarker);
      }
      var popup = L.popup();
      console.log(e.latlng)
      let lat = e.latlng.lat;
      let lng = e.latlng.lng;
      let coordinates = {lat: lat, lng: lng};
      $('#coordinates').val(JSON.stringify(coordinates));
      popup
          .setLatLng(e.latlng)
          .setContent('<p>Установить точку здесь?<br/> <button id="addPointButton" class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBothOptions" aria-controls="offcanvasWithBothOptions">Добавить точку</button></p>')
          .openOn(map);
      }

    map.on('contextmenu click', onMapClick);

    map.on('popupopen', function(e) {
        $('#addPointButton').on('click', function() {
            // Закрыть текущий popup
            map.closePopup();
            if (tempMarker) {
                map.removeLayer(tempMarker);
            }

            // Создаём новый временный маркер на месте клика
            tempMarker = L.marker(e.popup.getLatLng()).addTo(map);

        });

    });

    map.on('move start', function() {
        map.closePopup();
    });

    // Закрыть всплывающее окно при изменении масштаба карты
    map.on('zoomstart', function() {
        map.closePopup();
    });
    // Отправка точки в бэк
    $(document).on('submit', '#post-form', function(e) {
        e.preventDefault();
        var formData = new FormData();
        formData.append('name', $('#point_name').val());
        formData.append('description', $('#description').val());
        formData.append('type', $('#type').val());
        formData.append('coordinates', $('#coordinates').val());
        formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        // Добавляем изображения к объекту FormData
        var images = $('#formFileMultiple')[0].files; // Получаем список выбранных файлов
        for (var i = 0; i < images.length; i++) {
            formData.append('images', images[i]);
        }
        $.ajax({
            type:'POST',
            url: 'create-point/',
            data:formData,
            contentType: false, // Указываем, что тип содержимого не должен быть установлен автоматически
            processData: false, // Указываем, что не нужно обрабатывать данные перед отправкой
            success: function(pointData) {
              // Добавляем маркер на карту для только что созданной точки
              const marker = L.marker([pointData.coordinates.lat, pointData.coordinates.lng])
                .addTo(map);

              // Назначаем обработчик клика на маркер
              marker.on('click', function() {
                // Обновляем содержимое кастомного окна
                document.getElementById('point-infoLabel').textContent = pointData.name; // Заголовок кастомного окна
                document.querySelector('#point-info .offcanvas-body').innerHTML = `
                  <p>${pointData.user}</p>
                  <p>${pointData.description}</p>
                  <!-- Добавьте сюда любой дополнительный контент, например ссылки или изображения -->
                `;
                // Открываем кастомное окно
                const offcanvas = new bootstrap.Offcanvas(document.getElementById('point-info'));
                offcanvas.show();
              });
              let offcanvasAddPoint = bootstrap.Offcanvas.getInstance(document.getElementById('offcanvasWithBothOptions'));
              if (offcanvasAddPoint) {
                  offcanvasAddPoint.hide();
              }
              $('#post-form').trigger('reset');

              marker.fire('click');

            }

        })
    })
    const offcanvasElement = document.getElementById('offcanvasWithBothOptions');

    offcanvasElement.addEventListener('hide.bs.offcanvas', function () {
      if (tempMarker) {
        map.removeLayer(tempMarker);
        tempMarker = null; // Обнуляем переменную, чтобы избежать попыток удаления уже несуществующего маркера
      }
    });


});


