# Generated by Django 2.2 on 2022-12-19 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0017_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='detail',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
