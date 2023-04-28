# Generated by Django 4.2 on 2023-04-21 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0003_alter_experience_category'),
        ('workout', '0005_alter_workout_category_alter_workout_host'),
        ('medias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='experiences.experience'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='photo',
            name='workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='workout.workout'),
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.URLField(),
        ),
    ]
