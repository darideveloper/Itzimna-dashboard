# Generated by Django 4.2.7 on 2025-02-08 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0019_property_featured_alter_property_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nombre del desarrollo o propiedad'),
        ),
    ]
