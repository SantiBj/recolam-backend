# Generated by Django 4.2.4 on 2023-10-31 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
