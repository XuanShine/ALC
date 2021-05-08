# Generated by Django 3.2.2 on 2021-05-08 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0005_member_sexe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('adresse', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RenameModel(
            old_name='Family',
            new_name='Famille',
        ),
        migrations.RenameModel(
            old_name='Member',
            new_name='Membre',
        ),
    ]
