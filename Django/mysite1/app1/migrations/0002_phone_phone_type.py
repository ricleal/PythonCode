# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='phone_type',
            field=models.IntegerField(default=0, max_length=1, choices=[(0, b'Home'), (1, b'Mobile'), (2, b'Unknown')]),
            preserve_default=True,
        ),
    ]
