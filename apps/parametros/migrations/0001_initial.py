# Generated by Django 4.0.6 on 2022-07-24 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plantillas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('abreviado', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parametros_tipo', to='plantillas.tipoplantilla')),
            ],
        ),
    ]
