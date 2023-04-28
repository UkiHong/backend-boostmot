# Generated by Django 4.2 on 2023-04-21 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('direct_messages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='direct_messages.chattingroom'),
        ),
    ]
