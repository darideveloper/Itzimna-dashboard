# Generated by Django 4.2.7 on 2025-01-15 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_alter_property_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='active',
            field=models.BooleanField(default=True, help_text='Indica si la propiedad/desarrollo se mostrará en la página', verbose_name='Activo'),
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='property-images/', verbose_name='Imagen')),
                ('caption', models.CharField(blank=True, max_length=255, null=True, verbose_name='Pie de foto')),
                ('show_gallery', models.BooleanField(default=True, verbose_name='Mostrar en galería')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property', verbose_name='Propiedad')),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imágenes',
            },
        ),
    ]
