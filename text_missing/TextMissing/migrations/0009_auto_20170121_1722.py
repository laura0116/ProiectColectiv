# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-21 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('TextMissing', '0008_auto_20170121_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='city',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='country',
            field=django_countries.fields.CountryField(default=None, max_length=2),
        ),
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='financing_source',
            field=models.CharField(choices=[('no financing', 'No financing'), ('college budget', 'College budget'), ('university budget', 'University budget'), ('project/grant', 'Project/grant financing'), ('combined', 'Combined financing')], default='no financing', max_length=20),
        ),
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='phone_number',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='sum',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='sum_motivation',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='travel_mean',
            field=models.CharField(choices=[('auto', 'Auto'), ('plane', 'Plane'), ('boat', 'Boat'), ('train', 'Train')], default='auto', max_length=20),
        ),
        migrations.AddField(
            model_name='rectordispositiondocument',
            name='travel_purpose',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
