# Generated by Django 5.1.2 on 2024-11-23 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_setup_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peca',
            name='tdp',
            field=models.IntegerField(default=0),
        ),
    ]