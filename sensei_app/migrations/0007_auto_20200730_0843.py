# Generated by Django 3.0.8 on 2020-07-29 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0006_auto_20200730_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.IntegerField(choices=[(1, '日本語'), (2, '日本語教師・日本語指導'), (3, '日本語教育能力検定試験'), (4, 'その他')]),
        ),
    ]
