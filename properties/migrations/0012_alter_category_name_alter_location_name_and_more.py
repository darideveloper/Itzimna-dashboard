# Generated by Django 4.2.7 on 2025-01-23 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0001_initial'),
        ('properties', '0011_remove_propertyimage_caption_propertyimage_alt_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='translations.translation', verbose_name='Nombre de la categoría'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='translations.translation', verbose_name='Nombre de la ubicación'),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='alt_text',
            field=models.OneToOneField(help_text='Texto que se mostrará si la imagen no carga (recomendado para SEO)', on_delete=django.db.models.deletion.CASCADE, to='translations.translation', verbose_name='Texto alternativo'),
        ),
    ]
