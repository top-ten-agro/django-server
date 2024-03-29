# Generated by Django 4.2 on 2023-05-19 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cash_in', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='customer.customer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.TextField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customers', models.ManyToManyField(related_name='depots', through='depot.Balance', to='customer.customer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('stock_created', models.DateTimeField(auto_now_add=True)),
                ('stock_updated', models.DateTimeField(auto_now=True)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='depot.depot')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='product.product')),
            ],
            options={
                'ordering': ['-stock_created'],
                'unique_together': {('depot', 'product')},
            },
        ),
        migrations.CreateModel(
            name='DepotRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('MANAGER', 'Manager'), ('OFFICER', 'Officer'), ('DIRECTOR', 'Director')], default='OFFICER', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='depot.depot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('depot', 'user')},
            },
        ),
        migrations.AddField(
            model_name='depot',
            name='employees',
            field=models.ManyToManyField(related_name='depots', through='depot.DepotRole', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='depot',
            name='products',
            field=models.ManyToManyField(related_name='depots', through='depot.Stock', to='product.product'),
        ),
        migrations.AddField(
            model_name='balance',
            name='depot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='depot.depot'),
        ),
        migrations.AddField(
            model_name='balance',
            name='officer',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('depot', models.F('depot'))), null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='officers', to='depot.depotrole'),
        ),
        migrations.AlterUniqueTogether(
            name='balance',
            unique_together={('depot', 'customer')},
        ),
    ]
