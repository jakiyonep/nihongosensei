# Generated by Django 3.1 on 2020-10-29 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=150, verbose_name='ニックネーム'),
        ),
    ]
