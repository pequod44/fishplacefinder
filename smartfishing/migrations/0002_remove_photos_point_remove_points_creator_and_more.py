# Generated by Django 5.0.2 on 2024-02-21 09:24

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartfishing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='point',
        ),
        migrations.RemoveField(
            model_name='points',
            name='Creator',
        ),
        migrations.RemoveField(
            model_name='fish',
            name='point',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='point',
        ),
        migrations.RenameField(
            model_name='fish',
            old_name='Fish_Type',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='Equipment_Type',
        ),
        migrations.AddField(
            model_name='equipment',
            name='name',
            field=models.CharField(default='Снасти', max_length=30, verbose_name='Инструмент'),
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Наименование точки')),
                ('coordinates', models.CharField(max_length=50, verbose_name='Координаты точки')),
                ('description', models.CharField(max_length=128, verbose_name='Описание точки')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания точки')),
                ('type', models.CharField(max_length=128, verbose_name='Тип точки')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Фото')),
                ('point_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartfishing.point')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания комментария')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('point_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartfishing.point')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='point_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='smartfishing.point'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fish',
            name='point_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='smartfishing.point'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='Photos',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='Points',
        ),
    ]