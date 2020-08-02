# Generated by Django 3.0.8 on 2020-08-01 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0003_auto_20200801_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='login_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='login_author_answer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='login_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='login_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
