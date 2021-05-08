# Generated by Django 3.2.2 on 2021-05-08 02:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0008_auto_20210508_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='pec',
            name='date_debut',
            field=models.DateField(default=datetime.date(2021, 5, 8)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pec',
            name='date_fin',
            field=models.DateField(default=datetime.date(2021, 5, 8)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pec',
            name='derniere_date_facturee',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pec',
            name='famille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='PEC', to='gui.famille'),
        ),
    ]
