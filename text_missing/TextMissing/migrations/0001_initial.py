# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('LoginApp', '0003_manager_reader'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=64)),
                ('size', models.IntegerField(default=0)),
                ('version', models.CharField(max_length=64)),
                ('creation_date', models.DateField()),
                ('last_update', models.DateField()),
                ('abstract', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('final', 'Final'), ('finalRevised', 'Final revised'), ('blocked', 'Blocked')], max_length=20)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LoginApp.Client')),
            ],
        ),
    ]
