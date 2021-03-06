# Generated by Django 3.1 on 2020-12-28 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0045_blog_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='jltctcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
                ('category_slug', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='jltct',
            options={'ordering': ['category', 'number']},
        ),
        migrations.RemoveField(
            model_name='jltct',
            name='section',
        ),
        migrations.DeleteModel(
            name='jltctsection',
        ),
        migrations.AddField(
            model_name='jltct',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_name', to='sensei_app.jltctcategory'),
        ),
    ]
