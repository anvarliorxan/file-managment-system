# Generated by Django 4.2.16 on 2024-09-12 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledtask',
            name='status',
            field=models.CharField(choices=[('on_hold', 'On Hold'), ('completed', 'Completed')], default='on_hold', max_length=25),
        ),
    ]
