# Generated by Django 3.1 on 2020-12-21 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0035_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20, null=True)),
                ('category_slug', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20, null=True)),
                ('tag_slug', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='material',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='upload_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_materials', to='sensei_app.materialcategory'),
        ),
        migrations.AddField(
            model_name='material',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='tag_materials', to='sensei_app.MaterialTag'),
        ),
    ]
