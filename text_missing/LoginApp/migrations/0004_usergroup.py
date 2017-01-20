# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-20 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LoginApp', '0003_manager_reader'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('leader', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Leader', to='LoginApp.Client')),
                ('users', models.ManyToManyField(related_name='Users', to='LoginApp.Client')),
            ],
        ),
    ]
