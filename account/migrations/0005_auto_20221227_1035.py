# Generated by Django 2.2 on 2022-12-27 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_reporting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporting',
            name='new_reporting_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='New_reporting_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reporting',
            name='report_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Reporting_to', to=settings.AUTH_USER_MODEL),
        ),
    ]