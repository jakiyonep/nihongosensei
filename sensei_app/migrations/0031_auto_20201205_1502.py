# Generated by Django 3.1 on 2020-12-05 06:02

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0030_auto_20201204_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jltctcomment',
            name='content',
            field=markdownx.models.MarkdownxField(null=True),
        ),
    ]
