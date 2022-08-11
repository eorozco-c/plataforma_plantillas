# Generated by Django 4.0.6 on 2022-08-11 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresas', '0001_initial'),
        ('plantillas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PuntoMedicion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(max_length=500)),
                ('activo', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puntos_medicion_empresa', to='empresas.empresa')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puntos_medicion_tipo', to='plantillas.tipoplantilla')),
            ],
        ),
    ]
