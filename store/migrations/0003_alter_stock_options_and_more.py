# Generated by Django 4.2 on 2023-05-07 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['-stock_created']},
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='created_at',
            new_name='stock_created',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='updated_at',
            new_name='stock_updated',
        ),
    ]