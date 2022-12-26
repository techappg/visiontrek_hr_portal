# Generated by Django 2.2 on 2022-12-19 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hr', '0015_auto_20221219_0627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='task/'),
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('learning', 'learning'), ('development', 'development'), ('task', 'task'), ('project', 'project'), ('deployment', 'deployment')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('detail', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]