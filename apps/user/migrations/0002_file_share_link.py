# Generated by Django 5.1.1 on 2024-09-10 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='share_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
