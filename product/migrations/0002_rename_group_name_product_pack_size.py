# Generated by Django 4.2 on 2023-05-14 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='group_name',
            new_name='pack_size',
        ),
    ]
