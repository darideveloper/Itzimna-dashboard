# Generated by Django 4.2.7 on 2025-03-06 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0021_property_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='google_maps_src',
            field=models.TextField(blank=True, help_text='Puedes insertar el iframe completo', null=True, verbose_name='src de Google Maps'),
        ),
    ]
