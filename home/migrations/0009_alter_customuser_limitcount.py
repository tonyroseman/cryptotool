# Generated by Django 4.2.4 on 2023-09-12 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_telegramlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='limitcount',
            field=models.DecimalField(decimal_places=1, default=500, max_digits=5),
        ),
    ]