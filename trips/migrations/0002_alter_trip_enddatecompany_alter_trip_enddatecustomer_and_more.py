# Generated by Django 4.2.4 on 2023-08-29 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='endDateCompany',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='endDateCustomer',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='initialDateCompany',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='initialDateCustomer',
            field=models.DateTimeField(null=True),
        ),
    ]