# Generated by Django 4.2.7 on 2023-11-28 17:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_alter_position_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='ag',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(6)]),
        ),
    ]