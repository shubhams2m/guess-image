# Generated by Django 2.2 on 2019-12-12 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artigone', '0004_auto_20191211_1955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='option',
            old_name='image_url',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='image_url',
            new_name='image',
        ),
    ]