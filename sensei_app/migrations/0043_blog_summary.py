# Generated by Django 3.1 on 2020-12-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0042_blog_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
