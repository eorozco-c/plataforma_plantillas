# Generated by Django 4.0.6 on 2022-08-18 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametro',
            name='descripcion',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
    ]
