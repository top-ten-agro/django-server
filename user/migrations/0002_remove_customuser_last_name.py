# Generated by Django 4.2 on 2023-07-13 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
    ]
