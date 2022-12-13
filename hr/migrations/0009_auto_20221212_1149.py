# Generated by Django 2.2 on 2022-12-12 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hr', '0008_punch_punch_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='punch',
            name='marked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='punch',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
