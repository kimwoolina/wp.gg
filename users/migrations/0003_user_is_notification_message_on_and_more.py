# Generated by Django 4.2 on 2024-09-30 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_riot_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_notification_message_on',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_notification_sound_on',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='riot_tag',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]