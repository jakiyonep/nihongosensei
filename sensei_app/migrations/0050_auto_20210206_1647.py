# Generated by Django 3.1 on 2021-02-06 07:47

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0049_auto_20210206_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examexp',
            name='answer_1',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examexp',
            name='answer_2',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examexp',
            name='answer_3',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examexp',
            name='answer_4',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examexp',
            name='answer_5',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]
