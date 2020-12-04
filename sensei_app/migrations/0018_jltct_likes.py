# Generated by Django 3.1 on 2020-11-26 11:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0017_termsconditions_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='jltct',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]