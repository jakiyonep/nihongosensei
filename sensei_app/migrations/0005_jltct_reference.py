# Generated by Django 3.1 on 2020-10-30 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0004_jltct_related_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='jltct',
            name='reference',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]