from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models as m
from django.db import models
from django.contrib.gis.geos import Point as pnt


class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30,
        verbose_name="Наименование точки",
    )
    coordinates = m.PointField(geography=True, default=pnt(46.347141, 48.026459))
    description = models.CharField(
        max_length=128,
        verbose_name="Описание точки",
    )
    created_at = models.DateTimeField(
        default=datetime.now,
        verbose_name="Дата создания точки",
    )
    type = models.CharField(
        max_length=128,
        verbose_name="Тип точки",
    )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    message = models.TextField(
        verbose_name="Текст сообщения",
    )
    created_at = models.DateTimeField(
        default=datetime.now,
        verbose_name="Дата создания комментария",
    )

    def __str__(self):
        return f"{self.message}"


class Photo(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False, upload_to='photos/')


class Equipment(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30,
        verbose_name="Инструмент",
        default='Снасти'
    )


class Fish(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30,
        verbose_name="Вид рыбы",
    )
