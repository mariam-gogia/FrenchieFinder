# Generated by Django 3.1.1 on 2020-11-28 08:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puppysearch', '0010_remove_user_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]