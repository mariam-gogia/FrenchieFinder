# Generated by Django 3.1.1 on 2020-11-27 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puppysearch', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='breeder',
            new_name='review',
        ),
    ]
