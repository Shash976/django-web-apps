# Generated by Django 4.0.3 on 2022-04-30 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0021_remove_post_image_alter_post_time_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 30, 11, 52, 16, 418726)),
        ),
    ]
