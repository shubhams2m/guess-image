# Generated by Django 2.2 on 2019-12-11 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artigone', '0002_option_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='player2', to=settings.AUTH_USER_MODEL),
        ),
    ]
