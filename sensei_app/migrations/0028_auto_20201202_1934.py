# Generated by Django 3.1 on 2020-12-02 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0027_auto_20201202_1930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examexp',
            old_name='queston_num_small',
            new_name='question_num_small',
        ),
    ]