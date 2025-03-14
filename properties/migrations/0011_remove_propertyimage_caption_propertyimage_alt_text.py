# Generated by Django 4.2.7 on 2025-01-23 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_translation_en_alter_translation_es'),
        ('properties', '0010_remove_property_description_property_description_en_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyimage',
            name='caption',
        ),
        migrations.AddField(
            model_name='propertyimage',
            name='alt_text',
            field=models.OneToOneField(default=None, help_text='Texto que se mostrará si la imagen no carga (recomendado para SEO)', on_delete=django.db.models.deletion.CASCADE, to='core.translation', verbose_name='Texto alternativo'),
            preserve_default=False,
        ),
    ]
