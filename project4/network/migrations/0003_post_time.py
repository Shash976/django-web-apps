# Generated by Django 4.0.1 on 2022-03-14 15:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
