# Generated by Django 4.2 on 2023-04-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0006_workout_host_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='host_photo',
        ),
        migrations.AddField(
            model_name='workout',
            name='avatar',
            field=models.URLField(blank=True),
        ),
    ]
