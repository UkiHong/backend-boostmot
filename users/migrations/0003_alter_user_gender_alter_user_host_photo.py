# Generated by Django 4.2 on 2023-04-08 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_gender_user_host_photo_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='host_photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
