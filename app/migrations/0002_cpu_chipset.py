# Generated by Django 5.1.2 on 2024-10-29 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='chipset',
            field=models.CharField(max_length=100, null=True),
        ),
    ]