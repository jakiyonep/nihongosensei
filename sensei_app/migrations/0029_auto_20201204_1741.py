# Generated by Django 3.1 on 2020-12-04 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0028_auto_20201202_1934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examexp',
            options={'ordering': ['year', 'section', 'question_num', 'question_num_small']},
        ),
        migrations.AddField(
            model_name='examexp',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
