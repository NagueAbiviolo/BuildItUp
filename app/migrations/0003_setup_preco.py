<<<<<<< HEAD
# Generated by Django 5.1.3 on 2024-11-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cpu_chipset'),
    ]

    operations = [
        migrations.AddField(
            model_name='setup',
            name='preco',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
=======
# Generated by Django 5.1.3 on 2024-11-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cpu_chipset'),
    ]

    operations = [
        migrations.AddField(
            model_name='setup',
            name='preco',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
>>>>>>> 0b70f733a5fbdca43ff5f98bde71b74d625c3dbb
