# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-01 16:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sixerrapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gig',
            name='avgstars',
        ),
        migrations.RemoveField(
            model_name='gig',
            name='boughttimes',
        ),
        migrations.RemoveField(
            model_name='gig',
            name='sellmsg',
        ),
    ]