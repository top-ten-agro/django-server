# Generated by Django 4.2 on 2023-05-11 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('store', '0005_alter_balance_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='customer.customer'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='store.store'),
        ),
    ]