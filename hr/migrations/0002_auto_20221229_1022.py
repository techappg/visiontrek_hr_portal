# Generated by Django 2.2 on 2022-12-29 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punch',
            name='hours',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
