# Generated by Django 3.1 on 2020-11-14 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0010_auto_20201112_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterPerk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perk', models.CharField(blank=True, max_length=100, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
    ]