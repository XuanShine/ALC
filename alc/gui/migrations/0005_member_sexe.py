# Generated by Django 3.2.2 on 2021-05-08 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0004_auto_20210508_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='sexe',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
