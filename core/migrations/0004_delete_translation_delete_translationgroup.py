# Generated by Django 4.2.7 on 2025-01-23 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_alter_category_name_alter_location_name_and_more'),
        ('core', '0003_alter_translation_en_alter_translation_es'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Translation',
        ),
        migrations.DeleteModel(
            name='TranslationGroup',
        ),
    ]
