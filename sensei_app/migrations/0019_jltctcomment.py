# Generated by Django 3.1 on 2020-11-28 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensei_app', '0018_jltct_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='JltctComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_public', models.BooleanField(default=False)),
                ('login_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_comments_login_author', to=settings.AUTH_USER_MODEL)),
                ('note', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_comments', to='sensei_app.jltct')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]