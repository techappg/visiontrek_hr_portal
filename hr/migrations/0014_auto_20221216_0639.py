# Generated by Django 2.2 on 2022-12-16 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0013_task_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='task/'),
        ),
    ]