# Generated by Django 3.1.1 on 2020-11-27 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puppysearch', '0002_auto_20201127_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='color',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
