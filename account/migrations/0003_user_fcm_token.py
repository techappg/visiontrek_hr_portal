# Generated by Django 2.2 on 2022-12-17 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fcm_token',
            field=models.TextField(default=''),
        ),
    ]
