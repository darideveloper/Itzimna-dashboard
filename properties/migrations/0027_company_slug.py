# Generated by Django 4.2.7 on 2025-05-07 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0026_remove_company_details_company_banner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=255, null=True, unique=True, verbose_name='Slug'),
        ),
    ]
