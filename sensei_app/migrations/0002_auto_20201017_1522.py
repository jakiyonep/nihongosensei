# Generated by Django 3.1 on 2020-10-17 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='question',
            new_name='question_num',
        ),
    ]
