# Generated by Django 4.2.3 on 2023-11-11 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('au', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='my_buyes',
            name='adress',
            field=models.CharField(max_length=100),
        ),
    ]