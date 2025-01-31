# Generated by Django 4.2.7 on 2025-01-30 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0015_rename_key_shortdescription_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortdescription',
            name='en',
        ),
        migrations.RemoveField(
            model_name='shortdescription',
            name='es',
        ),
        migrations.RemoveField(
            model_name='shortdescription',
            name='name',
        ),
        migrations.AddField(
            model_name='shortdescription',
            name='details',
            field=models.TextField(blank=True, null=True, verbose_name='Detalles adicionales'),
        ),
        migrations.AlterField(
            model_name='property',
            name='short_description',
            field=models.ForeignKey(help_text='Descripción corta de la propiedad o desarrollo', on_delete=django.db.models.deletion.CASCADE, to='properties.shortdescription', verbose_name='Descripción corta'),
        ),
    ]
