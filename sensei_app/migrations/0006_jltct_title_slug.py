# Generated by Django 3.1 on 2020-10-27 09:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0005_auto_20201027_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='jltct',
            name='title_slug',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
