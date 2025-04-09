# Generated by Django 4.2.7 on 2025-04-09 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0001_initial'),
        ('properties', '0023_tag_property_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='translations.translation', verbose_name='Nombre de la etiqueta'),
        ),
    ]
