# Generated by Django 4.2 on 2024-10-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(choices=[('0', 'Unranked'), ('1', 'Iron'), ('2', 'Bronze'), ('3', 'Silver'), ('4', 'Gold'), ('5', 'Platinum'), ('6', 'Amarald'), ('7', 'Diamond'), ('8', 'Master'), ('9', 'Grand Master'), ('10', 'Challenger')], max_length=2)),
                ('server', models.CharField(choices=[('KR', 'KR1'), ('LAN', 'LA1'), ('LAS', 'LA2'), ('RU', 'RU1'), ('NA', 'NA1'), ('BR', 'BR1'), ('OCE', 'OC1'), ('EUNE', 'EUN1'), ('EUW', 'EUW1'), ('JP', 'JP1'), ('TR', 'TR1'), ('SG', 'SG2'), ('TH', 'TH2'), ('PH', 'PH2'), ('ME', 'ME1')], max_length=4)),
                ('language', models.CharField(choices=[('KR', '한국어'), ('EN', 'ENGLISH'), ('JP', '日本語')], max_length=2)),
                ('age', models.CharField(choices=[('10', '청소년'), ('20', '청년'), ('30', '중년'), ('40', '중장년')], max_length=2)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_rank', models.BooleanField(default=False)),
            ],
        ),
    ]
