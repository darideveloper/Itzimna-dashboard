# Generated by Django 4.2.7 on 2025-02-25 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0021_property_slug'),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='phone',
            field=models.CharField(default=0, max_length=15, verbose_name='Teléfono'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lead',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='done',
            field=models.BooleanField(default=False, verbose_name='Finalizado'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Correo Electrónico'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='message',
            field=models.CharField(max_length=300, verbose_name='Mensaje'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='properties.property', verbose_name='Propiedad'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Actualizado'),
        ),
    ]
