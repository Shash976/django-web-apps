# Generated by Django 4.0.1 on 2022-03-23 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_user_followers_user_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
    ]
