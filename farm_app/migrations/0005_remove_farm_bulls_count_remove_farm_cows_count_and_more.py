# Generated by Django 5.0.2 on 2024-02-11 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_app', '0004_remove_farm_bulls_remove_farm_cows_farm_bulls_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farm',
            name='bulls_count',
        ),
        migrations.RemoveField(
            model_name='farm',
            name='cows_count',
        ),
        migrations.AddField(
            model_name='farm',
            name='bulls',
            field=models.ManyToManyField(to='farm_app.bull'),
        ),
        migrations.AddField(
            model_name='farm',
            name='cows',
            field=models.ManyToManyField(to='farm_app.cow'),
        ),
    ]