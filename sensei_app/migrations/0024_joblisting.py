# Generated by Django 3.1 on 2020-12-02 09:25

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0023_auto_20201201_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_id', models.CharField(blank=True, max_length=20, null=True)),
                ('organization_name', models.CharField(max_length=50)),
                ('job_title', models.CharField(max_length=50)),
                ('contract_type', models.CharField(max_length=50)),
                ('workplace', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
    ]
