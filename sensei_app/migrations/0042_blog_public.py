# Generated by Django 3.1 on 2020-12-23 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0041_auto_20201223_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
