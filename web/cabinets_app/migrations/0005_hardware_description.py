# Generated by Django 2.2 on 2019-04-23 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinets_app', '0004_auto_20190423_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardware',
            name='description',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]
