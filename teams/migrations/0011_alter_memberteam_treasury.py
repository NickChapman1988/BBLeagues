# Generated by Django 4.2.7 on 2023-11-30 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_player_player_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberteam',
            name='treasury',
            field=models.IntegerField(default=1000000),
        ),
    ]
