# Generated by Django 3.0.8 on 2020-07-29 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0002_auto_20200729_1408'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
    ]