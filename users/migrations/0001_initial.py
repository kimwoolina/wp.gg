# Generated by Django 4.2 on 2024-10-04 15:06

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('username', models.CharField(max_length=15, unique=True)),
                ('riot_username', models.CharField(blank=True, max_length=15, null=True)),
                ('riot_tag', models.CharField(blank=True, max_length=15, null=True)),
                ('discord_username', models.CharField(blank=True, max_length=15, null=True)),
                ('discord_tag', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('credit_info', models.PositiveIntegerField(blank=True, null=True)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('score', models.FloatField(default=0.0)),
                ('is_notified', models.BooleanField(default=False)),
                ('is_blacklist', models.BooleanField(default=False)),
                ('riot_tier', models.CharField(blank=True, max_length=15, null=True)),
                ('is_notification_sound_on', models.BooleanField(default=True)),
                ('is_notification_message_on', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.platform')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kindness', models.IntegerField(default=0)),
                ('teamwork', models.IntegerField(default=0)),
                ('communication', models.IntegerField(default=0)),
                ('mental_strength', models.IntegerField(default=0)),
                ('punctuality', models.IntegerField(default=0)),
                ('positivity', models.IntegerField(default=0)),
                ('mvp', models.IntegerField(default=0)),
                ('mechanical_skill', models.IntegerField(default=0)),
                ('operation', models.IntegerField(default=0)),
                ('negativity', models.IntegerField(default=0)),
                ('profanity', models.IntegerField(default=0)),
                ('afk', models.IntegerField(default=0)),
                ('cheating', models.IntegerField(default=0)),
                ('verbal_abuse', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='platforms',
            field=models.ManyToManyField(related_name='users', through='users.UserPlatform', to='users.platform'),
        ),
        migrations.AddField(
            model_name='user',
            name='positions',
            field=models.ManyToManyField(blank=True, related_name='user', to='users.positions'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='userplatform',
            constraint=models.UniqueConstraint(fields=('user', 'platform'), name='unique_user_platform'),
        ),
    ]
