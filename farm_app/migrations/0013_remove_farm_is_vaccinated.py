# Generated by Django 5.0.2 on 2024-02-11 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm_app', '0012_remove_farm_vaccine_farm_vaccine1_farm_vaccine2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farm',
            name='is_vaccinated',
        ),
    ]