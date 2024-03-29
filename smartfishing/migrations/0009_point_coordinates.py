# Generated by Django 5.0.2 on 2024-03-05 18:33

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartfishing', '0008_remove_point_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(46.347141, 48.026459), geography=True, srid=4326),
        ),
    ]
