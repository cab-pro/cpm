# Generated by Django 2.2 on 2019-04-25 20:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cabinets_app', '0014_merge_20190425_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
