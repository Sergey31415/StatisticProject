# Generated by Django 5.1.4 on 2024-12-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_prepod_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='prepod',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prepod',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
