# Generated by Django 4.2.7 on 2023-12-04 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_alter_memberteam_treasury'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberteam',
            old_name='apothecary',
            new_name='apothecary_qty',
        ),
    ]
