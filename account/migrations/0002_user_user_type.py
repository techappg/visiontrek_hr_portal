# Generated by Django 2.2 on 2022-12-05 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[(1, 'Admin'), (2, 'Hr'), (3, 'Employee')], default=1, max_length=10, null=True),
        ),
    ]
