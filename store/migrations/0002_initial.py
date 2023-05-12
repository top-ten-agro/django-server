# Generated by Django 4.2 on 2023-05-12 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storerole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='customers',
            field=models.ManyToManyField(related_name='stores', through='store.Balance', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='store',
            name='employees',
            field=models.ManyToManyField(related_name='stores', through='store.StoreRole', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='products',
            field=models.ManyToManyField(related_name='stores', through='store.Stock', to='product.product'),
        ),
        migrations.AddField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='product.product'),
        ),
        migrations.AddField(
            model_name='stock',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='store.store'),
        ),
        migrations.AddField(
            model_name='balance',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='balance',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='store.store'),
        ),
        migrations.AlterUniqueTogether(
            name='storerole',
            unique_together={('store', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together={('store', 'product')},
        ),
        migrations.AlterUniqueTogether(
            name='balance',
            unique_together={('store', 'customer')},
        ),
    ]
