# Generated by Django 3.1 on 2020-12-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0034_auto_20201206_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='MinnaNoMaterial')),
            ],
        ),
    ]