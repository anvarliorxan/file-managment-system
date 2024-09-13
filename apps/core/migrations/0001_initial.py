# Generated by Django 5.1.1 on 2024-09-11 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0005_alter_file_expiration_date_alter_file_hashtags'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=255)),
                ('scheduled_time', models.DateTimeField()),
                ('task_id', models.CharField(blank=True, max_length=255, null=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_task', to='user.file')),
            ],
        ),
    ]
