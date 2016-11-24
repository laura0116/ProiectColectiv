# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LoginApp', '0002_contributor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('client_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='LoginApp.Client')),
            ],
            bases=('LoginApp.client',),
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('client_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='LoginApp.Client')),
            ],
            bases=('LoginApp.client',),
        ),
    ]
