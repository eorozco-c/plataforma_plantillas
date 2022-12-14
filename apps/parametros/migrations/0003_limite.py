# Generated by Django 4.0.6 on 2022-11-09 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('puntos_medicion', '0001_initial'),
        ('parametros', '0002_alter_parametro_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Limite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limite', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parametro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parametros_limite', to='parametros.parametro')),
                ('punto_medicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puntos_medicion_limite', to='puntos_medicion.puntomedicion')),
            ],
        ),
    ]
