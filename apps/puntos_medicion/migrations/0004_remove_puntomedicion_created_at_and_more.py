# Generated by Django 4.0.6 on 2022-07-27 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0001_initial'),
        ('puntos_medicion', '0003_remove_puntomedicion_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntomedicion',
            name='tipo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='puntos_medicion_tipo', to='plantillas.tipoplantilla'),
            preserve_default=False,
        ),
    ]
