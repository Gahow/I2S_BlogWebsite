# Generated by Django 4.1.2 on 2022-11-08 03:39

import blog.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('url_name', models.CharField(max_length=100)),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('introduction', models.TextField()),
                ('body', models.FileField(upload_to=blog.models.get_post_path)),
            ],
        ),
    ]
