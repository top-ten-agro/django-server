# Generated by Django 4.2 on 2023-05-07 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('store', '0003_alter_stock_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together={('store', 'product')},
        ),
    ]