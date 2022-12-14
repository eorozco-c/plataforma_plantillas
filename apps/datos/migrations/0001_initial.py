# Generated by Django 4.0.6 on 2022-08-11 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plantillas', '0001_initial'),
        ('parametros', '0001_initial'),
        ('puntos_medicion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(blank=True, null=True)),
                ('fecha', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parametro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametros.parametro')),
                ('plantilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plantillas.plantilla')),
                ('punto_medicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puntos_medicion.puntomedicion')),
            ],
        ),
    ]
