# Generated by Django 4.2.4 on 2023-08-29 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_alter_trip_truck'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='isDisable',
            field=models.BooleanField(default=False),
        ),
    ]