# Generated by Django 4.2.7 on 2023-11-29 18:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_memberteam_player_memberteam_players_memberteam_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberteam',
            name='player_qty',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(16)]),
        ),
        migrations.AddField(
            model_name='memberteam',
            name='reroll_qty',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)]),
        ),
        migrations.AddField(
            model_name='memberteam',
            name='team_value',
            field=models.IntegerField(default=0),
        ),
    ]