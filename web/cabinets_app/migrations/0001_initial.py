# Generated by Django 2.2 on 2019-04-23 16:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('billing_address', models.CharField(max_length=1024)),
                ('billing_phone', models.CharField(max_length=32)),
                ('billing_email', models.EmailField(max_length=256)),
                ('contact_name', models.CharField(max_length=128)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=128)),
                ('width', models.DecimalField(decimal_places=2, max_digits=6)),
                ('height', models.DecimalField(decimal_places=2, max_digits=6)),
                ('depth', models.DecimalField(decimal_places=2, max_digits=6)),
                ('number_of_doors', models.IntegerField()),
                ('number_of_shelves', models.IntegerField()),
                ('finished_interior', models.BooleanField(default=False)),
                ('finished_left_end', models.BooleanField(default=False)),
                ('finished_right_end', models.BooleanField(default=False)),
                ('finished_top', models.BooleanField(default=False)),
                ('finished_bottom', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('cost_per', models.DecimalField(decimal_places=2, max_digits=6)),
                ('unit_type', models.CharField(choices=[('each', 'Each'), ('pair', 'Pair'), ('set', 'Set')], max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Labor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=128)),
                ('minutes', models.IntegerField()),
                ('units', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=4)),
                ('width', models.DecimalField(decimal_places=2, max_digits=6)),
                ('length', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sheet_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('waste_factor', models.DecimalField(decimal_places=2, max_digits=3)),
                ('markup', models.DecimalField(decimal_places=2, max_digits=3)),
                ('date_updated', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('physical_address', models.CharField(max_length=1024)),
                ('site_contact', models.CharField(max_length=128)),
                ('contact_phone', models.CharField(max_length=32)),
                ('contact_email', models.EmailField(max_length=256)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=6)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='cabinets_app.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('construction', models.CharField(choices=[('frameless', 'Frameless'), ('faceframe', 'Faceframe Overlay'), ('faceframe-inset', 'Faceframe Inset')], default='frameless', max_length=32)),
                ('catalog', models.CharField(choices=[('laminate', 'Laminate'), ('wood slab', 'Wood Slab'), ('wood 5-piece', 'Wood 5-Piece'), ('thermofoil', 'Thermofoil')], default='laminate', max_length=32)),
                ('finish_level', models.IntegerField(choices=[(0, 'Unfinished'), (3, 'Sand & Prep Only'), (6, 'Clear'), (8, 'Stain'), (12, 'Stain & Glaze'), (12, 'Stain & Distress'), (16, 'Stain, Glaze & Distress'), (10, 'Paint'), (14, 'Paint & Glaze'), (14, 'Paint & Distress'), (18, 'Paint, Glaze & Distress')], default=0)),
                ('exterior_material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exterior_specifications', to='cabinets_app.Material')),
                ('interior_material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interior_specifications', to='cabinets_app.Material')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='cabinets_app.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Drawer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drawers', to='cabinets_app.Cabinet')),
            ],
        ),
        migrations.AddField(
            model_name='cabinet',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cabinets', to='cabinets_app.Project'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='specification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cabinets', to='cabinets_app.Specification'),
        ),
    ]